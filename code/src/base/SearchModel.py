from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers

from src.base.pSQLmodels import UserModel
from src.base.pSQLmodels import DepartmentModel
from src.base.pSQLmodels import UsDepModel

import json

from fastapi import APIRouter, Body

search_router = APIRouter(prefix="/elastic", tags=["Поиск по тексту"])

elastic_client = Elasticsearch('http://elastic:9200')


class UserSearchModel:
    def __init__(self):
        self.UserModel = UserModel
        self.index = 'user'

    def create_index(self):
        request_body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "GOD_PLEASE": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemming",
                                "myngram"
                            ]
                        },
                        "GOD_PLEASE_FUZZY": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase"
                            ]
                        }
                        # "fio_analyzer": {
                        #     "type": "custom",
                        #     "tokenizer": "standard",
                        #     "filter": [
                        #         "lowercase",
                        #         "ru_stop",
                        #         "ru_stemming",
                        #     ]
                        # },
                        # "fio_search_analyzer": {
                        #     "type": "custom",
                        #     "tokenizer": "standard",
                        #     "filter": [
                        #         "lowercase",
                        #         "ru_stop",
                        #         "ru_stemming",
                        #         # "name_synonyms",
                        #         "myngram"
                        #     ]
                        # }
                    },
                    "filter": {
                        "ru_stemming": {
                            "type": "stemmer",
                            "language": "russian"
                        },
                        "ru_stop": {
                            "type": "stop",
                            "stopwords": "_russian"
                        },
                        # "name_synonyms": {
                        #     "type": "synonym",
                        #     "synonyms": [
                        #         "олег => олег, олегович",
                        #         "виктор => виктор, викторович",
                        #         "кучер => кучеренко"
                        #         # добавьте другие распространенные имена/отчества
                        #     ]
                        # },
                        "myngram": {
                            "type": "edge_ngram",
                            "min_gram": 2,
                            "max_gram": 20
                        }
                    }
                },
                "max_ngram_diff" : "20"
            },
            "mappings": {
                "properties": {
                    "user_fio": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        # "search_analyzer": "standard",
                        "fields" : {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
                    },
                    # "user_fio": {
                    #     "type": "text",
                    #     "analyzer": "fio_analyzer",
                    #     "search_analyzer": "fio_search_analyzer",
                    #     "fields" : {
                    #         "fuzzy": {
                    #             "type": "text",
                    #             "analyzer": "standard"
                    #         }
                    #     }
                    # },
                    "email": {
                        "type": "text"
                    },
                    "phone": {
                        "type": "text"
                    },
                    "city": {
                        "type": "text"
                    },
                    "male": {
                        "type": "text"
                    },
                    "birthday": {
                        "type": "text"
                    },
                    "work_phone": {
                        "type": "text"
                    },
                    "work_position": {
                        "type": "text"
                    },
                    "work_office": {
                        "type": "text"
                    }
                }
            }
        }

        responce = elastic_client.indices.create(index=self.index, body=request_body)
        return responce


    def dump(self):
        self.delete_index()
        self.create_index() # создаем индекс перед dump-ом / ВОпрос: надо ли удалять предыдущий индекс на вский случай ?
        # print(self.create_index())
        users_data = self.UserModel().all()
        users_data_ES = []
        for user in users_data:

            important_list = ['email', 'personal_mobile', 'personal_city', 'personal_gender', 'personal_birthday', 'uf_phone_inner', "indirect_data"]

            data = user.__dict__
            # birth = f'{data['personal_birthday']}' 'work_position', 'uf_usr_1586854037086'
            if data['second_name'] is None:
                fio = f'{data['last_name']} {data['name']}'
            else:
                fio = f'{data['last_name']} {data['name']} {data['second_name']}'

        
            data_row = {"user_fio": fio}
            for param in important_list:
                if param in data.keys():
                    if param == 'indirect_data':
                        indirect_elem = data[param]
                        if "work_position" in indirect_elem.keys() and "uf_usr_1586854037086" in indirect_elem.keys():
                            data_row["work_position"] = indirect_elem["work_position"]
                            data_row["work_office"] = indirect_elem["uf_usr_1586854037086"]
                        else:
                            pass
                    elif param == 'uf_phone_inner':
                        data_row["work_phone"] = data[param]
                    else:
                        data_row[param] = data[param]
                else:
                    continue
            
            # second_row = {
            #     "user_fio":fio, "email":data['email'], "phone":data['personal_mobile'], 
            #     "city":data['personal_city'], "male":data['personal_gender'], "birthday":birth, "work_phone": data['uf_phone_inner'],
            #     "work_position": data['work_position'], "work_office": data['uf_usr_1586854037086']
            #     }

            user_id = int(data['id'])
            
            user_action = {
                "_index": self.index,
                "_op_type": "index", # либо create либо index че выбрать хз пока
                "_id": user_id,
                "_source": data_row
            }
            users_data_ES.append(user_action)
        
        helpers.bulk(elastic_client, users_data_ES)

        return {"status": True}

    def search(self, data):
        #сюда приходит словарь для поискового запроса по пользователям
        pass

    def show(self):
        #вывести по иерархии
        pass

    def search_by_name(self, name):
        res = elastic_client.search(
            index='user',
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "user_fio": {
                                    "query": name,
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "match": {
                                "user_fio.fuzzy": {
                                    "query": name,
                                    "fuzziness": "AUTO",  
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=1000
        )

        return res['hits']['hits']

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}


class StructureSearchModel:
    def  __init__ (self):
        self.DepartmentModel = DepartmentModel
        self.UsDepModel = UsDepModel
        self.UserModel = UserModel
        self.index = 'departs'

    def create_index(self):
        request_body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "GOD_PLEASE": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemming",
                                "myngram"
                            ]
                        },
                        "GOD_PLEASE_FUZZY": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase"
                            ]
                        }
                    },
                    "filter": {
                        "ru_stemming": {
                            "type": "stemmer",
                            "language": "russian"
                        },
                        "ru_stop": {
                            "type": "stop",
                            "stopwords": "_russian"
                        },
                        "myngram": {
                            "type": "edge_ngram",
                            "min_gram": 2,
                            "max_gram": 20
                        }
                    }
                },
                "max_ngram_diff" : "20"
            },
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields" : {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
                    },
                    "father_id": {
                        "type": "integer"
                    },
                    "user_head_id": {
                        "type": "integer"
                    },
                    "users": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer"
                            },
                            "user_fio": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE",
                                "fields" : {
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE_FUZZY"
                                    }
                                }
                            },
                            "user_position": {
                                "type": "text",
                                "search_analyzer": "standard"
                            }
                        }
                    }
                }
            }
        }

        responce = elastic_client.indices.create(index=self.index, body=request_body)
        return responce
        

    
    def dump(self):
        self.delete_index()
        self.create_index()
        users_list = []
        
        dep_data = [] # список 
        dep_sql_data = self.DepartmentModel().all()
        for dep in dep_sql_data:
            department_data = dep.__dict__
            users = self.UsDepModel(id = department_data['id']).find_user_by_dep_id() #берём id всех пользователей департамента
            if isinstance(users, list):
                for usr in users:
                    user_data = {}
                    user = self.UserModel(Id=usr).find_by_id()
                    user_data['user_id'] = user['id']

                    if user['second_name'] is not None or user['second_name'] != '':
                        user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                    else:
                        user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                    if 'work_position' in user['indirect_data'].keys() and user['indirect_data']['work_position'] != '':
                        user_data['user_position'] = user['indirect_data']['work_position']
                    else:
                        pass
       
                    users_list.append(user_data)
            else:
                pass
            
            depart = {
                "name" : department_data["name"],
                "father_id" : department_data["father_id"],
                "user_head_id" : department_data["user_head_id"],
                "users" : users_list
            }
            
            depart_data_ES = {
                "_index": self.index,
                "_op_type": "index", # либо create либо index че выбрать хз пока
                "_id": department_data['id'],
                "_source": depart
            }

            

            dep_data.append(depart_data_ES)
        helpers.bulk(elastic_client, dep_data)
        return {'status': True}

    async def index_structure_dep(department_id: str):
        # Получаем данные из PostgreSQL
        department = await DepartmentModel(self.id).find_dep_by_id()
        if "user_head_id" in department.keys() and department["user_head_id"] is not None:
            user = await UserModel(department["user_head_id"]).find_by_id()
            full_name = f"{user['second_name']} {user['name']} {user['last_name']}"
            leader = {
                "id" : user['id'],
                "name" : full_name,
                "photo_url" : user['photo_file_url']
            }
        
        user_dep_relations = UsDepModel(department['id']).find_user_by_dep_id()
        users = []
        for relation in user_dep_relations:
            #тут сложности из-за неочевидной структуры в случае когда один пользователь занимает несколько должностей
            user = await UserModel(relation).find_user_by_dep_id()
            
            full_name = f"{user['second_name']} {user['name']} {user['last_name']}"
            # position = 
            users.append({
                "id" : user['id'],
                "name" : full_name,
                # "position" : position
            })


    
    def search(self, data):
        #сюда приходит словарь для поискового запроса по пользователям
        pass

    def show(self):
        #вывести по иерархии
        pass

    def search_by_name(self, name):
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "users.user_fio": {
                                    "query": name,
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "match": {
                                "users.user_fio.fuzzy": {
                                    "query": name,
                                    "fuzziness": "AUTO",  
                                    "prefix_length": 2 
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=1000
        )

        return res['hits']['hits']

    def search_by_position(self, pos):
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "users.user_position": {
                                    "query": pos,
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "match": {
                                "users.user_position": {
                                    "query": pos,
                                    "fuzziness": "AUTO",  
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=1000
        )

        return res['hits']['hits']

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}



@search_router.get("/dump_user")
def create_data_user():
    return UserSearchModel().dump()

@search_router.get("/dump_depart")
def create_data_depart():
    return StructureSearchModel().dump()

@search_router.get("/users/search_by_name/{name}")
def search_users(name: str):
    return UserSearchModel().search_by_name(name)

@search_router.get("/departs/search_by_username/{name}")
def search_depart_users(name: str):
    return StructureSearchModel().search_by_name(name)

@search_router.get("/departs/search_by_user_position/{position}")
def search_depart_users(position: str):
    return StructureSearchModel().search_by_position(position)