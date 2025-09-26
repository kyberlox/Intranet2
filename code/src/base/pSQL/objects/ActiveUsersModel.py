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

        from .App import db
        self.session = db

        from ..models.ActiveUsers import ActiveUsers
        self.ActiveUsers = ActiveUsers

        from ..models.Activities import Activities
        self.Activities = Activities

        from ..models.PeerHistory import PeerHistory
        self.PeerHistory = PeerHistory

        from ..models.Roots import Roots
        self.Roots = Roots

    def upload_past_table_ActiveUsers(self):
        with open('./src/base/peer-data/active_users.json', mode='r', encoding='UTF-8') as f:
            cur_activities = json.load(f)
        for activity in cur_activities:
            existing_activity = self.session.query(self.ActiveUsers).filter(self.ActiveUsers.id == activity['id']).first()
            if existing_activity:
                continue
            else:
                new_activity = self.ActiveUsers(id=activity['id'], uuid_from=activity['uuid_from'], uuid_to=activity['uuid_to'], description=activity['description'], valid=activity['valid'], date_time=activity['date_time'], activities_id=activity['activities_id'])
                self.session.add(new_activity)
                self.session.commit()
        self.session.close()
        return {"status": True}

    def actions(self, roots):
        """выводит список доступных пользователю активностей"""
        month_ago = datetime.now() - timedelta(days=30)
        likes_count = self.session.query(self.ActiveUsers).filter(self.ActiveUsers.uuid_from == roots['user_id'], self.ActiveUsers.activities_id == 0, self.ActiveUsers.date_time >= month_ago).count()


        #проверить остаток доступных лайков
        likes_left = 10 - likes_count
        if likes_count > 10:
            likes_left = 0

        actions_for_all = self.session.query(self.Activities.id, self.Activities.name).filter(self.Activities.need_valid == True).all()
        if 'PeerCurator' in roots.keys() and len(roots['PeerCurator']) != 0:
            activities_list = []
            for activity_id in roots['PeerCurator']:
                activity_info = self.session.query(self.Activities.id, self.Activities.name).filter(self.Activities.id == activity_id).first()
                part = {"value": activity_info.id, "name": activity_info.name}
                activities_list.append(part)

            for activity in actions_for_all:
                part = {"value": activity.id, "name": activity.name}
                activities_list.append(part)
            # сюда добавить обработку
            
            self.session.close()
            return {
                "likes_left": likes_left,
                "activities": activities_list
            }
        else:
            
            activities_list = [
                {"value": activity.id, "name": activity.name}
                for activity in actions_for_all
            ]
            self.session.close()
            return {
                "likes_left": likes_left,
                "activities": activities_list
            }

    def history_mdr(self, activity_name):
        result = []
        res = self.session.scalars(self.session.query(self.ActiveUsers).join(Activities, and_(self.ActiveUsers.activities_id == Activities.id, Activities.name == activity_name))).all()
        stat = {0 : "Не подтверждено", 1 : "Подтверждено", 2 : "Отказано"}
        if res:
            for re in res:
                info = re.__dict__
                stat['valid'] = info['valid']
                info['stat'] = stat
                info.pop('valid')
                result.append(info)
            self.session.close()
            return result
        self.session.close()
        return res

    def sum(self, uuid):
        user_info = self.session.query(self.Roots).filter(self.Roots.user_uuid == uuid).first()
        if user_info:
            if user_info.user_points:
                return user_info.user_points
        return 0
    
    def top(self):
        stmt = self.session.query(
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
        res = self.session.scalars(stmt).all()
        self.session.close()
        return res

    def my_place(self):
        results = self.session.query(
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
        self.session.close()
        return "Либо Вы вне всяких оценок, либо ВЫ ЕЩЁ СПИТЕ!"

    def statistics(self):
        results = self.session.query(
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
        self.session.close()
        return [
            {
                'activity_id': activity_id,
                'activity_name': activity_name,
                'total_coast': total_coast
            }
            for activity_id, activity_name, total_coast in results
        ]   

    def statistics_history(self):
        results = self.session.query(
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
        self.session.close()
        return processed_results

    def new_a_week(self):
        week_start = func.date_trunc('week', func.now())
        results = self.session.query(
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
        self.session.close()
        return {"sum": total_sum, "activities": activities}

    def user_history(self):
        results = self.session.query(
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

        merch_history = self.session.query(self.PeerHistory).filter(self.PeerHistory.user_uuid == self.uuid_to, self.PeerHistory.info_type == 'merch').all()
        for merch in merch_history:
            activities.append({
                "id": merch.id,
                "merch_info": merch.merch_info,
                "date_time": merch.date_time,
                "merch_coast": merch.merch_coast
            })
        self.session.close()
        return activities
