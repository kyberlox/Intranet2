from ..models import Fieldvision
from .App import db


#!!!!!!!!!!!!!!!
from ....services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class FieldvisionModel:
    def __init__(self, vision_name: str = '', id: int = 0):
        self.session = db
        self.vision_name = vision_name
        self.id = id
        self.Fieldvision = Fieldvision

    def add_field_vision(self):
        existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.vision_name == self.vision_name).first()
        if existing_vision:
            self.session.close()
            return {"msg": "Уже создано"}
        
        new_vision = self.Fieldvision(vision_name=self.vision_name)
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