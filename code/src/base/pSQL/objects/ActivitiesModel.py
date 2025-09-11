import json

from .models import Activities
from .App import db




#!!!!!!!!!!!!!!!
from services import LogsMaker
#!!!!!!!!!!!!!!!

class ActivitiesModel:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, need_valid: bool = False):
        self.session = db
        self.id = id
        self.name = name
        self.coast = coast
        self.need_valid = need_valid
        self.Activities = Activities

    def upload_base_activities(self):
        with open('./src/base/peer-data/base_activities.json', mode='r', encoding='UTF-8') as f:
            cur_activities = json.load(f)
        for activity in cur_activities:
            existing_activity = self.session.query(self.Activities).filter(self.Activities.id == activity['id']).first()
            if existing_activity:
                continue
            else:
                new_activity = self.Activities(id=activity['id'], name=activity['name'], coast=activity['coast'], need_valid=activity['need_valid'])
                self.session.add(new_activity)
                self.session.commit()
        self.session.close()
        return {"status": True}
    
    def find_all_activities(self):
        res = self.session.query(self.Activities).all()
        self.session.close()
        return res

    def update_activity(self):
        activity = self.session.query(self.Activities).get(self.id)
        if activity:
            activity.name = self.name
            activity.coast = self.coast
            activity.user_uuid = self.user_uuid
            self.session.commit()
            self.session.close()
            self.session.close()
            return {"status": True}
        else:
            return {"msg": "нет такого id"}

    def delete_activity(self):
        existing_activity = self.session.query(self.Activities).get(self.id)
        if existing_activity:
            self.session.delete(existing_activity)
            self.session.commit()
            self.session.close()
            return {"status": True}
        else:
            self.session.close()
            return {"msg": "нет такой активности"}