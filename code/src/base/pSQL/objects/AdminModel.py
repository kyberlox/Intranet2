from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from typing import List, Optional, Dict

from datetime import datetime, timedelta

from .models import ActiveUsers, Moders
from .App import db

ADMINS_PEER = [] #!!!!!!!!!!!!!!!!!!ТЫ ЧЕ, ХРАНИШЬ СПИСОК АДМИНОВ В ПАМЯТИ ПРОГРАММЫ?!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!
from services import LogsMaker
#!!!!!!!!!!!!!!!

class AdminModel:
    def __init__(self, uuid: int = 0):
        self.session = db
        self.uuid = uuid
        self.ActiveUsers = ActiveUsers
        self.Moders = Moders

    def new_active(self, data):
        res = False
        uuid_from = data["uuid_from"]
        uuid_to =  data["uuid_to"]
        activities_id = data["activities_id"]
        description = data["description"]

        month_ago = datetime.now() - timedelta(days=30)
        likes_count = self.session.query(self.ActiveUsers).filter(self.ActiveUsers.uuid_from == uuid_from, self.ActiveUsers.activities_id == 0, self.ActiveUsers.date_time >= month_ago).count()
        likes_left = 10 - likes_count
        needs = self.session.scalars(self.session.query(self.ActiveUsers.id).where(self.ActiveUsers.need_valid == True)).all()
        
        if activities_id in needs:
            if likes_left < 0:
                return {"result" : False}
            else:
                max_id = self.session.query(func.max(self.ActiveUsers.id)).scalar() or 0
                new_id = max_id + 1
                new_action = self.ActiveUsers(
                    id=new_id,
                    uuid_from=uuid_from,
                    uuid_to=uuid_to,
                    description=description,
                    activities_id=activities_id,
                    valid=0,
                    date_time=datetime.now()
                )
        else:
            max_id = self.session.query(func.max(self.ActiveUsers.id)).scalar() or 0
            new_id = max_id + 1
            new_action = self.ActiveUsers(
                id=new_id,
                uuid_from=uuid_from,
                uuid_to=uuid_to,
                description=description,
                activities_id=activities_id,
                valid=1,
                date_time=datetime.now()
            )
        
        activity_moder = self.session.query(self.Moders.user_uuid).where(self.Moders.activities_id == activities_id).scalar()
        
        if activity_moder:
            if uuid_from == activity_moder or activity_moder == '*':
                
                self.session.add(new_action)
                self.session.commit()
                self.session.close()
                return {"result" : True}
        else:
            self.session.close()
            return {"result" : False}

    def get_admins_list(self):
        return ADMINS_PEER
    
    def add_peer_admin(self):
        if int(self.uuid) in ADMINS_PEER:
            self.session.close()
            return {"msg": "уже существует"}
        else:
            ADMINS_PEER.append(int(self.uuid))
            self.session.close()
            return {"msg": "добавлен"}
    
    def delete_admin(self):
        if int(self.uuid) in ADMINS_PEER:
            ADMINS_PEER.remove(int(self.uuid))
            return {"msg": "удален"}
        else:
            return {"msg": "отсутствует такой админ"}