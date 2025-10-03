import json

from ..models.Activities import Activities
from .PeerUserModel import PeerUserModel
from .App import db, func, get_db



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Активностей")

class ActivitiesModel:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, need_valid: bool = False, active: bool = False):
        # self.session = db
        self.id = id
        self.name = name
        self.coast = coast
        self.need_valid = need_valid
        self.active = active
        self.Activities = Activities

    # def upload_base_activities(self):
    #     with open('./src/base/peer-data/base_activities.json', mode='r', encoding='UTF-8') as f:
    #         cur_activities = json.load(f)
    #     for activity in cur_activities:
    #         existing_activity = database.query(self.Activities).filter(self.Activities.id == activity['id']).first()
    #         if existing_activity:
    #             continue
    #         else:
    #             new_activity = self.Activities(id=activity['id'], name=activity['name'], coast=activity['coast'], need_valid=activity['need_valid'])
    #             database.add(new_activity)
    #             database.commit()
    #     database.close()
    #     return {"status": True}
    
    def find_all_activities(self):
        db_gen = get_db()
        database = next(db_gen)
        res = database.query(self.Activities).filter(self.Activities.active == True).all()
        # database.close()
        return res

    def update_activity(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                activity = database.query(self.Activities).get(self.id)
                if activity:
                    activity.name = self.name
                    activity.coast = self.coast
                    activity.need_valid = self.need_valid
                    activity.active = self.active
                    database.commit()

                    return LogsMaker().info_message(f"Обновление активности {self.name} звершено успешно")
                else:
                    return LogsMaker().warning_message(f"Активности с id = {self.id} не существует!")
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(str(e))
        # finally:
        #     database.close()

    def delete_activity(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_activity = database.query(self.Activities).filter(self.Activities.id == self.id, self.Activities.active == True).first()
                if existing_activity:
                    PeerUserModel(activities_id=existing_activity.id).delete_curators(roots)
                    existing_activity.active = self.active
                    database.commit()
                    
                    return LogsMaker().info_message(f"Удаление активности c id = {self.id} звершено успешно")
                else:
                    return LogsMaker().warning_message(f"Активности с id = {self.id} не существует или она не активна!")
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(str(e))
        # finally:
        #     database.close()
    
    def new_activity(self, data, roots):
        db_gen = get_db()
        database = next(db_gen)
        try: 
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                max_id = database.query(func.max(self.Activities.id)).scalar() or 0
                new_id = max_id + 1
                new_active = self.Activities(
                    id=new_id,
                    name=data['name'],
                    coast=data['coast'],
                    need_valid=data['need_valid'],
                    active=True
                )
                # self.Activities.id=new_id,
                # self.Activities.name=data['name']
                # self.Activities.coast=data['coast']
                # self.Activities.need_valid=data['need_valid']
                # database.add(new_active)s
                # database.commit()
                # добавляем модера
                if data['need_valid'] == True:
                    database.add(new_active)
                    database.commit()
                    return LogsMaker().info_message(f"Обновление активности {data['name']} звершено успешно")
                else:
                    uuid = data['uuid']
                    curator_status = PeerUserModel(activities_id=new_id, uuid=uuid).add_curator(roots)
                    if curator_status:
                        database.add(new_active)
                        database.commit()
                        LogsMaker().info_message(f"Пользователь с id = {uuid} назначен куратором активности {data['name']}")
                        return LogsMaker().info_message(f"Создание активности {data['name']} звершено успешно")
                    else:
                        return LogsMaker().warning_message(f"Активность {data['name']} не была создана!")
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(str(e))
        # finally:
        #     database.close()
