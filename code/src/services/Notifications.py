"""
Модуль уведомлений.
Изолирован от Peer/User/scheduler, чтобы не было циклических импортов.
"""

import uuid as _uuid
from datetime import datetime
from typing import Optional

from .LogsMaker import LogsMaker


# Маппинг activities_id → (type, title, text)
# Опирается на РЕАЛЬНЫЙ код, а не на base_activities.json
PEER_ACTIVITY_NOTIFICATION = {
    1:  ("birthday",          "С днём рождения!",   "Вам начислены поздравительные баллы."),
    2:  ("best_employee",     "Сотрудник года",      "Вам начислены баллы как сотруднику года."),
    3:  ("new_user",          "Добро пожаловать!",   "Вам начислены приветственные баллы."),
    4:  ("idea",              "Идея принята",        "Вам начислены баллы за предложенную идею."),
    5:  ("news",              "Спасибо за новость",  "Вам начислены баллы за предложенную новость."),
    6:  ("honorary_diploma",  "Почётная грамота",    "Вам начислены баллы за почётную грамоту."),
    7:  ("anniversary",       "С годовщиной!",       "Вам начислены баллы за год работы в компании."),
    8:  ("anniversary",       "5 лет вместе!",       "Вам начислены баллы за 5 лет в компании."),
    9:  ("anniversary",       "10 лет вместе!",      "Вам начислены баллы за 10 лет в компании."),
    11: ("anniversary",       "15 лет вместе!",      "Вам начислены баллы за 15 лет в компании."),
    12: ("anniversary",       "20 лет вместе!",      "Вам начислены баллы за 20 лет в компании."),
    13: ("anniversary",       "25 лет вместе!",      "Вам начислены баллы за 25 лет в компании."),
    14: ("anniversary",       "30 лет вместе!",      "Вам начислены баллы за 30 лет в компании."),
    15: ("anniversary",       "35 лет вместе!",      "Вам начислены баллы за 35 лет в компании."),
    17: ("achievement",       "Новое достижение!",   "Вам начислены баллы за достижение."),
}


async def send_user_notification(
    user_id: int,
    type_: str,
    title: str,
    text: str,
    payload: Optional[dict] = None,
    session=None,
) -> bool:
    """
    Универсальная отправка уведомления.
    session задан → только flush, коммит на вызывающей стороне.
    session=None → открывает свою сессию и коммитит сама.
    """
    from ..base.pSQL.objects.UserModel import UserModel

    notif = {
        "id": str(_uuid.uuid4()),
        "type": type_,
        "title": title,
        "text": text,
        "created_at": datetime.now().isoformat(),
        "read_at": None,
        "payload": payload or {},
    }
    try:
        if session is not None:
            return await UserModel().add_notification(
                user_id=int(user_id), notification=notif, session=session
            )
        from ..base.pSQL.objects.App import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            ok = await UserModel().add_notification(
                user_id=int(user_id), notification=notif, session=db
            )
            await db.commit()
            return ok
    except Exception as e:
        LogsMaker().error_message(
            f"send_user_notification error (user={user_id}, type={type_}): {e}"
        )
        return False


async def notify_about_points(
    user_id: int,
    activity_id,
    description: str = "",
    points=None,
    session=None,
) -> bool:
    """
    Обёртка для автоначислений из PeerUserModel.send_auto_points / send_points.
    """
    try:
        key = int(activity_id) if activity_id is not None else 0
    except (TypeError, ValueError):
        key = 0

    type_, title, text = PEER_ACTIVITY_NOTIFICATION.get(
        key,
        ("points_transfer", "Начислены баллы", description or "Вам начислены баллы."),
    )
    return await send_user_notification(
        user_id=user_id,
        type_=type_,
        title=title,
        text=text,
        payload={"activity_id": activity_id, "description": description, "points": points},
        session=session,
    )
