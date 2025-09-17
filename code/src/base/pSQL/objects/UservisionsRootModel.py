from ..models.UservisionsRoot import UservisionsRoot
from ..models.User import User
from ..models.Fieldvision import Fieldvision
from .App import db



#!!!!!!!!!!!!!!!
from ....services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class UservisionsRootModel:
    def __init__(self, id: int = 0, vision_id: int = 0, user_id: int = 0):
        self.session = db
        self.id = id
        self.vision_id = vision_id
        self.user_id = user_id
        
        self.UservisionsRoot = UservisionsRoot
        self.Fieldvision = Fieldvision
        self.User = User

    def upload_user_to_vision(self):
        existing_user = self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id, self.UservisionsRoot.user_id == self.user_id).first()
        if existing_user:
            return {"msg": f"пользователь {self.user_id} уже сущетсвует в данной области видимости"}
        new_user = self.UservisionsRoot(vision_id=self.vision_id, user_id=self.user_id)
        self.session.add(new_user)
        self.session.commit()
        self.session.close()
        return {"msg": "Добавлен"}
    
    def upload_users_to_vision(self, user_data):
        for user in user_data:
            existing_user = self.session.query(self.User).filter(self.User.id == user, self.User.active == True).first()
            #print
            if existing_user:
                existing_user_in_vision = self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id, UservisionsRoot.user_id == user).first()
                if existing_user_in_vision:
                    #return {"msg": f"пользователь {self.user_id} уже сущетсвует в данной области видимости"}
                    continue
                else:
                    new_user = self.UservisionsRoot(vision_id=self.vision_id, user_id=user)
                    self.session.add(new_user)
                    self.session.commit()
                    self.session.close()
        return {"status": True}
    
    def remove_user_from_vision(self):
        existing_user = self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id, self.UservisionsRoot.user_id == self.user_id).first()
        if existing_user:
            self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id, self.UservisionsRoot.user_id == self.user_id).delete()
            self.session.commit()
            self.session.close()
            return {"msg": f"пользователь {self.user_id} удален из области видимости"}
        return {"msg": f"пользователя {self.user_id} не существует в данной области видимости"}

    def remove_users_from_vision(self, user_data):
        for user in user_data:
            stmt = self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id, self.UservisionsRoot.user_id == user)
            existing_user = stmt.first()
            if existing_user:
                stmt.delete()
                self.session.commit()
            else:
                pass
        self.session.close()
        return True

    def find_users_in_vision(self):
        from .UserModel import UserModel
        result = []
        existing_vision = self.session.query(self.Fieldvision).filter(self.Fieldvision.id == self.vision_id).first()
        if existing_vision:
            users_in_vis = self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.vision_id == self.vision_id).all()
            for user in users_in_vis:
                general_info = {}
                user_info = UserModel(Id=user.user_id).find_by_id()
                if user_info['active']:
                    general_info['id'] = user_info['id']
                    # name = user_info['name'] if 'name' in user_info.keys() else ''
                    # last_name = user_info['last_name'] if 'last_name' in user_info.keys() else ''
                    # second_name = user_info['second_name'] if 'second_name' in user_info.keys() else ''
                    name = user_info['name'] if user_info['name'] else ''
                    last_name = user_info['last_name'] if user_info['last_name'] else ''
                    second_name = user_info['second_name'] if user_info['second_name'] else ''
                    print(type(name), type(last_name), type(second_name))
                    general_info['name'] = last_name + ' ' + name + ' ' + second_name
                    general_info['depart'] = user_info['indirect_data']['uf_department'][0] if 'uf_department' in user_info['indirect_data'].keys() else None
                    general_info['depart_id'] = user_info['indirect_data']['uf_department_id'][0] if 'uf_department_id' in user_info['indirect_data'].keys() else None
                    if 'work_position' in user_info['indirect_data'].keys():
                        general_info['post'] = user_info['indirect_data']['work_position']
                    general_info['image'] = user_info['photo_file_url'] if 'photo_file_url' in user_info.keys() else None
                    result.append(general_info)
            return result
        return False

    def remove_depart_in_vision(self, dep_id):
        users = self.find_users_in_vision()
        if users:
            for user in users:
                if user['depart_id'] == dep_id:
                    self.session.query(self.UservisionsRoot).filter(self.UservisionsRoot.user_id == user['id']).delete()
                    self.session.commit()
                    self.session.close()
            return True
        self.session.close()
        return False