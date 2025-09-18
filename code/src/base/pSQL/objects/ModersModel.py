from sqlalchemy import update
from sqlalchemy.sql.expression import func

import json
from .App import db

ADMINS_PEER = []

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы модераторов")

class ModersModel:
    def __init__(self, activities_id: int = 0, uuid: int = 0, id: int = 0):
        self.session = db
        self.activities_id = activities_id
        self.uuid = uuid
        self.id = id

        from ..models.Moders import Moders
        self.Moders = Moders

        from ..models.ActiveUsers import ActiveUsers
        self.Activities = Activities

        from ..models.Activities import Activities
        self.ActiveUsers = ActiveUsers

    def upload_past_moders(self):
        with open('./src/base/peer-data/activities_moders.json', mode='r', encoding='UTF-8') as f:
            cur_moders = json.load(f)
        for moder in cur_moders:
            existing_moder = self.session.query(self.Moders).filter(self.Moders.id == moder['id']).first()
            if existing_moder:
                continue
            else:
                new_moder = self.Moders(id=moder['id'], user_uuid=moder['user_uuid'], activities_id=moder['active_id'])
                self.session.add(new_moder)
                self.session.commit()
        self.session.close()
        return {"status": True}
    
    def confirmation(self):
        res = self.session.query(self.ActiveUsers, self.Activities).join(self.Activities, self.Activities.id == self.ActiveUsers.activities_id).filter(self.ActiveUsers.activities_id == self.Activities.id, self.ActiveUsers.valid == 0, self.Activities.id == self.activities_id).all()
        if res:
            result = []
            for activities in res:
                data = {
                    "id": activities[0].id,
                    "name": activities[1].name,
                    "uuid_from": activities[0].uuid_from,
                    "uuid_to": activities[0].uuid_to,
                    "description": activities[0].description,
                    "date_time": activities[0].date_time,
                    "coast": activities[1].coast,
                    "need_valid": activities[1].need_valid
                }
                result.append(data)
            self.session.close()
            return result
        self.session.close()
        return res
        
    def do_valid(self, action_id):
        res = False
        user_uuid = self.session.query(self.Moders.user_uuid).join(self.ActiveUsers, self.ActiveUsers.activities_id == self.Moders.activities_id).filter(self.ActiveUsers.id == action_id).first()
        if str(self.uuid) == user_uuid or int(self.uuid) in ADMINS_PEER:
            stmt = update(ActiveUsers).where(ActiveUsers.id == action_id).values(valid=1)
            self.session.execute(stmt)
            self.session.commit()
            res = True
        self.session.close()
        return res

    def do_not_valid(self, action_id):
        res = False
        user_uuid = self.session.query(self.Moders.user_uuid).join(self.ActiveUsers, self.ActiveUsers.activities_id == self.Moders.activities_id).filter(self.ActiveUsers.id == action_id).first()
        if str(self.uuid) == user_uuid or int(self.uuid) in self.ActiveUsers:
            stmt = update(self.ActiveUsers).where(self.ActiveUsers.id == action_id).values(valid=2)
            self.session.execute(stmt)
            self.session.commit()
            res = True
        self.session.close()
        return res

    def get_moders(self):
        result = self.session.query(self.Moders.user_uuid, self.Activities.id, self.Activities.name).join(self.Activities, self.Activities.id == self.Moders.activities_id).all()
        moders = []
        for re in result:
            moder = {}
            moder['moder_id'] = re[0]
            moder['activity_id'] = re[1]
            moder['activity_name'] = re[2]
            moders.append(moder)
        self.session.close()
        return moders

    def add_moder(self):
        existing_activity = self.session.query(self.Activities).filter(self.Activities.id == self.activities_id).first()
        if existing_activity:
            existing_moder = self.session.query(self.Moders).filter(self.Moders.user_uuid == str(self.uuid), self.Moders.activities_id == self.activities_id).first()
            if existing_moder:
                return {"msg": f"У {self.uuid} уже существует активность {self.activities_id}"}
            else:
                max_id = self.session.query(func.max(self.Moders.id)).scalar() or 0
                new_id = max_id + 1
                new_moder = self.Moders(id=new_id, user_uuid=self.uuid, activities_id=self.activities_id)
                self.session.add(new_moder)
                self.session.commit()
                self.session.close()
                return {"msg": "Создано"}
        else:
            self.session.close()
            return {"msg": "Не существует такой активности"}

    def is_moder(self):
        existing_moder = self.session.query(self.Moders).filter(self.Moders.user_uuid == str(self.uuid)).first()
        self.session.close()
        if existing_moder:
            return True
        else:
            return False