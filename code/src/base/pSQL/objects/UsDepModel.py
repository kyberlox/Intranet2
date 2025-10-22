from sqlalchemy.sql.expression import select

from ..models.UsDep import UsDep
from .App import get_db

# from .App import AsyncSessionLocal, async_engine
import asyncio

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Пользователь-Подразделение")

db_gen = get_db()
database = next(db_gen)

class UsDepModel():
    def __init__(self, id=0, user_id=0, dep_id=0):
        self.id = id
        self.user_id = user_id
        self.dep_id = dep_id
        self.us_dep = UsDep

        # Base.metadata.create_all(bind=engine)
        # SessionLocal = sessionmaker(autoflush=True, bind=engine)
        # database = db
    
    async def put_uf_depart(self, usr_dep):
        from .UserModel import UserModel
        from .DepartmentModel import DepartmentModel

        existing_user = await UserModel(Id=usr_dep['id']).find_by_id()
        if existing_user and existing_user['active'] is True:
            for dep in usr_dep['depart']:
                existing_depart = await DepartmentModel(Id=int(dep)).find_dep_by_id()
                #print(existing_user, existing_depart[0].__dict__)
                #print(existing_depart[0].__dict__)
                if existing_depart != []:
                    self.user_id = usr_dep['id']
                    self.dep_id = int(dep)
                    existing_note = self.find_note()
                    if not existing_note:
                        new_usdep = UsDep(user_id=usr_dep['id'], dep_id=int(dep))
                        database.add(new_usdep)
                        database.commit()

        return True

    def find_note(self):
        result =  database.query(UsDep).filter(UsDep.user_id == self.user_id, UsDep.dep_id == self.dep_id).first()

        return result
        

    def find_dep_by_user_id(self):
        """
        Выдает данные по департаментам пользователя
        """
        res = database.execute(select(self.us_dep).where(self.us_dep.user_id == self.id)).scalars().all()
        if res != []:
            return [res]
        else:
            return []
    
    def find_user_by_dep_id(self):
        """
        Выдает id пользователей по id департамента
        """
        users = database.execute(select(self.us_dep).where(self.us_dep.dep_id == self.id)).scalars().all()
        if users != []:
            res = []
            for usr in users:
                res.append(usr.user_id)
            return res
        else:
            return []
