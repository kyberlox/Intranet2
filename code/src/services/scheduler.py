import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any

import aioschedule as schedule

from .LogsMaker import LogsMaker
from ..base.pSQL.objects.App import get_async_db
from ..model.User import User
from .MerchStore import MerchStore
from .Peer import Peer

logger = logging.getLogger(__name__)

# ==================== РЕАЛИЗАЦИЯ ЗАПРОСОВ ====================

async def get_today_birthdays() -> List[int]:
    """
    Найти всех пользователей, у которых сегодня день рождения
    Возвращает список ID пользователей
    """
    async with SessionLocal() as db:
        today = datetime.now()
        
        query = select(User.id).where(
            (extract('month', User.birth_date) == today.month) &
            (extract('day', User.birth_date) == today.day) &
            (User.is_active == True)
        )
        
        result = await db.execute(query)
        birthdays = result.scalars().all()
        
        logger.info(f"Найдено пользователей с днём рождения: {len(birthdays)}")
        return birthdays

async def get_registration_anniversaries() -> List[Dict[str, Any]]:
    """
    Найти юбилеи регистрации (5, 10, 15, 20, 25, 30 лет)
    Возвращает список словарей с информацией
    """
    async with SessionLocal() as db:
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
        
        logger.info(f"Найдено юбилеев регистрации: {len(anniversary_users)}")
        return anniversary_users

async def check_inactive_users() -> List[int]:
    """
    Проверка пользователей, которые не заходили больше 30 дней
    """
    async with SessionLocal() as db:
        month_ago = datetime.now() - timedelta(days=30)
        
        query = select(User.id).where(
            (User.last_login < month_ago) &
            (User.is_active == True)
        )
        
        result = await db.execute(query)
        inactive_users = result.scalars().all()
        
        logger.info(f"Найдено неактивных пользователей: {len(inactive_users)}")
        return inactive_users

async def check_trial_expiring() -> List[int]:
    """
    Проверка пользователей, у которых скоро закончится триал
    (если у вас есть такая функциональность)
    """
    async with SessionLocal() as db:
        three_days_later = datetime.now() + timedelta(days=3)
        
        query = select(User.id).where(
            (User.trial_ends_at <= three_days_later) &
            (User.trial_ends_at >= datetime.now()) &
            (User.is_active == True) &
            (User.subscription_status == 'trial')
        )
        
        result = await db.execute(query)
        expiring_users = result.scalars().all()
        
        logger.info(f"Найдено пользователей с истекающим триалом: {len(expiring_users)}")
        return expiring_users



# ==================== ФУНКЦИИ ОБРАБОТКИ ====================

async def send_birthday_notifications(user_ids: List[int]):
    """
    Отправка уведомлений о днях рождения
    """
    if not user_ids:
        return
    
    logger.info(f"Отправка поздравлений с ДР для {len(user_ids)} пользователей")
    
    # Пример: логика отправки
    # for user_id in user_ids[:5]:  # Для примера покажем только первые 5
    #     logger.info(f"  - Пользователь {user_id}: С Днём рождения!")
    async with SessionLocal() as db:
        for user_id in user_ids:
            send_data = {
                "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
                "uuid_to": int(user_id),
                "activities_id": 7, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
                "description": f"Поздравительные баллы. С днем рождения!"
            }
            send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=db)
        await db.commit()
    # Здесь можно добавить:
    # 1. Отправку email через ваш email-сервис
    # 2. Webhook на внешний сервис
    # 3. Запись в очередь на отправку push-уведомлений
    # 4. Запись в таблицу уведомлений для отправки через веб-сокеты

async def send_anniversary_notifications(anniversary_users: List[Dict[str, Any]]):
    """
    Отправка поздравлений с юбилеями регистрации
    """
    if not anniversary_users:
        return
    
    logger.info(f"Отправка поздравлений с юбилеем для {len(anniversary_users)} пользователей")
    
    for user in anniversary_users:
        logger.info(f"  - {user['username']} ({user['email']}): "
                   f"Поздравляем с {user['years']}-летием регистрации!")
        
        # Пример отправки email
        # await send_email(
        #     to=user['email'],
        #     subject=f"Поздравляем с {user['years']}-летием!",
        #     template="anniversary.html",
        #     context=user
        # )

async def handle_inactive_users(user_ids: List[int]):
    """
    Обработка неактивных пользователей
    """
    if not user_ids:
        return
    
    logger.info(f"Обработка {len(user_ids)} неактивных пользователей")
    
    # Здесь можно:
    # 1. Отправить email с напоминанием
    # 2. Изменить статус пользователя
    # 3. Записать в аналитику

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
        
        # 5. Другие ваши проверки...
        # await other_checks()
        
        logger.info_message(f"ЗАВЕРШЕНИЕ ЕЖЕДНЕВНОЙ ПРОВЕРКИ - УСПЕХ")
        
    except Exception as e:
        logger.error_message(f"ОШИБКА в ежедневной проверке: {e}")
        # Здесь можно добавить отправку уведомления об ошибке администратору
        
    logger.info_message("=" * 50)

# ==================== ПЛАНИРОВЩИК ====================

async def scheduler_worker():
    """
    Рабочий процесс планировщика
    """
    # Настраиваем расписание
    
    # Основная задача каждый день в 02:00
    # schedule.every().day.at("02:00").do(daily_check)
    
    # Для тестирования - раскомментировать:
    schedule.every(5).minutes.do(daily_check)  # Каждые 5 минут
    # schedule.every().minute.do(daily_check)    # Каждую минуту
    
    logger = LogsMaker()
    logger.info_message("Планировщик инициализирован. Задачи:")
    for job in schedule.jobs:
        logger.info_message(f"  • {job}")
    
    # Бесконечный цикл проверки
    while True:
        try:
            await schedule.run_pending()
            await asyncio.sleep(60)  # Проверяем каждую минуту
            
        except Exception as e:
            logger.error_message(f"Ошибка в планировщике: {e}")
            await asyncio.sleep(60)  # Ждём минуту при ошибке

async def start_background_scheduler():
    """
    Запустить планировщик в фоне
    Возвращает задачу для возможности отмены
    """
    logger = LogsMaker()
    logger.debug("Запуск фонового планировщика задач...")
    
    # Создаём и запускаем задачу планировщика
    scheduler_task = asyncio.create_task(scheduler_worker())

    return scheduler_task