from src.services.LogsMaker import LogsMaker

from .App import flag_modified, select, func, delete
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


    async def get_token_by_id(self, session):
        res = await session.execute(select(self.Roots.root_token).where(self.Roots.user_uuid == int(self.user_uuid)))
        result = res.scalar_one_or_none()
        return result

    async def get_token_by_uuid(self, session):
        try:
            res = await session.execute(select(self.Roots.root_token).where(self.Roots.user_uuid == int(self.user_uuid)))
            result = res.scalar()
            return result
        except Exception as e:
            LogsMaker().error_message(str(e))


    async def token_processing_for_peer(self, root_token):
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
    

    async def token_processing_for_vision(self, root_token):
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
    

    async def token_processing_for_editor(self, root_token):
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


    async def create_primary_admins(self, session):
        BOYS_DONT_CRY = [2366, 2375, 4133]
        try:
            for guy in BOYS_DONT_CRY:
                res = await session.execute(select(self.Roots).where(self.Roots.user_uuid == guy))
                existing_admin = res.scalar_one_or_none()
                if existing_admin:
                    continue
                    
                else:

                    stmt = select(func.max(self.Roots.id))
                    result = await session.execute(stmt)
                    max_id = result.scalar() or 0
                    new_id = max_id + 1
                    new_moder = self.Roots()
                    new_moder.id=new_id
                    new_moder.user_uuid=guy
                    new_moder.root_token={
                        "PeerAdmin": True,
                        "VisionAdmin": True,
                        "EditorAdmin": True
                    }

                    session.add(new_moder)
                    await session.commit()
            return True
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка создания первичных админов: {e}")

    async def create_editor_moder(self, sec_id, session):
        try:
            stmt = select(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).where(self.Roots.user_uuid == self.user_uuid)
            res = await session.execute(stmt)
            existing_moder = res.scalar_one_or_none()
            if existing_moder:
                if "EditorModer" in existing_moder.root_token.keys() and sec_id in existing_moder.root_token['EditorModer']:
                    return False
                elif "EditorModer" in existing_moder.root_token.keys():
                    existing_moder.root_token["EditorModer"].append(sec_id)
                    flag_modified(existing_moder, 'root_token')

                    await session.commit()
                    return True
                else:
                    existing_moder.root_token["EditorModer"] = [sec_id]
                    flag_modified(existing_moder, 'root_token')

                    await session.commit()
                    return True
            else:
                stmt = select(func.max(self.Roots.id))
                result = await session.execute(stmt)
                max_id = result.scalar() or 0
                new_id = max_id + 1
                new_moder = self.Roots(
                    id=new_id,
                    user_uuid=int(self.user_uuid),
                    root_token={"EditorModer": [sec_id]}
                )

                session.add(new_moder)
                await session.commit()
                return True
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка добавления модератора редакторки в раздел с id = {sec_id}: {e}")
    
    async def delete_editor_moder(self, sec_id, session):
        try:
            stmt = select(self.Roots).where(self.Roots.user_uuid == self.user_uuid, self.Roots.root_token['EditorModer'].contains([sec_id]))
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()
            if user:
                user.root_token['EditorModer'].remove(sec_id)
                flag_modified(user, 'root_token')
                await session.commit()
                return LogsMaker().info_message(f"У раздела с id = {sec_id} пользователь с id = {self.user_uuid} больше не является редактором")
            else:
                return LogsMaker().info_message(f"У раздела с id = {sec_id} не редактировал пользователь с id = {self.user_uuid}")

        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении редактора с id = {self.user_uuid} из раздела с id = {sec_id}: {e}")
    

    async def create_editor_admin(self, session):
        try:
            stmt = select(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).where(self.Roots.user_uuid == self.user_uuid)
            res = await session.execute(stmt)
            existing_admin = res.scalar_one_or_none()
            if existing_admin:
                if "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == True:
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} уже является администратором радакторки")
                elif "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == False:
                    existing_admin.root_token["EditorAdmin"] = True
                    flag_modified(existing_admin, 'root_token')

                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
                else:
                    existing_admin.root_token["EditorAdmin"] = True
                    flag_modified(existing_admin, 'root_token')

                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
            else:
                stmt = select(func.max(self.Roots.id))
                result = await session.execute(stmt)
                max_id = result.scalar() or 0
                new_id = max_id + 1
                new_admin = self.Roots(
                    id=new_id,
                    user_uuid=int(self.user_uuid),
                    root_token={"EditorAdmin": True}
                )
                # self.Roots.user_uuid=int(self.uuid)
                # self.Roots.root_token={"PeerAdmin": True}

                session.add(new_admin)
                await session.commit()
                return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} назначен администратором радакторки")
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при назначении пользователя с id = {self.user_uuid} администратором радакторки: {e}")
    

    async def delete_editor_admin(self, session):
        try:
            stmt = select(self.Roots).join(self.User, self.Roots.user_uuid == self.User.id).where(self.Roots.user_uuid == self.user_uuid)
            res = await session.execute(stmt)
            existing_admin = res.scalar_one_or_none()
            if existing_admin:
                if "EditorAdmin" in existing_admin.root_token.keys() and existing_admin.root_token["EditorAdmin"] == True:
                    existing_admin.root_token["EditorAdmin"] = False
                    flag_modified(existing_admin, 'root_token')

                    await session.commit()
                    return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} больше не администратор радакторки")
            return LogsMaker().info_message(f"Пользователь с id = {self.user_uuid} не был администратором радакторки")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении пользователя с id = {self.user_uuid} из администраторов радакторки: {e}")


    async def get_editors_list(self, section_id, session):
        from ..models.Section import Section
        from src.model.File import File
        from .App import DOMAIN
        result = []
        try:
            stmt = select(self.Roots).where(self.Roots.root_token.has_key("EditorModer"))
            res = await session.execute(stmt)
            moders = res.scalars().all()
            for moder in moders:
                if section_id in moder.root_token['EditorModer']:
                # for sec_id in moder.root_token['EditorModer']:
                    stmt = select(Section.name).where(Section.id == section_id)
                    res = await session.execute(stmt)
                    section_name = res.scalar()

                    stmt = select(self.User.name, self.User.second_name, self.User.last_name, self.User.photo_file_id).where(self.User.id == moder.user_uuid)
                    res = await session.execute(stmt)
                    moder_fio = res.first()
                    if moder_fio.photo_file_id:
                        photo_inf = await File(id=moder_fio.photo_file_id).get_users_photo(session)
                        url = photo_inf['URL']
                        photo_file_url = f"{DOMAIN}{url}" 
                    else:
                        photo_file_url = "https://portal.emk.ru/local/templates/intranet/img/no-user-photo.png"
                    moder_info = {
                        'id': moder.user_uuid,
                        'name': f"{moder_fio.last_name} {moder_fio.name} {moder_fio.second_name}",
                        'photo_file_url': photo_file_url,
                        'section_id': section_id,
                        'section_name': section_name
                    }
                    result.append(moder_info)

            return result
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка вывода кураторов: {e}")