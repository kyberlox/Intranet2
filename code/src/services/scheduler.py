import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from contextlib import asynccontextmanager
from sqlalchemy.future import select
from sqlalchemy import extract

# Импорт aioscheduler
from aioscheduler import TimedScheduler

from .LogsMaker import LogsMaker
from ..base.pSQL.objects.App import get_async_db, AsyncSessionLocal
from ..model.User import User
from .MerchStore import MerchStore
from .Peer import Peer

# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================

# Глобальный экземпляр планировщика
_scheduler = None
_scheduler_task = None
_scheduler_manager = None

# ==================== РЕАЛИЗАЦИЯ ЗАПРОСОВ ====================

async def get_today_birthdays() -> List[int]:
    """
    Найти всех пользователей, у которых сегодня день рождения
    Возвращает список ID пользователей
    """
    async with AsyncSessionLocal() as db:
        today = datetime.now()
        
        query = select(User.id).where(
            (extract('month', User.birth_date) == today.month) &
            (extract('day', User.birth_date) == today.day) &
            (User.is_active == True)
        )
        
        result = await db.execute(query)
        birthdays = result.scalars().all()
        
        LogsMaker().info_message(f"Найдено пользователей с днём рождения: {len(birthdays)}")
        return birthdays

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
    if not user_ids:
        return
    
    logger = LogsMaker()
    logger.info_message(f"Отправка поздравлений с ДР для {len(user_ids)} пользователей")
    
    try:
        async with AsyncSessionLocal() as db:
            for user_id in user_ids:
                send_data = {
                    "uuid_from": 4133,  # В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
                    "uuid_to": int(user_id),
                    "activities_id": 7,  # В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
                    "description": f"Поздравительные баллы. С днем рождения!"
                }
                send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)
            
            await db.commit()
            logger.info_message("Уведомления о днях рождения успешно отправлены")
    
    except Exception as e:
        logger.error_message(f"Ошибка при отправке уведомлений о днях рождения: {e}")
        # Откатываем изменения в случае ошибки
        if 'db' in locals():
            await db.rollback()

async def send_anniversary_notifications(anniversary_users: List[Dict[str, Any]]):
    """
    Отправка поздравлений с юбилеями регистрации
    """
    if not anniversary_users:
        return
    
    logger = LogsMaker()
    logger.info_message(f"Отправка поздравлений с юбилеем для {len(anniversary_users)} пользователей")
    
    try:
        async with AsyncSessionLocal() as db:
            for user in anniversary_users:
                send_data = {
                    "uuid_from": 4133,  # Административный аккаунт
                    "uuid_to": int(user['id']),
                    "activities_id": 8,  # ID активности для юбилея
                    "description": f"Поздравляем с {user['years']}-летием регистрации!"
                }
                send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)
            
            await db.commit()
            logger.info_message("Уведомления о юбилеях успешно отправлены")
    
    except Exception as e:
        logger.error_message(f"Ошибка при отправке уведомлений о юбилеях: {e}")
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
        
        # 2. Юбилеи регистрации
        # anniversary_users = await get_registration_anniversaries()
        # await send_anniversary_notifications(anniversary_users)
        
        # 3. Неактивные пользователи
        # inactive_users = await check_inactive_users()
        # await handle_inactive_users(inactive_users)
        
        # 4. Триал (опционально)
        # expiring_trials = await check_trial_expiring()
        # await handle_expiring_trials(expiring_trials)
        
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
    
    def schedule_daily_check(self, interval_seconds: int = 300):
        """
        Запланировать ежедневную проверку
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        # Создаем задачу
        task = self.scheduler.schedule(daily_check(), interval_seconds)
        
        # Сохраняем задачу
        job_id = f"daily_check_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Ежедневная проверка запланирована каждые {interval_seconds} секунд, ID: {job_id}")
        
        return job_id
    
    def schedule_test_task(self, interval_seconds: int = 60):
        """
        Запланировать тестовую задачу
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        task = self.scheduler.schedule(test_task(), interval_seconds)
        
        job_id = f"test_task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Тестовая задача запланирована каждые {interval_seconds} секунд, ID: {job_id}")
        
        return job_id
    
    def schedule_custom_task(self, coro_func, interval_seconds: int, job_name: str = None):
        """
        Запланировать пользовательскую задачу
        """
        if not self.scheduler:
            raise RuntimeError("Планировщик не инициализирован")
        
        # Создаем корутину из функции
        coro = coro_func()
        
        # Планируем задачу
        task = self.scheduler.schedule(coro, interval_seconds)
        
        # Генерируем ID
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if job_name:
            job_id = f"{job_name}_{timestamp}"
        else:
            job_id = f"task_{coro_func.__name__}_{timestamp}"
        
        self.jobs[job_id] = task
        
        logger = LogsMaker()
        logger.info_message(f"Задача '{job_id}' запланирована каждые {interval_seconds} секунд")
        
        return job_id
    
    def remove_job(self, job_id: str) -> bool:
        """
        Удалить задачу из планировщика
        """
        if job_id not in self.jobs:
            return False
        
        task = self.jobs[job_id]
        
        # Пытаемся отменить задачу
        try:
            task.cancel()
            del self.jobs[job_id]
            
            logger = LogsMaker()
            logger.info_message(f"Задача '{job_id}' удалена")
            return True
            
        except Exception as e:
            logger.error_message(f"Ошибка при удалении задачи '{job_id}': {e}")
            return False
    
    async def scheduler_worker(self):
        """
        Основной рабочий процесс планировщика
        """
        logger = LogsMaker()
        
        try:
            # Инициализируем планировщик
            await self.init_scheduler()
            
            # Запускаем планировщик
            self.scheduler.start()
            self.is_running = True
            
            logger.info_message("Планировщик aioscheduler запущен")
            
            # Добавляем задачи по умолчанию
            
            # 1. Ежедневная проверка каждые 5 минут (300 секунд)
            daily_job_id = self.schedule_daily_check(interval_seconds=300)
            
            # 2. Тестовая задача каждую минуту (60 секунд)
            # test_job_id = self.schedule_test_task(interval_seconds=60)
            
            logger.info_message(f"Задач в планировщике: {len(self.jobs)}")
            
            # Бесконечный цикл для поддержания работы
            while self.is_running:
                await asyncio.sleep(60)  # Проверяем каждую минуту
                
                # Можно добавить периодическую проверку состояния
                if datetime.now().minute == 0:  # Каждый час
                    logger.debug_message("Планировщик работает, активных задач: {}".format(
                        len([t for t in self.jobs.values() if not t.done()])
                    ))
        
        except asyncio.CancelledError:
            logger.info_message("Планировщик остановлен по запросу")
        
        except Exception as e:
            logger.error_message(f"Критическая ошибка в планировщике: {e}")
            import traceback
            logger.error_message(traceback.format_exc())
        
        finally:
            self.is_running = False
            if self.scheduler:
                self.scheduler.shutdown()
    
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
                    task.cancel()
                except:
                    pass
            
            self.jobs.clear()
            
            # Останавливаем планировщик
            if self.scheduler:
                self.scheduler.shutdown()
            
            # Отменяем задачу планировщика
            if self.scheduler_task and not self.scheduler_task.done():
                self.scheduler_task.cancel()
                try:
                    await self.scheduler_task
                except asyncio.CancelledError:
                    pass
            
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
                "cancelled": task.cancelled()
            })
        
        return {
            "status": "running" if self.is_running else "stopped",
            "running": self.is_running,
            "jobs_count": len(self.jobs),
            "active_jobs": len([t for t in self.jobs.values() if not t.done()]),
            "jobs": jobs_info
        }

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

def add_scheduler_job(coro_func, interval_seconds: int, job_name: str = None):
    """
    Добавить задачу в планировщик
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        raise RuntimeError("Планировщик не инициализирован")
    
    return _scheduler_manager.schedule_custom_task(coro_func, interval_seconds, job_name)

def remove_scheduler_job(job_id: str) -> bool:
    """
    Удалить задачу из планировщика
    """
    global _scheduler_manager
    
    if _scheduler_manager is None:
        return False
    
    return _scheduler_manager.remove_job(job_id)

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