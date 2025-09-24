from ..models.Fieldvision import Fieldvision
from .App import db



#!!!!!!!!!!!!!!!
from src.services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class UservisionsRootModel:
    def __init__(self, id: int = 0, vision_id: int = 0, user_id: int = 0):
        self.session = db
        self.id = id
        self.vision_id = vision_id
        self.user_id = user_id
        
        from ..models.Roots import Roots
        self.Roots = Roots
        self.Fieldvision = Fieldvision

        from ..models.User import User
        self.User = User

    def upload_user_to_vision(self, user_to, roots):
        try:
            if "VisionAdmin" in roots.keys() and roots["VisionAdmin"] == True:
                existing_user = self.session.query(self.Roots).filter(self.Roots.user_uuid == user_to).first()
                if existing_user:
                    if "VisionRoots" in existing_user.root_token.keys() and self.vision_id in existing_user.root_token['VisionRoots']:
                        return LogsMaker().warning_message(f"Пользователь с id = {user_to} уже существует в ОВ id = {self.vision_id}")
                    elif "VisionRoots" in existing_user.root_token.keys():
                        existing_user.root_token["VisionRoots"].append(self.vision_id)
                        flag_modified(existing_user, 'root_token')
                        self.session.commit()
                        return LogsMaker().info_message(f"Добавление пользователя с id = {user_to} в ОВ id = {self.vision_id} звершено успешно")
                    else:
                        existing_user.root_token["VisionRoots"] = [self.vision_id]
                        flag_modified(existing_user, 'root_token')
                        self.session.commit()
                        return LogsMaker().info_message(f"Добавление пользователя с id = {user_to} в ОВ id = {self.vision_id} звершено успешно")
                else:
                    new_user_vis = self.Roots
                    self.Roots.user_uuid=user_to
                    self.Roots.root_token={"VisionRoots": [self.vision_id]}
                    
                    self.session.add(new_user_vis)
                    self.session.commit()
                    return LogsMaker().info_message(f"Добавление пользователя с id = {user_to} в ОВ id = {self.vision_id} звершено успешно")
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"ошибка при добавлении пользователя в ОВ: {e}")
        finally:
            self.session.close()
    
    def upload_users_to_vision(self, user_data, roots):
        try:
            for user in user_data:
                self.user_id = user
                self.upload_user_to_vision(roots)
            return LogsMaker().info_message(f"Пользователи добавлены в ОВ id = {self.vision_id} звершено успешно")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"ошибка при добавлении пользователей в ОВ: {e}")
        finally:
            self.session.close()
    
    def remove_user_from_vision(self, roots):
        try:
            if "VisionAdmin" in roots.keys() and roots["VisionAdmin"] == True:
                existing_user = self.session.query(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).filter(self.Roots.user_uuid == self.user_id).first()
                if existing_user:
                    if "VisionRoots" in existing_user.root_token.keys() and self.vision_id in existing_user.root_token["VisionRoots"]:
                        existing_user.root_token["VisionRoots"].remove(self.vision_id)
                        flag_modified(existing_user, 'root_token')
                        self.session.commit()
                        return LogsMaker().info_message(f"Удаление пользователя с id = {self.user_id} из ОВ id = {self.vision_id} завершено успешно")
                return LogsMaker().info_message(f"Пользователь с id = {self.user_id} либо не существует, либо отсуствует в ОВ id = {self.vision_id}")
            else:
                return LogsMaker().warning_message(f"У Вас недостаточно прав")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"ошибка при удалении пользователя с id = {self.user_id} из ОВ {self.vision_id}: {e}")
        finally:
            self.session.close()

    def remove_users_from_vision(self, user_data):
        try:
            for user in user_data:
                self.user_id = user
                self.remove_user_from_vision(roots)
            return LogsMaker().info_message(f"Удаление пользователей из ОВ id = {self.vision_id} завершено успешно") 
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"ошибка при удалении пользователей из ОВ {self.vision_id}: {e}")
        finally:
            self.session.close()

    def find_users_in_vision(self):
        from .UserModel import UserModel
        try:
            result = []
            existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.id == self.vision_id).first()
            if existing_vision:
                # users_in_vis = self.session.query(UservisionsRoot).filter(UservisionsRoot.vision_id == self.vision_id).all()
                query = select(self.Roots.user_uuid).where(
                    exists().where(
                        self.Roots.root_token['VisionUser'].astext.cast(JSONB).contains([self.vision_id])
                    )
                )

                users_in_vis = self.session.scalars(query).all()
                for user in users_in_vis:
                    general_info = {}
                    user_info = UserModel(Id=user).find_by_id()
                    if user_info['active']:
                        general_info['id'] = user_info['id']
                        name = user_info['name'] if user_info['name'] else ''
                        last_name = user_info['last_name'] if user_info['last_name'] else ''
                        second_name = user_info['second_name'] if user_info['second_name'] else ''
                        general_info['name'] = last_name + ' ' + name + ' ' + second_name
                        general_info['depart'] = user_info['indirect_data']['uf_department'][0] if 'uf_department' in user_info['indirect_data'].keys() else None
                        general_info['depart_id'] = user_info['indirect_data']['uf_department_id'][0] if 'uf_department_id' in user_info['indirect_data'].keys() else None
                        if 'work_position' in user_info['indirect_data'].keys():
                            general_info['post'] = user_info['indirect_data']['work_position']
                        general_info['image'] = user_info['photo_file_url'] if 'photo_file_url' in user_info.keys() else None
                        result.append(general_info)
                return result
            return LogsMaker().warning_message(f"ОВ с id = {self.vision_id} не существует")
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"ошибка при выводе пользователей из ОВ {self.vision_id}: {e}")
        finally:
            self.session.close()

    def remove_depart_in_vision(self, dep_id, roots):
        users = self.find_users_in_vision()
        if users:
            for user in users:
                if user['depart_id'] == dep_id:
                    self.remove_user_from_vision(roots)
            return LogsMaker().info_message(f"Удаление пользователей из ОВ id = {self.vision_id} завершено успешно") 
        return LogsMaker().warning_message(f"Пользователей в ОВ с id = {self.vision_id} не существует")
