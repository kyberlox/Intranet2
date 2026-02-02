from sqlalchemy.sql.expression import func, or_, and_


from .App import select, func


import json

from datetime import datetime, timedelta



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Истории Активностей Пользователей")


class ActiveUsersModel:
    def __init__(self, id: int = 0, description: str = '', valid: int = 0, uuid_from: int = 0, uuid_to: int = 0, activities_id: int = 0):
        self.id = id
        self.description = description
        self.valid = valid
        self.uuid_from = uuid_from
        self.uuid_to = uuid_to
        self.activities_id = activities_id


        from ..models.ActiveUsers import ActiveUsers
        self.ActiveUsers = ActiveUsers

        from ..models.Activities import Activities
        self.Activities = Activities

        from ..models.PeerHistory import PeerHistory
        self.PeerHistory = PeerHistory

        from ..models.Roots import Roots
        self.Roots = Roots

        from ..models.User import User
        self.User = User

    async def upload_past_table_ActiveUsers(self, session):
        try:
            with open('./src/base/peer-data/active_users.json', mode='r', encoding='UTF-8') as f:
                cur_activities = json.load(f)
            
            for activity in cur_activities:
                stmt = select(self.ActiveUsers).where(self.ActiveUsers.id == activity['id'])
                result = await session.execute(stmt)
                existing_activity = result.scalar_one_or_none()
                
                if existing_activity:
                    continue
                else:
                    new_activity = self.ActiveUsers(
                        id=activity['id'], 
                        uuid_from=activity['uuid_from'], 
                        uuid_to=activity['uuid_to'], 
                        description=activity['description'], 
                        valid=activity['valid'], 
                        date_time=activity['date_time'], 
                        activities_id=activity['activities_id']
                    )
                    session.add(new_activity)
            
            await session.commit()
            return {"status": True}
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в upload_past_table_ActiveUsers при загрузке исторических данных ActiveUsers: {e}")

    async def actions(self, session, roots):
        """выводит список доступных пользователю активностей"""
        try:
            month_ago = datetime.now() - timedelta(days=30)
            activities_list = []
            
            # Активности для всех
            stmt_all = select(self.Activities.id, self.Activities.name).where(
                self.Activities.need_valid == True, 
                self.Activities.active == True
            )
            result_all = await session.execute(stmt_all)
            actions_for_all = result_all.all()

            if 'PeerCurator' in roots.keys() and len(roots['PeerCurator']) != 0:
                for activity_id in roots['PeerCurator']:
                    stmt_activity = select(self.Activities.id, self.Activities.name).where(
                        self.Activities.id == activity_id, 
                        self.Activities.active == True
                    )
                    result_activity = await session.execute(stmt_activity)
                    activity_info = result_activity.first()
                    
                    if activity_info:
                        part = {"value": activity_info.id, "name": activity_info.name}
                        activities_list.append(part)
                
                # return {"activities": activities_list}
            
            # Для обычных пользователей
            for activity in actions_for_all:
                stmt_count = select(func.count(self.ActiveUsers.id)).where(
                    self.ActiveUsers.uuid_from == roots['user_id'],
                    self.ActiveUsers.activities_id == activity.id,
                    self.ActiveUsers.date_time >= month_ago
                )
                result_count = await session.execute(stmt_count)
                likes_count = result_count.scalar()

                likes_left = 5 - likes_count
                if likes_count > 5:
                    likes_left = 0
                    
                action = {"value": activity.id, "name": activity.name, "likes_left": likes_left}
                activities_list.append(action)
                
            return {"activities": activities_list}
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в actions при получении списка активностей для пользователя {roots.get('user_id', 'unknown')}: {e}")

    async def history_mdr(self, session, activity_name: str):
        try:
            result = []
            stmt = select(self.ActiveUsers).join(
                self.Activities, 
                and_(
                    self.ActiveUsers.activities_id == self.Activities.id, 
                    self.Activities.name == activity_name
                )
            )
            query_result = await session.execute(stmt)
            res = query_result.scalars().all()
            
            stat = {0: "Не подтверждено", 1: "Подтверждено", 2: "Отказано"}
            
            if res:
                for re in res:
                    info = re.__dict__
                    info['stat'] = stat[info['valid']]
                    info.pop('_sa_instance_state', None)
                    result.append(info)
                return result
                
            return []
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в history_mdr при получении истории для активности '{activity_name}': {e}")

    async def sum(self, session, uuid: int):
        try:
            stmt = select(self.Roots).where(self.Roots.user_uuid == uuid)
            result = await session.execute(stmt)
            user_info = result.scalar_one_or_none()
            
            if user_info and user_info.user_points:
                return user_info.user_points
            return 0
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в sum при получении суммы очков для пользователя {uuid}: {e}")

    async def top(self, session):
        try:
            stmt = select(
                self.ActiveUsers.uuid_to,
                func.sum(self.Activities.coast).label('total_coast')
            ).join(
                self.Activities,
                self.Activities.id == self.ActiveUsers.activities_id
            ).where(
                self.ActiveUsers.valid == 1
            ).group_by(
                self.ActiveUsers.uuid_to
            ).order_by(
                func.sum(self.Activities.coast).desc()
            ).limit(10)
            
            result = await session.execute(stmt)
            return result.all()
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в top при получении топа пользователей: {e}")

    async def my_place(self, session):
        try:
            stmt = select(
                self.ActiveUsers.uuid_to,
                func.sum(self.Activities.coast).label('total_coast')
            ).join(
                self.Activities,
                self.Activities.id == self.ActiveUsers.activities_id
            ).where(
                self.ActiveUsers.valid == 1
            ).group_by(
                self.ActiveUsers.uuid_to
            ).order_by(
                func.coalesce(func.sum(self.Activities.coast), 0).desc()
            )
            
            result = await session.execute(stmt)
            results = result.all()
            
            for rank, (uuid, coast) in enumerate(results, 1):
                if uuid == self.uuid_to:
                    return rank
                    
            return "Либо Вы вне всяких оценок, либо ВЫ ЕЩЁ СПИТЕ!"
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в my_place при определении места пользователя {self.uuid_to}: {e}")

    async def statistics(self, session):
        try:
            stmt = select(
                self.Activities.id,
                self.Activities.name,
                func.coalesce(func.sum(self.Activities.coast), 0).label('total_coast')
            ).join(
                self.ActiveUsers,
                self.ActiveUsers.activities_id == self.Activities.id
            ).where(
                self.ActiveUsers.uuid_to == self.uuid_to,
                self.ActiveUsers.valid == 1
            ).group_by(
                self.Activities.name,
                self.Activities.id
            ).order_by(
                func.sum(self.Activities.coast).desc()
            )
            
            result = await session.execute(stmt)
            results = result.all()
            
            return [
                {
                    'activity_id': activity_id,
                    'activity_name': activity_name,
                    'total_coast': total_coast
                }
                for activity_id, activity_name, total_coast in results
            ]
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в statistics при получении статистики для пользователя {self.uuid_to}: {e}")

    async def statistics_history(self, session):
        try:
            stmt = select(
                self.ActiveUsers.id,
                self.ActiveUsers.uuid_from,
                self.ActiveUsers.description,
                self.ActiveUsers.date_time,
                self.Activities.name,
                self.Activities.coast,
                self.Activities.id
            ).join(self.Activities).where(
                self.ActiveUsers.uuid_to == self.uuid_to,
                self.ActiveUsers.valid == 1,
                self.Activities.id == self.activities_id
            )
            
            result = await session.execute(stmt)
            results = result.all()

            processed_results = []
            for row in results:
                adjusted_time = row.date_time + timedelta(hours=4) if row.date_time else None
                processed_results.append({
                    'id': row.id,
                    'uuid_from': row.uuid_from,
                    'description': row.description,
                    'adjusted_time': adjusted_time,
                    'activity_name': row.name,
                    'coast': row.coast,
                    'activity_id': row.id
                })
                
            return processed_results
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в statistics_history при получении истории статистики для пользователя {self.uuid_to} и активности {self.activities_id}: {e}")

    async def new_a_week(self, session):
        try:
            week_start = func.date_trunc('week', func.now())
            stmt = select(
                self.ActiveUsers.id,
                self.ActiveUsers.uuid_from,
                self.ActiveUsers.description,
                self.ActiveUsers.date_time,
                self.Activities.name,
                self.Activities.coast,
                self.Activities.id,
                func.sum(self.Activities.coast).over().label('total_sum')
            ).join(self.Activities).where(
                self.ActiveUsers.uuid_to == self.uuid_to,
                func.date_trunc('week', self.ActiveUsers.date_time) == week_start,
                self.ActiveUsers.valid == 1
            )
            
            result = await session.execute(stmt)
            results = result.all()

            activities = []
            for row in results:
                activities.append({
                    "id_activeusers": row.id,
                    "uuid": row.uuid_from,
                    "description": row.description,
                    "date_time": row.date_time,
                    "activity_name": row.name,
                    "cost": row.coast,
                    "id_activites": row.id
                })
                
            total_sum = results[0].total_sum if results else 0
            return {"sum": total_sum, "activities": activities}
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в new_a_week при получении недельной статистики для пользователя {self.uuid_to}: {e}")

    async def user_history(self, session):
        YEARS_ID = [21, 22, 23, 24, 25, 26, 27] # менять значеняи к годам если поменялись айдишники
        try:
            # Получаем активность пользователя
            stmt_activities = select(
                self.ActiveUsers.id,
                self.ActiveUsers.uuid_from,
                self.ActiveUsers.description,
                self.ActiveUsers.date_time,
                self.Activities.name,
                self.Activities.coast,
                self.Activities.id,
            ).join(self.Activities).where(
                self.ActiveUsers.uuid_to == self.uuid_to,
                self.ActiveUsers.valid == 1
            )
            
            result_activities = await session.execute(stmt_activities)
            results = result_activities.all()
            
            activities = []
            if results:
                for row in results:
                    # Получаем информацию о пользователе
                    stmt_user = select(
                        self.User.name, 
                        self.User.second_name, 
                        self.User.last_name
                    ).where(self.User.id == row.uuid_from)
                    
                    result_user = await session.execute(stmt_user)
                    user_info = result_user.first()
                    
                    user_fio = ""
                    if user_info:
                        user_fio = f"{user_info.last_name or ''} {user_info.name or ''} {user_info.second_name or ''}".strip()
                    
                    activity_name = row.name
                    description = row.description

                    if row[-1] == 7:
                        description = f"Лучший сотрудник {row.description} года"
                    elif row[-1] == 18:
                        description = f"Почетная грамота в конкурсе 'Лучший сотрудник {row.description} года'"
                    elif row[-1] in YEARS_ID:
                        activity_name = f"Награда за юбилей {row.name}"
                    elif row[-1] == 16:
                        activity_name = f"Баллы за идею"
                        description = f"Идея №{row.description}"

                        
                    activities.append({
                        "id_activeusers": row.id,
                        "uuid_from": row.uuid_from,
                        "fio_from": user_fio,
                        "description": description,
                        "date_time": row.date_time,
                        "activity_name": activity_name,
                        "cost": row.coast,
                        "id_activites": row[-1]
                    })
            
            # Получаем историю мерча
            stmt_merch = select(self.PeerHistory).where(
                self.PeerHistory.user_uuid == self.uuid_to,
                self.PeerHistory.info_type == 'merch'
            )
            result_merch = await session.execute(stmt_merch)
            merch_history = result_merch.scalars().all()
            if not merch_history:
                sorted_result = sorted(activities, key=lambda x: x['date_time'], reverse=True)
                return sorted_result
            for merch in merch_history:
                activities.append({
                    "id": merch.id,
                    "user_uuid": merch.user_uuid,
                    "fio_from": "Магазин мерча",
                    "description": merch.merch_info,
                    "date_time": merch.date_time,
                    "activity_name": "Снятие баллов за покупку",
                    "cost": -merch.merch_coast
                })
            sorted_result = sorted(activities, key=lambda x: x['date_time'], reverse=True)
            return sorted_result
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в user_history при получении полной истории для пользователя {self.uuid_to}: {e}")
