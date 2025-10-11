from src.services.LogsMaker import LogsMaker
from .App import get_db, func, select
LogsMaker().ready_status_message("Успешная инициализация таблицы Области Видимости")

db_gen = get_db()
database = next(db_gen)

class FieldvisionModel:
    def __init__(self, vision_name: str = '', id: int = 0, art_id: int = 0):
        # from .App import db
        # database = db
        self.vision_name = vision_name
        self.id = id
        self.art_id = art_id

        from ..models.Fieldvision import Fieldvision
        self.Fieldvision = Fieldvision

        from ..models.ArtVis import ArtVis
        self.ArtVis = ArtVis

        from ..models.Article import Article
        self.Article = Article



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
    
    def set_art_to_vision(self):
        try:
            existing_vision = database.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
            if not existing_vision:
                return LogsMaker().info_message(f"Области видимости с id = {self.id} не сщуествует")
            
            existing_art = database.query(self.Article).filter(self.Article.id == self.art_id).first()
            if not existing_art:
                return LogsMaker().info_message(f"Статью с id = {self.id} невозможно добавить в ОВ с id = {self.id}, статьи не существует")

            max_id = database.query(func.max(self.ArtVis.id)).scalar() or 0
            new_id = max_id + 1
            new_node = self.ArtVis()
            new_node.id = new_id,
            new_node.vision_id = self.id,
            new_node.art_id = self.art_id
            database.add(new_node)
            database.commit()
            return LogsMaker().info_message(f"Статья с id = {self.id} успешно добавлена в ОВ с id = {self.id}") 
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при добавлении статьи с id = {self.art_id} в ОВ с id = {self.id}, {e}")

    def delete_art_from_vision(self):
        try:
            existing_vision = database.query(self.Fieldvision).filter(self.Fieldvision.id == self.id).first()
            if not existing_vision:
                return LogsMaker().info_message(f"Области видимости с id = {self.id} не сщуествует")
            
            existing_art = database.query(self.Article).filter(self.Article.id == self.art_id).first()
            if not existing_art:
                return LogsMaker().info_message(f"Статью с id = {self.id} невозможно удалить с ОВ с id = {self.id}, статьи не существует")

            database.query(self.ArtVis).filter(self.ArtVis.art_id == self.art_id, self.ArtVis.vision_id == self.id).delete()
            database.commit()
            return LogsMaker().info_message(f"Статья с id = {self.id} успешно удалена из ОВ с id = {self.id}") 
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении статьи с id = {self.id} из ОВ с id = {self.id}, {e}")
    
    def get_all_vis_in_art(self):
        result = []
        art_info = database.query(self.ArtVis.vision_id, self.Fieldvision.vision_name).join(self.Fieldvision, self.Fieldvision.id == self.ArtVis.vision_id).filter(self.ArtVis.art_id == self.art_id).all()
        if art_info:
            for art in art_info:
                vis_info = {
                    "id": art[0],
                    "name": art[1]
                }
                result.append(vis_info)
        return result
    
    def check_user_root(self, user_id):
        from ..models.Roots import Roots
        self.Roots = Roots

        # flag = False
        user_roots = database.query(self.Roots.root_token['VisionRoots']).filter(self.Roots.user_uuid == user_id).scalar()

        art_vis = database.scalars(select(self.ArtVis.vision_id).where(self.ArtVis.art_id == self.art_id)).all()
        if user_roots is not None and art_vis is not None:
            for user_root in user_roots:
                if user_root in art_vis:
                    return True
        return False
 