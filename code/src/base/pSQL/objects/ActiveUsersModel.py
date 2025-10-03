from sqlalchemy.sql.expression import func, or_, and_

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

        # from .App import db
        # self.session = db

        from ..models.ActiveUsers import ActiveUsers
        self.ActiveUsers = ActiveUsers

        from ..models.Activities import Activities
        self.Activities = Activities

        from ..models.PeerHistory import PeerHistory
        self.PeerHistory = PeerHistory

        from ..models.Roots import Roots
        self.Roots = Roots

    def upload_past_table_ActiveUsers(self):
        from .App import get_db
        db_gen = get_db()
        database = next(db_gen)
        with open('./src/base/peer-data/active_users.json', mode='r', encoding='UTF-8') as f:
            cur_activities = json.load(f)
        for activity in cur_activities:
            existing_activity = database.query(self.ActiveUsers).filter(self.ActiveUsers.id == activity['id']).first()
            if existing_activity:
                continue
            else:
                new_activity = self.ActiveUsers(id=activity['id'], uuid_from=activity['uuid_from'], uuid_to=activity['uuid_to'], description=activity['description'], valid=activity['valid'], date_time=activity['date_time'], activities_id=activity['activities_id'])
                database.add(new_activity)
                database.commit()
        # database.close()
        return {"status": True}

    def actions(self, roots):
        from .App import get_db
        db_gen = get_db()
        database = next(db_gen)
        """выводит список доступных пользователю активностей"""
        month_ago = datetime.now() - timedelta(days=30)
        likes_count = database.query(self.ActiveUsers).filter(self.ActiveUsers.uuid_from == roots['user_id'], self.ActiveUsers.activities_id == 1, self.ActiveUsers.date_time >= month_ago).count()


        #проверить остаток доступных лайков
        likes_left = 10 - likes_count
        if likes_count > 10:
            likes_left = 0

        actions_for_all = database.query(self.Activities.id, self.Activities.name).filter(self.Activities.need_valid == True, self.Activities.active == True).all()
        if 'PeerCurator' in roots.keys() and len(roots['PeerCurator']) != 0:
            activities_list = []
            for activity_id in roots['PeerCurator']:
                activity_info = database.query(self.Activities.id, self.Activities.name).filter(self.Activities.id == activity_id, self.Activities.active == True).first()
                part = {"value": activity_info.id, "name": activity_info.name}
                activities_list.append(part)

            for activity in actions_for_all:
                part = {"value": activity.id, "name": activity.name, "likes_left": likes_left}
                activities_list.append(part)
            # сюда добавить обработку
            
            # database.close()
            return {
                "activities": activities_list
            }
        else:
            
            activities_list = [
                {"value": activity.id, "name": activity.name, "likes_left": likes_left}
                for activity in actions_for_all
            ]
            # database.close()
            return {
                "activities": activities_list
            }

    def history_mdr(self, activity_name):
        from .App import get_db
        db_gen = get_db()
        database = next(db_gen)
        result = []
        res = database.scalars(database.query(self.ActiveUsers).join(Activities, and_(self.ActiveUsers.activities_id == Activities.id, Activities.name == activity_name))).all()
        stat = {0 : "Не подтверждено", 1 : "Подтверждено", 2 : "Отказано"}
        if res:
            for re in res:
                info = re.__dict__
                stat['valid'] = info['valid']
                info['stat'] = stat
                info.pop('valid')
                result.append(info)
            database.close()
            return result
        # database.close()
        return res

    def sum(self, uuid):
        from .App import get_db
        db_gen = get_db()
        database = next(db_gen)
        user_info = database.query(self.Roots).filter(self.Roots.user_uuid == uuid).first()
        # user_info = database.query(self.Roots).filter(self.Roots.user_uuid == 2375).first()
        # database.close()
        if user_info:
            if user_info.user_points:
                points = user_info.user_points
                return points
        return 0
    
    def top(self):
        stmt = database.query(
            self.ActiveUsers.uuid_to,
            func.sum(self.Activities.coast)
        ).join(
            self.Activities,
            self.Activities.id == self.ActiveUsers.activities_id
        ).filter(self.ActiveUsers.valid == 1).group_by(
            self.ActiveUsers.uuid_to
        ).order_by(
            func.sum(self.Activities.coast).desc()
        ).limit(10)
        res = database.scalars(stmt).all()
        database.close()
        return res

    def my_place(self):
        results = database.query(
            self.ActiveUsers.uuid_to,
            func.sum(self.Activities.coast).label('total_coast')
        ).join(
            self.Activities,
            self.Activities.id == self.ActiveUsers.activities_id
        ).filter(
            self.ActiveUsers.valid == 1
        ).group_by(
            self.ActiveUsers.uuid_to
        ).order_by(
            func.coalesce(func.sum(self.Activities.coast), 0).desc()
        ).all()

        for rank, (uuid, coast) in enumerate(results, 1):
            if uuid == self.uuid_to:
                return rank
        database.close()
        return "Либо Вы вне всяких оценок, либо ВЫ ЕЩЁ СПИТЕ!"

    def statistics(self):
        results = database.query(
            self.Activities.id,
            self.Activities.name,
            func.coalesce(func.sum(self.Activities.coast), 0)
        ).join(
            self.ActiveUsers,
            self.ActiveUsers.activities_id == self.Activities.id
        ).filter(
            self.ActiveUsers.uuid_to == self.uuid_to,
            self.ActiveUsers.valid == 1
        ).group_by(
            self.Activities.name,
            self.Activities.id
        ).order_by(
            func.sum(self.Activities.coast).desc()
        ).all()
        database.close()
        return [
            {
                'activity_id': activity_id,
                'activity_name': activity_name,
                'total_coast': total_coast
            }
            for activity_id, activity_name, total_coast in results
        ]   

    def statistics_history(self):
        results = database.query(
            self.ActiveUsers.id,
            self.ActiveUsers.uuid_from,
            self.ActiveUsers.description,
            self.ActiveUsers.date_time,
            self.Activities.name,
            self.Activities.coast,
            self.Activities.id
        ).join(self.Activities).filter(
            self.ActiveUsers.uuid_to == self.uuid_to,
            self.ActiveUsers.valid == 1,
            self.Activities.id == self.activities_id
        ).all()

        processed_results = []
        for result in results:
            adjusted_time = result.date_time + timedelta(hours=4) if result.date_time else None
            processed_results.append({
                'id': result.id,
                'uuid_from': result.uuid_from,
                'description': result.description,
                'adjusted_time': adjusted_time,
                'activity_name': result.name,
                'coast': result.coast,
                'activity_id': result.id
            })
        database.close()
        return processed_results

    def new_a_week(self):
        week_start = func.date_trunc('week', func.now())
        results = database.query(
            self.ActiveUsers.id,
            self.ActiveUsers.uuid_from,
            self.ActiveUsers.description,
            self.ActiveUsers.date_time,
            self.Activities.name,
            self.Activities.coast,
            self.Activities.id,
            func.sum(self.Activities.coast).over().label('total_sum')
        ).join(self.Activities).filter(
            self.ActiveUsers.uuid_to == self.uuid_to,
            func.date_trunc('week', self.ActiveUsers.date_time) == week_start,
            self.ActiveUsers.valid == 1
        ).all()

        activities = []
        for result in results:
            activities.append({
                "id_activeusers": result.id,
                "uuid": result.uuid_from,
                "description": result.description,
                "date_time": result.date_time,
                "activity_name": result.name,
                "cost": result.coast,
                "id_activites": result.id
            })
        total_sum = results[0].total_sum if results else 0
        database.close()
        return {"sum": total_sum, "activities": activities}

    def user_history(self):
        # results = database.query(
        #     self.ActiveUsers.id,
        #     self.ActiveUsers.uuid_from,
        #     self.ActiveUsers.description,
        #     self.ActiveUsers.date_time,
        #     self.Activities.name,
        #     self.Activities.coast,
        #     self.Activities.id,
        # ).join(self.Activities).filter(
        #     self.ActiveUsers.uuid_to == self.uuid_to,
        #     self.ActiveUsers.valid == 1
        # ).all()
        from ..models.User import User

        from .App import get_db
        db_gen = get_db()
        database = next(db_gen)
        results = database.query(
            self.ActiveUsers.id,
            self.ActiveUsers.uuid_from,
            self.ActiveUsers.description,
            self.ActiveUsers.date_time,
            self.Activities.name,
            self.Activities.coast,
            self.Activities.id,
        ).join(self.Activities).filter(
            self.ActiveUsers.uuid_to == self.uuid_to,
            self.ActiveUsers.valid == 1
        ).all()
        # database.close()
        activities = []
        
        for result in results:
            user_info = database.query(User.name, User.second_name, User.last_name).filter(User.id == result.uuid_from).first()
            user_fio = user_info.last_name + " " + user_info.name + " " + user_info.second_name
            activities.append({
                # "id_activeusers": result.id,
                "id_activeusers": result[0],
                "uuid_from": result.uuid_from,
                "fio_from": user_fio,
                "description": result.description,
                "date_time": result.date_time,
                "activity_name": result.name,
                "cost": result.coast,
                # "id_activites": result.id
                "id_activites": result[-1]
            })

        merch_history = database.query(self.PeerHistory).filter(self.PeerHistory.user_uuid == self.uuid_to, self.PeerHistory.info_type == 'merch').all()
        for merch in merch_history:
            activities.append({
                "id": merch.id,
                "merch_info": merch.merch_info,
                "date_time": merch.date_time,
                "merch_coast": merch.merch_coast
            })
        
        return activities
