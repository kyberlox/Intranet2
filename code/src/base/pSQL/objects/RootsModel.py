from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Прав доступа")



class RootsModel:
    def __init__(self, user_uuid: int = 0):
        from .App import db
        self.session = db
        from ..models.Roots import Roots
        self.Roots = Roots
        self.user_uuid = user_uuid

    def get_token_by_id(self):
        result = self.session.query(self.Roots.root_token).filter(self.Roots.id == self.id).first()
        self.session.close()
        return result

    def get_token_by_uuid(self):
        try:
            result = self.session.query(self.Roots.root_token).filter(self.Roots.user_uuid == self.user_uuid).scalar()
            self.session.close()
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

    def create_primary_admins(self):
        BOYS_DONT_CRY = [2366, 2375, 4133]
        try:
            for guy in BOYS_DONT_CRY:
                existing_admin = self.session.query(Roots).filter(Roots.user_uuid == guy).first()
                    if not "PeerAdmin" in existing_admin.root_token.keys() and not "VisionAdmin" in existing_admin.root_token.keys():
                        max_id = self.session.query(func.max(self.Roots.id)).scalar() or 0
                        new_id = max_id + 1
                        new_moder = self.Roots()
                        new_moder.id=new_id
                        new_moder.user_uuid=guy
                        new_moder.root_token={
                            "PeerAdmin": True,
                            "VisionAdmin": True
                        }
                        
                        self.session.add(new_moder)
                        self.session.commit()
                    else:
                        return LogsMaker().info_message(f"Пользователь с id = {guy} уже назначен администратором")
            return True
            
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"Ошибка создания первичных админов: {e}")
        finally:
            self.session.close()