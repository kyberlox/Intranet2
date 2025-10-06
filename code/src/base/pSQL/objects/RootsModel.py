from src.services.LogsMaker import LogsMaker
from .App import flag_modified, get_db, func
LogsMaker().ready_status_message("Успешная инициализация таблицы Прав доступа")



class RootsModel:
    def __init__(self, user_uuid: int = 0):
        # from .App import db
        # self.session = db
        from ..models.User import User
        self.User = User
        from ..models.Roots import Roots
        self.Roots = Roots
        self.user_uuid = user_uuid

    def get_token_by_id(self):
        db_gen = get_db()
        database = next(db_gen)
        result = database.query(self.Roots.root_token).filter(self.Roots.id == self.id).first()
        return result

    def get_token_by_uuid(self):
        db_gen = get_db()
        database = next(db_gen)
        try:
            result = database.query(self.Roots.root_token).filter(self.Roots.user_uuid == self.user_uuid).scalar()
            return result
        except Exception as e:
            LogsMaker().error_message(str(e))

    def token_processing_for_peer(self, root_token):
        roots = {
            'user_id': self.user_uuid
        }
        if root_token:
            for key, value in root_token.items():
                if key == "PeerAdmin":
                    roots["PeerAdmin"] = value
                elif key == "PeerModer":
                    roots["PeerModer"] = value
                elif key == "PeerCurator":
                    roots["PeerCurator"] = value
        return roots
    
    def token_processing_for_vision(self, root_token):
        roots = {
            'user_id': self.user_uuid
        }
        if root_token:
            for key, value in root_token.items():
                if key == "VisionAdmin":
                    roots["VisionAdmin"] = value
                elif key == "VisionRoots":
                    roots["VisionRoots"] = value
        return roots
    
    def token_processing_for_editor(self, root_token):
        roots = {
            'user_id': self.user_uuid
        }
        if root_token:
            for key, value in root_token.items():
                if key == "EditorAdmin":
                    roots["EditorAdmin"] = value
                elif key == "EditorModer":
                    roots["EditorModer"] = value
        return roots

    def create_primary_admins(self):
        db_gen = get_db()
        database = next(db_gen)
        BOYS_DONT_CRY = [2366, 2375, 4133]
        try:
            for guy in BOYS_DONT_CRY:
                existing_admin = database.query(self.Roots).filter(self.Roots.user_uuid == guy).first()
                if existing_admin:
                    continue
                    
                else:
                    max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                    new_id = max_id + 1
                    new_moder = self.Roots()
                    new_moder.id=new_id
                    new_moder.user_uuid=guy
                    new_moder.root_token={
                        "PeerAdmin": True,
                        "VisionAdmin": True,
                        "EditorAdmin": True
                    }
                    
                    database.add(new_moder)
                    database.commit()
            return True
            
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка создания первичных админов: {e}")

    def create_editor_moder(self, sec_id):
        db_gen = get_db()
        database = next(db_gen)
        try:
            existing_moder = database.query(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).filter(self.Roots.user_uuid == self.user_uuid).first()
            if existing_moder:
                if "EditorModer" in existing_moder.root_token.keys() and sec_id in existing_moder.root_token['EditorModer']:
                    return False
                elif "EditorModer" in existing_moder.root_token.keys():
                    existing_moder.root_token["EditorModer"].append(sec_id)
                    flag_modified(existing_moder, 'root_token')
                    database.commit()
                    return True
                else:
                    existing_moder.root_token["EditorModer"] = [sec_id]
                    flag_modified(existing_moder, 'root_token')
                    database.commit()
                    return True
            else:
                max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                new_id = max_id + 1
                new_moder = self.Roots(
                    id=new_id,
                    user_uuid=int(self.user_uuid),
                    root_token={"EditorModer": [sec_id]}
                )
                database.add(new_moder)
                database.commit()
                return True
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка добавления модератора редакторки в раздел с id = {sec_id}: {e}")
    
    def delete_editor_moder(self, sec_id):
        db_gen = get_db()
        database = next(db_gen)
        try:
            user = database.query(self.Roots).filter(
                self.Roots.user_uuid == self.user_uuid,
                self.Roots.root_token['EditorModer'].contains([sec_id])
            ).first()
            if user:
                user.root_token['EditorModer'].remove(sec_id)
                flag_modified(user, 'root_token')
                database.commit()
                return LogsMaker().info_message(f"У раздела с id = {sec_id} пользователь с id = {self.user_uuid} больше не является редактором")
            else:
                return LogsMaker().info_message(f"У раздела с id = {sec_id} не редактировал пользователь с id = {self.user_uuid}")

        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении редактора с id = {self.user_uuid} из раздела с id = {sec_id}: {e}")
    
    def create_editor_admin(self):
        db_gen = get_db()
        database = next(db_gen)
        try:
            existing_admin = database.query(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).filter(self.Roots.user_uuid == self.user_uuid).first()
            if existing_admin:
                if "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == True:
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} уже является администратором радакторки")
                elif "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == False:
                    existing_admin.root_token["EditorAdmin"] = True
                    flag_modified(existing_admin, 'root_token')
                    database.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
                else:
                    existing_admin.root_token["EditorAdmin"] = True
                    flag_modified(existing_admin, 'root_token')
                    database.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
            else:
                max_id = database.query(func.max(self.Roots.id)).scalar() or 0
                new_id = max_id + 1
                new_admin = self.Roots(
                    id=new_id,
                    user_uuid=int(self.user_uuid),
                    root_token={"EditorAdmin": True}
                )
                # self.Roots.user_uuid=int(self.uuid)
                # self.Roots.root_token={"PeerAdmin": True}
                database.add(new_admin)
                database.commit()
                return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при назначении пользователя с id = {self.user_uuid} администратором радакторки: {e}")
    
    def delete_editor_admin(self):
        db_gen = get_db()
        database = next(db_gen)
        try:
            existing_admin = database.query(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).filter(self.Roots.user_uuid == self.user_uuid).first()
            if existing_admin:
                if "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == True:
                    existing_admin.root_token["EditorAdmin"] = False
                    flag_modified(existing_admin, 'root_token')
                    database.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} больше не администратор радакторки")
            return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} не был администратором радакторки")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении пользователя с id = {self.user_uuid} из администраторов радакторки: {e}")

    def get_editors_list(self, sec_id):
        from ..models.Section import Section
        db_gen = get_db()
        database = next(db_gen)
        result = []
        try:
            moders = database.query(self.Roots).filter(self.Roots.root_token.has_key("EditorModer")).all()
            for moder in moders:
                for sec_id in moder.root_token['EditorModer']:
                    section_name = database.query(Section.name).filter(Section.id == sec_id).scalar()
                    moder_fio = database.query(self.User.name, self.User.second_name, self.User.last_name).filter(self.User.id == moder.user_uuid).first()
                    moder_info = {
                        'moder_id': moder.user_uuid,
                        "moder_name": moder_fio.name,
                        "moder_second_name": moder_fio.second_name,
                        "moder_last_name": moder_fio.last_name,
                        'section_id': sec_id,
                        'section_name': section_name
                    }
                    result.append(moder_info)

            return result
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка вывода кураторов: {e}")