from datetime import datetime
from ..models.Roots import Roots
from datetime import timedelta
from ..models.ActiveUsers import ActiveUsers
from ..models.Activities import Activities
from ..models.PeerHistory import PeerHistory
from ..models.User import User

from .MerchStoreModel import MerchStoreModel

from .App import flag_modified, func, update, JSONB, get_db # db, 

from src.services.LogsMaker import LogsMaker

class PeerUserModel:
    def __init__(self, activities_id: int = 0, uuid: int = 0, id: int = 0):
        # self.session = db
        self.activities_id = activities_id
        self.uuid = uuid
        self.id = id
        self.Roots = Roots
    
    def points_to_confirm(self):
        db_gen = get_db()
        database = next(db_gen)
        res = database.query(ActiveUsers, Activities).join(Activities, Activities.id == ActiveUsers.activities_id).filter(ActiveUsers.activities_id == Activities.id, ActiveUsers.valid == 0, Activities.id == self.activities_id).all()
        # database.close()
        result = []
        if res:
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
        return result
    
    def do_valid(self, action_id, uuid_to, roots):
        db_gen = get_db()
        database = next(db_gen)
        res = False
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                active_info = database.query(Activities).join(ActiveUsers, Activities.id == ActiveUsers.activities_id).filter(ActiveUsers.id == action_id).scalar()
                if active_info and active_info.need_valid == True:
                    stmt = update(ActiveUsers).where(ActiveUsers.id == action_id).values(valid=1)
                    res = True

                    MerchStoreModel(uuid_to).upload_user_sum(active_info.coast)
                    database.execute(stmt) 
                    database.commit()
                else:
                    return LogsMaker().info_message(f"Активности с id = {action_id} не существует")
            return res
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка валидации: {e}")
        # finally:
        #     database.close()
    
    def do_not_valid(self, action_id, roots):
        db_gen = get_db()
        database = next(db_gen)
        res = False
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                active_info = database.query(Activities).join(ActiveUsers, Activities.id == ActiveUsers.activities_id).filter(ActiveUsers.id == action_id).scalar()
                if active_info and active_info.need_valid == True:
                    stmt = update(ActiveUsers).where(ActiveUsers.id == action_id).values(valid=2)
                    res = True
                    database.execute(stmt) 
                    database.commit()
                else:
                    return LogsMaker().info_message(f"Активности с id = {action_id} не существует")
            return res
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка валидации активности: {e}")
        # finally:
        #     database.close()

    def get_curators(self):
        db_gen = get_db()
        database = next(db_gen)
        result = []
        try:
            curators = database.query(self.Roots).filter(self.Roots.root_token.has_key("PeerCurator")).all()
            for curator in curators:
                for active_id in curator.root_token['PeerCurator']:
                    active_name = database.query(Activities.name).filter(Activities.id == active_id).scalar()
                    curator_fio = database.query(User.name, User.second_name, User.last_name).filter(User.id == curator.user_uuid).first()
                    active_info = {
                        'curator_id': curator.user_uuid,
                        "curator_name": curator_fio.name,
                        "curator_second_name": curator_fio.second_name,
                        "curator_last_name": curator_fio.last_name,
                        'activity_id': active_id,
                        'activity_name': active_name
                    }
                    result.append(active_info)

            return result
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка вывода кураторов: {e}")
        # finally:
        #     database.close()

    def add_curator(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_curator = database.query(self.Roots).filter(Roots.user_uuid == int(self.uuid)).first()
                if existing_curator:
                    if "PeerCurator" in existing_curator.root_token.keys() and self.activities_id in existing_curator.root_token['PeerCurator']:
                        return False
                    elif "PeerCurator" in existing_curator.root_token.keys():
                        existing_curator.root_token["PeerCurator"].append(self.activities_id)
                        flag_modified(existing_curator, 'root_token')
                        database.commit()
                        return True
                    else:
                        existing_curator.root_token["PeerCurator"] = [self.activities_id]
                        flag_modified(existing_curator, 'root_token')
                        database.commit()
                        return True
                else:
                    max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                    new_id = max_id + 1
                    new_moder = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerCurator": [self.activities_id]}
                    )
                    database.add(new_moder)
                    database.commit()
                    return True
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка добавления куратора: {e}")
        # finally:
        #     database.close()

    def delete_curators(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_activity = database.query(Activities).get(self.activities_id)
                if existing_activity:
                    users_with_activity = database.query(self.Roots).filter(
                        self.Roots.root_token['PeerCurator'].contains([self.activities_id])
                    ).all()
                    for user in users_with_activity:
                        root_token = user.root_token
                        if 'PeerCurator' in user.root_token.keys() and self.activities_id in user.root_token['PeerCurator']:
                            if self.activities_id in root_token['PeerCurator']:
                                user.root_token['PeerCurator'].remove(self.activities_id)
                                flag_modified(user, 'root_token')
                                database.commit()
                    return LogsMaker().info_message(f"У активности с id = {self.activities_id} больше нет кураторов")
                else:
                    return LogsMaker().info_message(f"Активности с id = {self.activities_id} не существует")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении кураторов из активности с id = {self.activities_id}: {e}")
        # finally:
        #     database.close()
    
    def delete_curator(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                user = database.query(self.Roots).filter(
                    self.Roots.user_uuid == self.uuid,
                    self.Roots.root_token['PeerCurator'].contains([self.activities_id])
                ).first()
                if user:
                    user.root_token['PeerCurator'].remove(self.activities_id)
                    flag_modified(user, 'root_token')
                    database.commit()
                    return LogsMaker().info_message(f"У активности с id = {self.activities_id} пользователь с id = {self.uuid} больше не является куратором")
                else:
                    return LogsMaker().info_message(f"Активности с id = {self.activities_id} не курировал пользователь с id = {self.uuid}")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении куратора с id = {self.uuid} из активности с id = {self.activities_id}: {e}")
        # finally:
        #     database.close()
            
    def send_points(self, data, roots):
        db_gen = get_db()
        database = next(db_gen)
        res = False
        uuid_from = str(roots['user_id'])
        uuid_to =  data["uuid_to"]
        activities_id = data["activities_id"]
        description = data["description"]
        existing_user = database.query(User).filter(User.id == uuid_to, User.active == True).first()
        if not existing_user:
            return LogsMaker().warning_message(f"Пользователя с id = {uuid_to} не существует")
        try:
            month_ago = datetime.now() - timedelta(days=30)
            likes_count = database.query(ActiveUsers).filter(ActiveUsers.uuid_from == uuid_from, ActiveUsers.activities_id == activities_id, ActiveUsers.date_time >= month_ago).count()
            likes_left = 10 - likes_count
            needs = database.scalars(database.query(Activities.id).where(Activities.need_valid == True)).all()
    
            if activities_id in needs:
                if likes_left < 0:
                    return LogsMaker().warning_message(f"У пользователя с id = {uuid_to} закончились баллы для активности с id = {activities_id}")
                elif uuid_from == uuid_to:
                    return LogsMaker().warning_message(f"Пользователь с id = {uuid_to} пытается поставить быллы сам себе!")
                else:
                    max_id = database.query(func.max(ActiveUsers.id)).scalar() or 0
                    new_id = max_id + 1
                    new_action = ActiveUsers(
                        id=new_id,
                        uuid_from=uuid_from,
                        uuid_to=uuid_to,
                        description=description,
                        activities_id=activities_id,
                        valid=0,
                        date_time=datetime.now()
                    )
                    database.add(new_action)
                    database.commit()
                    return LogsMaker().info_message(f"Вы успешно отправили активность пользователю с id = {uuid_to} ")
            elif "PeerCurator" in roots.keys() or "PeerAdmin" in roots.keys():
                max_id = database.query(func.max(ActiveUsers.id)).scalar() or 0
                new_id = max_id + 1
                new_action = ActiveUsers(
                    id=new_id,
                    uuid_from=uuid_from,
                    uuid_to=uuid_to,
                    description=description,
                    activities_id=activities_id,
                    valid=1,
                    date_time=datetime.now()
                )
                value = 0
                flag = False
                if activities_id in roots["PeerCurator"]:
                    database.add(new_action)
                    database.commit()
                    # тут начислить пользователю баллы
                    value = database.query(Activities.coast).filter(Activities.id == activities_id).scalar()
                    MerchStoreModel(uuid_to).upload_user_sum(value)
                    flag = True
                elif roots["PeerAdmin"] == True:
                    database.add(new_action)
                    database.commit()
                    # тут начислить пользователю баллы
                    value = database.query(Activities.coast).filter(Activities.id == activities_id).scalar()
                    MerchStoreModel(uuid_to).upload_user_sum(value)
                    flag = True

                if flag:
                    # сохраняем в историю начислений
                    add_history = PeerHistory(
                        user_uuid=roots['user_id'],
                        user_to=uuid_to,
                        active_info=description,
                        active_coast=value,
                        info_type='activity',
                        date_time=datetime.now()
                    )
                    database.add(add_history) 
                    database.commit()
                    return LogsMaker().info_message(f"Вы успешно отправили активность пользователю с id = {uuid_to} ")
                else:
                    return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка отправления баллов: {e}")
        # finally:
        #     database.close()
    
    def get_admins_list(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        result = []
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                admins = database.query(self.Roots).filter(self.Roots.root_token.has_key("PeerAdmin")).all()
                for admin in admins:
                    if admin.root_token["PeerAdmin"] == True:
                        admin_fio = database.query(User.name, User.second_name, User.last_name).filter(User.id == admin.user_uuid).first()
                        admin_info = {
                            "admin_id": admin.user_uuid,
                            "admin_name": admin_fio.name,
                            "admin_second_name": admin_fio.second_name,
                            "admin_last_name": admin_fio.last_name
                        }
                        result.append(admin_info)
                return result
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при выводе админов системы эффективности: {e}")
        # finally:
        #     database.close()
    
    def add_peer_admin(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_admin = database.query(self.Roots).join(User, self.Roots.user_uuid == User.id).filter(self.Roots.user_uuid == self.uuid).first()
                if existing_admin:
                    if "PeerAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["PeerAdmin"] == True:
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} уже является администратором системы эффективности")
                    elif "PeerAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["PeerAdmin"] == False:
                        existing_admin.root_token["PeerAdmin"] = True
                        flag_modified(existing_admin, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен администратором системы эффективности")
                    else:
                        existing_admin.root_token["PeerAdmin"] = True
                        flag_modified(existing_admin, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен администратором системы эффективности")
                else:
                    max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                    new_id = max_id + 1
                    new_admin = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerAdmin": True}
                    )
                    # self.Roots.user_uuid=int(self.uuid)
                    # self.Roots.root_token={"PeerAdmin": True}
                    database.add(new_admin)
                    database.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен администратором системы эффективности")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при назначении пользователя с id = {self.uuid} администратором системы эффективности: {e}")
        # finally:
        #     database.close()
    
    def delete_admin(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_admin = database.query(self.Roots).join(User, self.Roots.user_uuid == User.id).filter(self.Roots.user_uuid == self.uuid).first()
                if existing_admin:
                    if "PeerAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["PeerAdmin"] == True:
                        existing_admin.root_token["PeerAdmin"] = False
                        flag_modified(existing_admin, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} больше не администратор системы эффективности")
                return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не был администратор системы эффективности")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении пользователя с id = {self.uuid} из администраторов системы эффективности: {e}")
        # finally:
        #     database.close()
    
    def add_peer_moder(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_moder = database.query(self.Roots).join(User, self.Roots.user_uuid == User.id).filter(self.Roots.user_uuid == self.uuid).first()
                if existing_moder:
                    if "PeerModer" in existing_moder.root_token.keys() and existing_moder.root_token["PeerModer"] == True:
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} уже является модератором системы эффективности")
                    elif "PeerModer" in existing_moder.root_token.keys() and existing_moder.root_token["PeerModer"] == False:
                        existing_moder.root_token["PeerModer"] = True
                        flag_modified(existing_moder, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен модератором системы эффективности")
                    else:
                        existing_moder.root_token["PeerModer"] = True
                        flag_modified(existing_moder, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен модератором системы эффективности")
                else:
                    max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                    new_id = max_id + 1
                    new_moder = self.Roots(
                        id=new_id,
                        user_uuid=int(self.uuid),
                        root_token={"PeerModer": True}
                    )
                    # self.Roots.user_uuid=int(self.uuid)
                    # self.Roots.root_token={"PeerModer": True}
                    database.add(new_moder)
                    database.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.uuid} назначен модератором системы эффективности")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при назначении пользователя с id = {self.uuid} модератором системы эффективности: {e}")
        # finally:
        #     database.close()

    def delete_peer_moder(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        try:
            if "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                existing_moder = database.query(self.Roots).join(User, self.Roots.user_uuid == User.id).filter(self.Roots.user_uuid == self.uuid).first()
                if existing_moder:
                    if "PeerModer" in existing_moder.root_token.keys() and existing_moder.root_token["PeerModer"] == True:
                        existing_moder.root_token["PeerModer"] = False
                        flag_modified(existing_moder, 'root_token')
                        database.commit()
                        return LogsMaker().info_message(f"Пользователь с id = {self.uuid} больше не модератор системы эффективности")
                return LogsMaker().info_message(f"Пользователь с id = {self.uuid} не был модератор системы эффективности")
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении пользователя с id = {self.uuid} из модераторов системы эффективности: {e}")
        # finally:
        #     database.close()
    
    def get_moders_list(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        result = []
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                moders = database.query(self.Roots).filter(self.Roots.root_token.has_key("PeerModer")).all()
                for moder in moders:
                    if moder.root_token["PeerModer"] == True:
                        moder_fio = database.query(User.name, User.second_name, User.last_name).filter(User.id == moder.user_uuid).first()
                        moder_info = {
                            "moder_id": moder.user_uuid,
                            "moder_name": moder_fio.name,
                            "moder_second_name": moder_fio.second_name,
                            "moder_last_name": moder_fio.last_name
                        }
                        result.append(moder_info)
                return result
            else:
                return LogsMaker().warning_message(f"Недостаточно прав")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при выводе модераторов системы эффективности: {e}")
        # finally:
        #     database.close()
            
    def get_curators_history(self, roots):
        db_gen = get_db()
        database = next(db_gen)
        if "PeerAdmin" in roots.keys() or "PeerCurator" in roots.keys():
            user_history = database.query(PeerHistory).filter(PeerHistory.user_uuid == roots['user_id'], PeerHistory.info_type == 'activity').all()
            activity_history = []
            if user_history:
                for active in user_history:
                    user_info = database.query(User.name, User.second_name, User.last_name).filter(User.id == active.user_to).first()
                    user_fio = user_info.last_name + " " + user_info.name + " " + user_info.second_name
                    active_name = database.query(Activities.name).join(ActiveUsers, ActiveUsers.activities_id == Activities.id).filter(ActiveUsers.id == active.id).scalar()
                    
                    info = {
                        "id": active.id,
                        "date_time": active.date_time,
                        "uuid_to": active.user_to,
                        "uuid_to_fio": user_fio,
                        "description": active.active_info,
                        "activity_name": active_name,
                        "coast": active.active_coast
                    } 
                    # database.close()
                    activity_history.append(info)
                return activity_history
            else:
                return activity_history
        else:
            return LogsMaker().warning_message(f"Недостаточно прав")
    
    def return_points_to_user(self, note_id, user_uuid):
        db_gen = get_db()
        database = next(db_gen)
        try:
            points = database.query(PeerHistory.merch_coast).filter(PeerHistory.id == note_id).scalar()
            status = database.query(PeerHistory).filter(PeerHistory.id == note_id).delete()
            if status:
                user_info = database.query(self.Roots).filter(self.Roots.user_uuid == user_uuid).first()
                user_info.user_points = user_info.user_points + points
                database.commit()
                return True
            else:
                return LogsMaker().error_message(f"Ошибка при удалении записи c id = {note_id} из PeerHistory")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при возрате средств пользователю с id = {user_uuid}: {e}")
        # finally:
        #     database.close()
    
    def remove_user_points(self, action_id, roots):
        db_gen = get_db()
        database = next(db_gen)
        res = False
        try:
            if "PeerModer" in roots.keys() and roots["PeerModer"] == True or "PeerAdmin" in roots.keys() and roots["PeerAdmin"] == True:
                active_info = database.query(Activities).join(ActiveUsers, Activities.id == ActiveUsers.activities_id).filter(ActiveUsers.id == action_id).scalar()
                print(active_info.__dict__)
                if active_info:
                    action_info = database.query(ActiveUsers).filter(ActiveUsers.id == action_id, ActiveUsers.valid == 1).first()
                    if action_info:
                        stmt = update(ActiveUsers).where(ActiveUsers.id == action_id).values(valid=2)
                        res = True
                        database.execute(stmt) 
                        user_info = database.query(self.Roots).filter(self.Roots.user_uuid == self.uuid).first()
                        user_info.user_points = user_info.user_points - active_info.coast  
                        database.commit()
                        return LogsMaker().info_message(f"Успешно сняты баллы у пользователя с id = {self.uuid}")
                    else:
                        return LogsMaker().info_message(f"Активности с id = {action_id} не была валидна, за нее нельзя списать баллы")
                else:
                    return LogsMaker().info_message(f"Активности с id = {action_id} не существует")
            return res
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка при удалении баллов у пользователя с id {self.uuid} за action_id = {action_id}: {e}")