from sqlalchemy.sql.expression import select

from ..models import UsDep
from .App import db



#!!!!!!!!!!!!!!!
from ....services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class UsDepModel():
    def __init__(self, id=0, user_id=0, dep_id=0):
        self.id = id
        self.user_id = user_id
        self.dep_id = dep_id
        self.us_dep = UsDep

        # Base.metadata.create_all(bind=engine)
        # SessionLocal = sessionmaker(autoflush=True, bind=engine)
        self.session = db
    
    def put_uf_depart(self, usr_dep):
        from .UserModel import UserModel
        from .DepartmentModel import DepartmentModel

        existing_user = UserModel(Id=usr_dep['id']).find_by_id()
        if existing_user and existing_user['active'] is True:
            for dep in usr_dep['depart']:
                existing_depart = DepartmentModel(Id=int(dep)).find_dep_by_id()
                #print(existing_user, existing_depart[0].__dict__)
                #print(existing_depart[0].__dict__)
                if existing_depart != []:
                    self.user_id = usr_dep['id']
                    self.dep_id = int(dep)
                    existing_note = self.find_note()
                    if not existing_note:
                        new_usdep = UsDep(user_id=usr_dep['id'], dep_id=int(dep))
                        self.session.add(new_usdep)
                        self.session.commit()
            self.session.close()
        return True

    def find_note(self):
        result =  self.session.query(UsDep).filter(UsDep.user_id == self.user_id, UsDep.dep_id == self.dep_id).first()
        self.session.close()
        return result
        

    def find_dep_by_user_id(self):
        """
        Выдает данные по департаментам пользователя
        """
        res = self.session.execute(select(self.us_dep).where(self.us_dep.user_id == self.id)).scalars().all()
        print(res)
        self.session.close()
        if res != []:
            return [res]
        else:
            return []
    
    def find_user_by_dep_id(self):
        """
        Выдает id пользователей по id департамента
        """
        users = self.session.execute(select(self.us_dep).where(self.us_dep.dep_id == self.id)).scalars().all()
        if users != []:
            res = []
            for usr in users:
                res.append(usr.user_id)
            return res
        else:
            return []
