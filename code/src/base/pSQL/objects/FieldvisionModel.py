from src.services.LogsMaker import LogsMaker
from .App import get_db
LogsMaker().ready_status_message("Успешная инициализация таблицы Области Видимости")

db_gen = get_db()
database = next(db_gen)

class FieldvisionModel:
    def __init__(self, vision_name: str = '', id: int = 0):
        # from .App import db
        # database = db
        self.vision_name = vision_name
        self.id = id

        from ..models.Fieldvision import Fieldvision
        self.Fieldvision = Fieldvision

    def add_field_vision(self):
        from .App import func
        existing_vision = database.query(self.Fieldvision).filter(self.Fieldvision.vision_name == self.vision_name).first()
        if existing_vision:
             
            return {"msg": "Уже создано"}
        max_id = database.query(func.max(self.Fieldvision.id)).scalar() or 0
        new_id = max_id + 1
        new_vision = self.Fieldvision(id=new_id, vision_name=self.vision_name)
        database.add(new_vision)
        database.commit()
         
        return database.query(self.Fieldvision).filter(self.Fieldvision.vision_name == self.vision_name).first()

    def remove_field_vision(self):
        existing_vision = database.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
        
        if existing_vision:
            database.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).delete()
            database.commit()
             
            return {"msg": "Удалено"}
        
         
        return {"msg": "Такой области не существует"}
    
    def find_vision_by_id(self):
        existing_vision = database.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
         
        if existing_vision:
            return existing_vision
        return {"msg": "такого vision_id не существует"}
    
    def find_all_visions(self):
        res = database.query(self.Fieldvision).all()
         
        return res
    
    