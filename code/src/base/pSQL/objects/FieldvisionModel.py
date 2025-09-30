from src.services.LogsMaker import LogsMaker

LogsMaker().ready_status_message("Успешная инициализация таблицы Области Видимости")



class FieldvisionModel:
    def __init__(self, vision_name: str = '', id: int = 0):
        from .App import db
        self.session = db
        self.vision_name = vision_name
        self.id = id

        from ..models.Fieldvision import Fieldvision
        self.Fieldvision = Fieldvision

    def add_field_vision(self):
        from .App import func
        existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.vision_name == self.vision_name).first()
        if existing_vision:
            self.session.close()
            return {"msg": "Уже создано"}
        max_id = self.session.query(func.max(self.Fieldvision.id)).scalar() or 0
        new_id = max_id + 1
        new_vision = self.Fieldvision(id=new_id, vision_name=self.vision_name)
        self.session.add(new_vision)
        self.session.commit()
        self.session.close()
        return self.session.query(self.Fieldvision).filter(self.Fieldvision.vision_name == self.vision_name).first()

    def remove_field_vision(self):
        existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
        
        if existing_vision:
            self.session.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).delete()
            self.session.commit()
            self.session.close()
            return {"msg": "Удалено"}
        
        self.session.close()
        return {"msg": "Такой области не существует"}
    
    def find_vision_by_id(self):
        existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
        self.session.close()
        if existing_vision:
            return existing_vision
        return {"msg": "такого vision_id не существует"}
    
    def find_all_visions(self):
        res = self.session.query(self.Fieldvision).all()
        self.session.close()
        return res