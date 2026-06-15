import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from sqlalchemy.future import select
from sqlalchemy import extract
from ..model.User import TASK_HANDLERS
# Импорт aioscheduler
from aioscheduler import TimedScheduler

from .LogsMaker import LogsMaker
from ..base.pSQL.objects.App import get_async_db, AsyncSessionLocal
# from ..model.User import User
# from ..base.pSQL.models.User import User
from .MerchStore import MerchStore
from .Peer import Peer
from .SendMail import SendEmail

import redis.asyncio as redis
import json, time

import os
from dotenv import load_dotenv

load_dotenv()
# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================

# Глобальный экземпляр планировщика
_scheduler = None
_scheduler_task = None
_scheduler_manager = None


def make_date_valid(date):
    if date is not None:
        if isinstance(date, str):
            if '-' in date:
                if 'T' in date:
                    try:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                    except:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        return datetime.strptime(date, '%Y-%m-%d')
                else:
                    try:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    except:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        return datetime.strptime(date, '%Y-%m-%d')
            elif '.' in date:
                try:
                    return datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                    # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                except:
                    # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                    return datetime.strptime(date, '%d.%m.%Y')
                    # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
# ==================== РЕАЛИЗАЦИЯ ЗАПРОСОВ ====================

async def get_today_birthdays() -> List[int]:
    """
    Найти всех пользователей, у которых сегодня день рождения
    Возвращает список ID пользователей
    Удаляет поздравления за прошлый месяц
    """
    from ..base.pSQL.models.User import User
    from ..base.pSQL.objects.UserModel import UserModel
    async with AsyncSessionLocal() as db:
        # today = datetime.now()
        today = datetime.strptime('12.06.2026', '%d.%m.%Y')
        #отсчитываем месяц чтобы почистить поздравления
        month_ago = today - timedelta(days=30)
        query = select(User.id, User.indirect_data).where(
            (extract('month', User.personal_birthday) == month_ago.month) &
            (extract('day', User.personal_birthday) == month_ago.day)
        )
        result = await db.execute(query)
        last_birthdays = result.mappings().all()

        for user in last_birthdays:
            user['indirect_data']['congratulations'] = []
            user_bd = await db.get(User, user['id'])
            # Обновляем только переданные поля
            setattr(user_bd, 'indirect_data', user['indirect_data'])
        await db.commit()


        # today = datetime.strptime('22.03.2026', '%d.%m.%Y')
        query = select(User.id).where(
            (extract('month', User.personal_birthday) == today.month) &
            (extract('day', User.personal_birthday) == today.day) &
            (User.active == True)
        )
        
        result = await db.execute(query)
        birthdays = result.scalars().all()
        
        LogsMaker().info_message(f"Найдено пользователей с днём рождения: {len(birthdays)}")
        return birthdays

async def get_new_users(session) -> List[int]:
    from sqlalchemy import select
    
    from ..base.pSQL.objects.App import NewUser
    
    
    # Выполняем запрос
    stmt = select(NewUser)
    result = await session.execute(stmt)
    ids = result.scalars().all()
    return ids

async def get_registration_anniversaries() -> List[Dict[str, Any]]:
    """
    Найти юбилеи регистрации (5, 10, 15, 20, 25, 30 лет)
    Возвращает список словарей с информацией
    """
    async with AsyncSessionLocal() as db:
        today = datetime.now()
        
        # Получаем всех, у кого сегодня день регистрации
        query = select(
            User.id,
            User.created_at,
            User.email,
            User.username
        ).where(
            (extract('month', User.created_at) == today.month) &
            (extract('day', User.created_at) == today.day) &
            (User.is_active == True)
        )
        
        result = await db.execute(query)
        users = result.all()
        
        # Рассчитываем стаж и фильтруем юбилеи
        anniversary_users = []
        anniversary_years = {5, 10, 15, 20, 25, 30}
        
        for user in users:
            years_ago = today.year - user.created_at.year
            
            # Корректируем, если день в году ещё не наступил
            if (today.month, today.day) < (user.created_at.month, user.created_at.day):
                years_ago -= 1
            
            if years_ago in anniversary_years:
                anniversary_users.append({
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'years': years_ago,
                    'registered_at': user.created_at
                })
        
        LogsMaker().info_message(f"Найдено юбилеев регистрации: {len(anniversary_users)}")
        return anniversary_users

async def check_inactive_users() -> List[int]:
    """
    Проверка пользователей, которые не заходили больше 30 дней
    """
    async with AsyncSessionLocal() as db:
        month_ago = datetime.now() - timedelta(days=30)
        
        query = select(User.id).where(
            (User.last_login < month_ago) &
            (User.is_active == True)
        )
        
        result = await db.execute(query)
        inactive_users = result.scalars().all()
        
        LogsMaker().info_message(f"Найдено неактивных пользователей: {len(inactive_users)}")
        return inactive_users

async def check_trial_expiring() -> List[int]:
    """
    Проверка пользователей, у которых скоро закончится триал
    (если у вас есть такая функциональность)
    """
    async with AsyncSessionLocal() as db:
        three_days_later = datetime.now() + timedelta(days=3)
        
        query = select(User.id).where(
            (User.trial_ends_at <= three_days_later) &
            (User.trial_ends_at >= datetime.now()) &
            (User.is_active == True) &
            (User.subscription_status == 'trial')
        )
        
        result = await db.execute(query)
        expiring_users = result.scalars().all()
        
        LogsMaker().info_message(f"Найдено пользователей с истекающим триалом: {len(expiring_users)}")
        return expiring_users

# ==================== ФУНКЦИИ ОБРАБОТКИ ====================

async def send_birthday_notifications(user_ids: List[int]):
    """
    Отправка уведомлений о днях рождения
    """
    from ..model.User import User
    from .SendMail import SendEmail
    if not user_ids:
        return
    
    logger = LogsMaker()
    logger.info_message(f"Отправка поздравлений с ДР для {len(user_ids)} пользователей")
    
    try:
        async with AsyncSessionLocal() as db:
            for user_id in user_ids:
                send_data = {
                    "uuid_from": 2,  # В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
                    "uuid_to": int(user_id),
                    "activities_id": 1,  # В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
                    "description": f"Поздравительные баллы. С днем рождения!"
                }
                send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)
                if send_point['status'] == 'info':
                    user_info = await User(id=int(user_id)).search_by_id(session=db)
                    if 'email' in user_info and user_info['email']:
                        data = {'sender': user_info['email']}
                        SendEmail(data=data).send_to_birthday_notifications()
            await db.commit()
            logger.info_message("Уведомления о днях рождения успешно отправлены")
    
    except Exception as e:
        logger.error_message(f"Ошибка при отправке уведомлений о днях рождения: {e}")
        # Откатываем изменения в случае ошибки
        if 'db' in locals():
            await db.rollback()

async def send_to_new_users():
    """
    Отправка баллов новым сотрудникам
    """
    logger = LogsMaker()
    logger.info_message(f"Отправка баллов новым сотрудникам")
    from ..model.User import User
    try:
        async with AsyncSessionLocal() as db:
            users = await get_new_users(session=db)
            for user_id in users:
                send_data = {
                    "uuid_from": 2, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
                    # "uuid_to": int(user_id['id']),
                    "uuid_to": int(user_id),
                    "activities_id": 3, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
                    "description": f"Добро пожаловать в ЭМК!"
                }
                send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)

                if send_point['status'] == 'info':
                    user_info = await User(id=int(user_id)).search_by_id(session=db)
                    if 'email' in user_info and user_info['email']:
                        data = {'sender': user_info['email']}
                        SendEmail(data=data).send_to_new_wrokers()
            
            await db.commit()
            logger.info_message("Баллы новым сотрудникам успешно отправлены")
    
    except Exception as e:
        logger.error_message(f"Ошибка при отправке уведомлений о днях рождения: {e}")
        # Откатываем изменения в случае ошибки
        if 'db' in locals():
            await db.rollback()

async def send_to_new_idea():
    """
    Функция отправляет баллы за идеи со статусом "В работе", "Реализовано"
    """
    try:
        from .Idea import Idea
        #Дата запуска капитала ЭМК
        LogsMaker().info_message("Отправка баллов пользователям за идею")
        LAUNCH_DATE_OF_CAPITAL_EMK = datetime.strptime("03.02.2026", '%d.%m.%Y')

        #Статус с которым выдаем баллы
        # STATUS_IDEA = "Принято"
        STATUS_IDEA = ["В работе", "Реализовано"]
        #Получаем все идеи
        all_ideas = await Idea().validate_ideas()
        async with AsyncSessionLocal() as db:
            for idea in all_ideas:
                # if '-' in idea['date_create']:
                #     date_idea = datetime.strptime(idea['date_create'].split('T')[0], '%Y-%m-%d')
                # else:
                date_idea = make_date_valid(idea['date_create'])
                #пропускаем идеи которые были отправлены до запуска каптиала ЭМК
                if date_idea < LAUNCH_DATE_OF_CAPITAL_EMK:
                    continue
                #пропускаем идеи у которых статус не соответствует 
                # if idea['status'] != STATUS_IDEA:
                if idea['status'] not in STATUS_IDEA:
                    continue
                
                send_data = {
                    "uuid_from": 2, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
                    "uuid_to": int(idea['user_id']),
                    "activities_id": 4, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
                    "description": idea["number"]
                }
                send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)
                
            await db.commit()
        return True
    except Exception as e:
        LogsMaker().error_message(f"Ошибка при отправке баллов за идею: {e}")
        # Откатываем изменения в случае ошибки
        if 'db' in locals():
            await db.rollback()
                
async def send_to_anniversary_in_company():
    """
    Функция отправляет баллы за годовщину
    """     
    LogsMaker().info_message(f"Отправка баллов за годовщину")
    from ..model.User import User  
    try:
        async with AsyncSessionLocal() as db:
            await User().anniversary_in_company(session=db)
        
    except Exception as e:
        LogsMaker().error_message(f"Ошибка при отправке баллов за годовщину: {e}")
        # Откатываем изменения в случае ошибки
        if 'db' in locals():
            await db.rollback()


async def handle_inactive_users(user_ids: List[int]):
    """
    Обработка неактивных пользователей
    """
    if not user_ids:
        return
    
    logger = LogsMaker()
    logger.info_message(f"Обработка {len(user_ids)} неактивных пользователей")
    
    # Здесь можно добавить логику для неактивных пользователей
    # Например, отправка напоминания или изменение статуса

# ==================== ОСНОВНАЯ ЗАДАЧА ====================
async def weekly_check():
    """
    Основная задача, которая выполняется раз в неделю
    Скачивает из битрикс данные о структуре
    """
    from ..model.Department import Department
    from ..model.UsDep import UsDep
    logger = LogsMaker()
    logger.info_message("=" * 50)
    logger.info_message(f"НАЧАЛО ЕЖЕНЕДЕЛЬНОГО СКАЧИВАНИЯ - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        async with AsyncSessionLocal() as db:
            await Department().fetch_departments_data(session=db)
            await UsDep().get_usr_dep(session=db)

        logger.info_message(f"ЗАВЕРШЕНИЕ ЕЖЕНЕДЕЛЬНОГО СКАЧИВАНИЯ - УСПЕХ")
    except Exception as e:
        logger.error_message(f"ОШИБКА в еженедельном скачивании: {e}")
        import traceback
        logger.error_message(traceback.format_exc())


async def daily_check():
    """
    Основная задача, которая выполняется каждый день
    Собирает все проверки в одну
    """
    logger = LogsMaker()
    logger.info_message("=" * 50)
    logger.info_message(f"НАЧАЛО ЕЖЕДНЕВНОЙ ПРОВЕРКИ - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Дни рождения
        birthday_users = await get_today_birthdays()
        await send_birthday_notifications(birthday_users)
        
        # 2. Новые сотрудники
        await send_to_new_users()
        
        # 3. Идеи
        await send_to_new_idea()
        
        # 4. Годовщина
        await send_to_anniversary_in_company()
        
        logger.info_message(f"ЗАВЕРШЕНИЕ ЕЖЕДНЕВНОЙ ПРОВЕРКИ - УСПЕХ")
        
    except Exception as e:
        logger.error_message(f"ОШИБКА в ежедневной проверке: {e}")
        import traceback
        logger.error_message(traceback.format_exc())
        
    logger.info_message("=" * 50)

async def test_task():
    """
    Тестовая задача для проверки работы планировщика
    """
    logger = LogsMaker()
    logger.info_message(f"Тестовая задача выполнена: {datetime.now().strftime('%H:%M:%S')}")

# ==================== КЛАСС ДЛЯ УПРАВЛЕНИЯ ПЛАНИРОВЩИКОМ ====================

class AioSchedulerManager:
    """
    Менеджер для управления планировщиком aioscheduler
    """
    
    def __init__(self):
        self.scheduler = None
        self.scheduler_task = None
        self.is_running = False
        self.jobs = {}  # Словарь для хранения задач: job_id -> task
        # self.redis = RedisStorage().client
        redis_host = "redis"
        redis_port = 6379
        redis_db = 0
        redis_password = os.getenv("pswd")

        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )
    
    async def init_scheduler(self):
        """
        Инициализация планировщика
        """
        logger = LogsMaker()
        
        try:
            # Создаем экземпляр TimedScheduler
            self.scheduler = TimedScheduler()
            
            # Настраиваем планировщик (по желанию)
            # Максимальное количество параллельных задач
            self.scheduler.max_tasks = 10
            
            logger.info_message("Планировщик aioscheduler инициализирован")
            return self.scheduler
            
        except Exception as e:
            logger.error_message(f"Ошибка инициализации планировщика: {e}")
            import traceback
            logger.error_message(traceback.format_exc())
            raise
    
    def schedule_periodic_task(self, coro_func, interval_seconds: int = 300):
        """
        Запланировать периодическую задачу (исправленная версия)
        
        ВНИМАНИЕ: aioscheduler.schedule() ожидает datetime для when, а не int!
        Правильное использование: schedule(coro, delay_seconds)
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        # Создаем обертку для периодического выполнения
        async def periodic_wrapper():
            while True:
                try:
                    # Ждем указанный интервал
                    await asyncio.sleep(interval_seconds)
                    
                    # Выполняем задачу
                    await coro_func()
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger = LogsMaker()
                    logger.error_message(f"Ошибка в периодической задаче: {e}")
                    await asyncio.sleep(60)  # Ждем минуту при ошибке
        
        # Запускаем обертку через asyncio.create_task
        # и добавляем в планировщик для отслеживания
        task = asyncio.create_task(periodic_wrapper())
        
        # Сохраняем задачу
        job_id = f"periodic_{coro_func.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Периодическая задача '{coro_func.__name__}' запланирована каждые {interval_seconds} секунд")
        
        return job_id
    
    def schedule_daily_at_time(self, coro_func, hour: int, minute: int = 0):
        """
        Запланировать выполнение задачи в определенное время каждый день
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        async def daily_time_wrapper():
            while True:
                try:
                    now = datetime.now()
                    
                    # Вычисляем время следующего запуска
                    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    # Если время уже прошло сегодня, планируем на завтра
                    if now >= target_time:
                        target_time += timedelta(days=1)
                    
                    # Ждем до целевого времени
                    wait_seconds = (target_time - now).total_seconds()
                    
                    if wait_seconds > 0:
                        logger = LogsMaker()
                        logger.info_message(f"Задача '{coro_func.__name__}' будет выполнена в "
                                           f"{target_time.strftime('%H:%M')} "
                                           f"(через {wait_seconds:.0f} секунд)")
                        
                        await asyncio.sleep(wait_seconds)
                    
                    # Выполняем задачу
                    logger.info_message(f"Выполнение задачи '{coro_func.__name__}' в {datetime.now().strftime('%H:%M')}")
                    await coro_func()
                    
                    # Ждем минуту после выполнения, чтобы не запускать снова
                    await asyncio.sleep(60)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error_message(f"Ошибка в ежедневной задаче: {e}")
                    await asyncio.sleep(60)
        
        # Запускаем обертку
        task = asyncio.create_task(daily_time_wrapper())
        
        # Сохраняем задачу
        job_id = f"daily_{hour:02d}{minute:02d}_{coro_func.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Задача '{coro_func.__name__}' запланирована ежедневно в {hour:02d}:{minute:02d}")
        
        return job_id
    
    def schedule_weekly_at_time(self, coro_func, days):
        """
        Запланировать выполнение задачи в определенное время каждый день
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        async def daily_time_wrapper():
            while True:
                try:
                    now = datetime.now()
                    
                    # Вычисляем время следующего запуска
                    target_time = now.replace(day=(now.day + days), hour=2, minute=0, second=0, microsecond=0)
                    
                    # Если время уже прошло сегодня, планируем на завтра
                    if now >= target_time:
                        target_time += timedelta(days=1)
                    
                    # Ждем до целевого времени
                    wait_seconds = (target_time - now).total_seconds()
                    
                    if wait_seconds > 0:
                        logger = LogsMaker()
                        logger.info_message(f"Задача '{coro_func.__name__}' будет выполнена в "
                                           f"{target_time.strftime('%d:%H:%M')} "
                                           f"(через {wait_seconds:.0f} секунд)")
                        
                        await asyncio.sleep(wait_seconds)
                    
                    # Выполняем задачу
                    logger.info_message(f"Выполнение задачи '{coro_func.__name__}' в {datetime.now().strftime('%d:%H:%M')}")
                    await coro_func()
                    
                    # Ждем минуту после выполнения, чтобы не запускать снова
                    await asyncio.sleep(60)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error_message(f"Ошибка в ежедневной задаче: {e}")
                    await asyncio.sleep(60)
        
        # Запускаем обертку
        task = asyncio.create_task(daily_time_wrapper())
        
        # Сохраняем задачу
        job_id = f"weekly_{2:}{00}_{coro_func.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Задача '{coro_func.__name__}' запланирована раз в неделю в 02:00")
        
        return job_id
    
    async def scheduler_worker(self):
        """
        Основной рабочий процесс планировщика
        """
        import os
        logger = LogsMaker()
        
        try:
            # Инициализируем планировщик
            await self.init_scheduler()
            
            # Запускаем планировщик
            self.scheduler.start()
            self.is_running = True
            
            logger.info_message("Планировщик aioscheduler запущен")
            
            # Добавляем задачи по умолчанию
            
            # 1. Ежедневная проверка каждые 5 минут (исправленный метод)
            # daily_job_id = self.schedule_periodic_task(daily_check, interval_seconds=60)
            main_portal = os.getenv('HOST')
            if 'intranet.emk.ru' in main_portal:
                # 2. Ежедневная проверка в 7 утра
                daily_7am_job_id = self.schedule_daily_at_time(daily_check, hour=7, minute=0)

                # 2. Раз в неделю скачиваем подразделения и связь подразделений и пользователей
                weekly_job = self.schedule_weekly_at_time(weekly_check, days=6)

                self.redis_worker_task = asyncio.create_task(self._redis_worker())
            
            # 3. Тестовая задача каждую минуту (для мониторинга)
            # test_job_id = self.schedule_periodic_task(test_task, interval_seconds=60)
            
            logger.info_message(f"Задач в планировщике: {len(self.jobs)}")
            
            # Бесконечный цикл для поддержания работы
            while self.is_running:
                await asyncio.sleep(60)  # Проверяем каждую минуту
                
                # Можно добавить периодическую проверку состояния
                if datetime.now().minute == 0:  # Каждый час
                    active_tasks = len([t for t in self.jobs.values() if not t.done()])
                    logger.info_message(f"Планировщик работает, активных задач: {active_tasks}")
        
        except asyncio.CancelledError:
            logger.info_message("Планировщик остановлен по запросу")
        
        except Exception as e:
            logger.error_message(f"Критическая ошибка в планировщике: {e}")
            import traceback
            logger.error_message(traceback.format_exc())
        
        finally:
            self.is_running = False
            if self.scheduler:
                self.scheduler.stop()
                if hasattr(self, 'redis_worker_task'):
                    self.redis_worker_task.cancel()
    
    async def start(self):
        """
        Запуск планировщика
        """
        if not self.is_running:
            self.scheduler_task = asyncio.create_task(self.scheduler_worker())
            return self.scheduler_task
    
    async def stop(self):
        """
        Остановка планировщика
        """
        if self.is_running:
            logger = LogsMaker()
            logger.info_message("Остановка планировщика aioscheduler...")
            
            self.is_running = False
            
            # Отменяем все задачи
            for job_id, task in list(self.jobs.items()):
                try:
                    if not task.done():
                        task.cancel()
                except:
                    pass
            
            self.jobs.clear()
            
            # Останавливаем планировщик
            if self.scheduler:
                self.scheduler.stop() 
            
            # Отменяем задачу планировщика
            if self.scheduler_task and not self.scheduler_task.done():
                self.scheduler_task.cancel()
                try:
                    await self.scheduler_task
                except asyncio.CancelledError:
                    pass

            if hasattr(self, 'redis_worker_task'):
                self.redis_worker_task.cancel()

            logger.info_message("Планировщик aioscheduler остановлен")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Получить статус планировщика
        """
        if not self.scheduler:
            return {
                "status": "not_initialized",
                "running": False,
                "jobs_count": 0,
                "jobs": []
            }
        
        jobs_info = []
        for job_id, task in self.jobs.items():
            jobs_info.append({
                "id": job_id,
                "done": task.done(),
                "cancelled": task.cancelled(),
                "running": not task.done() and not task.cancelled()
            })
        
        return {
            "status": "running" if self.is_running else "stopped",
            "running": self.is_running,
            "jobs_count": len(self.jobs),
            "active_jobs": len([t for t in self.jobs.values() if not t.done()]),
            "jobs": jobs_info
        }
    
    def add_job(self, coro_func, interval_seconds: int = 300, job_name: str = None):
        """
        Добавить периодическую задачу
        """
        if job_name:
            func_name = job_name
        else:
            func_name = coro_func.__name__
        
        # Создаем обертку с именем
        async def named_wrapper():
            while True:
                try:
                    await asyncio.sleep(interval_seconds)
                    await coro_func()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger = LogsMaker()
                    logger.error_message(f"Ошибка в задаче '{func_name}': {e}")
                    await asyncio.sleep(60)
        
        # Запускаем задачу
        task = asyncio.create_task(named_wrapper())
        
        job_id = f"{func_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Задача '{func_name}' добавлена с интервалом {interval_seconds} секунд")
        
        return job_id

    async def add_redis_task(self, task_name: str, delay_seconds: float, *args, **kwargs):
        """
        Поставить задачу в Redis с отложенным выполнением.
        task_name – имя функции-обработчика, зарегистрированной в TASK_HANDLERS.
        """
        logger = LogsMaker()
        if not self.redis:
            raise RuntimeError("Redis не инициализирован")
        
        task_id = f"{int(time.time() * 1000)}-{id(args)}"
        execute_at = time.time() + delay_seconds

        # Сериализуем данные
        task_data = {
            "task_name": task_name,
            "args": json.dumps(args),
            "kwargs": json.dumps(kwargs)
        }
        
        async with self.redis.pipeline() as pipe:
            # Сохраняем детали задачи в Hash
            await pipe.hset(f"scheduler:task:{task_id}", mapping=task_data)
            # Добавляем в очередь с временем выполнения
            await pipe.zadd("scheduler:queue", {task_id: execute_at})
            await pipe.execute()

        logger.info_message(f"Задача '{task_name}' (ID: {task_id}) запланирована через {delay_seconds} сек в Redis")
        return task_id
    
    async def _redis_worker(self):
        """Фоновый воркер, обрабатывающий задачи из Redis."""
        logger = LogsMaker()
        logger.info_message("Redis worker запущен")
        while self.is_running:
            try:
                now = time.time()
                # Получаем все task_id, готовые к выполнению (score <= now)
                raw_tasks = await self.redis.zrangebyscore(
                    "scheduler:queue", 0, now, withscores=True
                )
                if raw_tasks:
                    task_ids = []
                    for member, score in raw_tasks:
                        # member может быть bytes или str
                        if isinstance(member, bytes):
                            task_ids.append(member.decode())
                        else:
                            task_ids.append(member)
                    logger.info_message(f"Найдено {len(task_ids)} готовых задач в Redis")
                    for task_id in task_ids:
                        await self._execute_redis_task(task_id)

                await asyncio.sleep(1)  # опрос раз в секунду
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error_message(f"Ошибка в Redis worker: {e}")
                await asyncio.sleep(5)

    async def _execute_redis_task(self, task_id: str):
        """Выполнить одну задачу из Redis по её ID."""
        logger = LogsMaker()
        task_key = f"scheduler:task:{task_id}"
        # Атомарно получаем данные и удаляем из очереди и хранилища
        async with self.redis.pipeline() as pipe:
            pipe.hgetall(task_key)
            pipe.zrem("scheduler:queue", task_id)
            pipe.delete(task_key)
            results = await pipe.execute()

        task_data_raw = results[0]
        if not task_data_raw:
            logger.warning(f"Задача {task_id} не найдена в Redis (возможно, уже выполнена)")
            return

        # Декодируем байтовые ключи/значения
        task_data = {}
        for k, v in task_data_raw.items():
            key = k.decode() if isinstance(k, bytes) else k
            value = v.decode() if isinstance(v, bytes) else v
            task_data[key] = value

        task_name = task_data.get("task_name")
        if not task_name:
            logger.error_message(f"Нет task_name в задаче {task_id}")
            return
        args = json.loads(task_data["args"])
        kwargs = json.loads(task_data["kwargs"])

        handler = TASK_HANDLERS.get(task_name)
        if not handler:
            logger.error_message(f"Неизвестная задача: {task_name}")
            return

        # Запускаем обработчик в фоне (чтобы не блокировать воркер)
        async def safe_executor():
            try:
                logger.info_message(f"▶ Старт задачи {task_id}: {task_name}, args={args}, kwargs={kwargs}")
                await handler(*args, **kwargs)
                logger.info_message(f"✔ Задача {task_id} ({task_name}) успешно завершена")
            except Exception as e:
                import traceback, sys
                err_msg = f"✖ Ошибка в задаче {task_id} ({task_name}): {e}\n{traceback.format_exc()}"
                logger.error_message(err_msg)
                # Дублируем в stderr для гарантированной видимости при любых настройках логирования
                print(err_msg, file=sys.stderr)

        asyncio.create_task(safe_executor())
        logger.info_message(f"Задача {task_id} ('{task_name}') запущена из Redis")

# ==================== ГЛОБАЛЬНЫЕ ФУНКЦИИ ДЛЯ ИМПОРТА ====================

async def init_global_scheduler():
    """
    Инициализация глобального планировщика
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        _scheduler_manager = AioSchedulerManager()
    
    return _scheduler_manager

def get_scheduler_manager():
    """
    Получить глобальный менеджер планировщика
    """
    global _scheduler_manager
    return _scheduler_manager

async def start_background_scheduler():
    """
    Запустить планировщик в фоне
    Возвращает задачу для возможности отмены
    """
    global _scheduler_manager
    
    logger = LogsMaker()
    logger.info_message("Запуск фонового планировщика задач (aioscheduler)...")
    
    try:
        # Инициализируем менеджер
        manager = await init_global_scheduler()
        
        # Запускаем планировщик
        scheduler_task = await manager.start()
        
        logger.info_message("✓ Планировщик aioscheduler запущен")
        
        return scheduler_task
        
    except Exception as e:
        logger.error_message(f"✗ Ошибка запуска планировщика: {e}")
        import traceback
        logger.error_message(traceback.format_exc())
        raise

async def stop_background_scheduler():
    """
    Остановить планировщик
    """
    global _scheduler_manager
    
    if _scheduler_manager:
        await _scheduler_manager.stop()

def get_scheduler_status() -> Dict[str, Any]:
    """
    Получить статус планировщика
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        return {
            "status": "not_initialized",
            "running": False,
            "jobs_count": 0,
            "jobs": []
        }
    
    return _scheduler_manager.get_status()

def add_scheduler_job(coro_func, interval_seconds: int = 300, job_name: str = None):
    """
    Добавить задачу в планировщик
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        raise RuntimeError("Планировщик не инициализирован")
    
    return _scheduler_manager.add_job(coro_func, interval_seconds, job_name)

def remove_scheduler_job(job_id: str) -> bool:
    """
    Удалить задачу из планировщика
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        return False
    
    if job_id not in _scheduler_manager.jobs:
        return False
    
    task = _scheduler_manager.jobs[job_id]
    
    try:
        if not task.done():
            task.cancel()
        del _scheduler_manager.jobs[job_id]
        return True
    except:
        return False
# ==================== ДЛЯ ИСПОЛЬЗОВАНИЯ В MAIN.PY ====================

def create_lifespan_context():
    """
    Создать контекст lifespan для FastAPI
    """
    scheduler_task = None
    
    @asynccontextmanager
    async def lifespan_context(app):
        nonlocal scheduler_task
        
        # Старт приложения
        logger = LogsMaker()
        logger.info_message("=" * 50)
        logger.info_message("Запуск приложения FastAPI")
        logger.info_message("=" * 50)
        
        # Запускаем планировщик в фоне
        try:
            scheduler_task = await start_background_scheduler()
            logger.info_message("✓ Фоновый планировщик запущен")
            
            # Проверяем статус
            status = get_scheduler_status()
            logger.info_message(f"Статус планировщика: {status['status']}")
            logger.info_message(f"Задач в планировщике: {status['jobs_count']}")
            
        except Exception as e:
            logger.fatal_message(f"✗ Ошибка запуска планировщика: {e}")
            import traceback
            logger.fatal_message(traceback.format_exc())
        
        yield
        
        # Остановка приложения
        logger.warning_message("=" * 50)
        logger.warning_message("Остановка приложения FastAPI")
        logger.warning_message("=" * 50)
        
        # Останавливаем планировщик
        await stop_background_scheduler()
        
        logger.warning_message("✓ Фоновый планировщик остановлен")
    
    return lifespan_context