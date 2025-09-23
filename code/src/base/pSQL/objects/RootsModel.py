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
        result = self.session.query(self.Roots.root_token).filter(self.Roots.user_uuid == self.user_uuid).scalar()
        self.session.close()
        return result  

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
