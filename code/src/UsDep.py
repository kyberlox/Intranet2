from src.pSQLmodels import UsDepModel
from src.B24 import B24

class UsDep:
    def __init__(self, ID=0, usr_id=0, dep_id=0):
        self.ID = ID
        self.usr_id = usr_id
        self.dep_id = dep_id
    
    def get_usr_dep(self):
        b24 = B24()
        data = b24.getUsers()
        UserSQL = UsDepModel()
        
        result = dict()
        for usr in data:
            if usr['ID'] is not None:
                result[int(usr['ID'])] = usr['UF_DEPARTMENT']
        
        return UserSQL.put_uf_depart(result)
        
    def search_usdep_by_id(self):
        return UsDepModel(self.ID).find_dep_by_user_id()      