from elasticsearch import Elasticsearch
from elasticsearch import helpers

from src.base.pSQLmodels import UserModel
from src.base.pSQLmodels import DepartmentModel
from src.base.pSQLmodels import UsDepModel

import json

elastic_client = Elasticsearch('http://elastic:9200')

# request_body = {
#             "settings": {
#                 "analysis": {
#                     "analyzer": {
#                         "russian_custom": {
#                         "type": "standard",
#                         "stopwords": "_russian_",
#                         "filter": ["lowercase", "russian_morphology", "russian_stop"]
#                         }
#                     }
#                 }
#             },
#             "mappings": {
#                 "properties": {
#                     "user_fio": {
#                         "type": "text"
#                     },
#                     "email": {
#                         "type": "text"
#                     },
#                     "phone": {
#                         "type": "text"
#                     },
#                     "city": {
#                         "type": "text"
#                     },
#                     "male": {
#                         "type": "text"
#                     },
#                     "birthday": {
#                         "type": "text"
#                     },
#                 }
#             }
#         }



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
        

        return helpers.bulk(elastic_client, users_data_ES)

    def search(self, data):
        #сюда приходит словарь для поискового запроса по пользователям
        pass

    def show(self):
        #вывести по иерархии
        pass

    def search_by_name(self, name):
        # res = elastic_client.search(
        #     index='user',
        #     query={
        #         'match': {
        #             "user_fio": name,
        #         }
        #     },
        #     size=1000
        # )
        # res = elastic_client.search(
        #     index='user',
        #     query={
        #         "should"
        #     }
        # )
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
    
    def dump(self):

        global_list = []
        dep_data = [] # список 
        dep_sql_data = self.DepartmentModel().all()
        for dep in dep_sql_data:
            department_data = dep.__dict__
            
            users = self.UsDepModel(id = dep.id).find_user_by_dep_id() #берём id всех пользователей департамента

            depart = {
                "name" : department_data["name"],
                "father_id" : department_data["father_id"],
                "user_head_id" : department_data["user_head_id"],
                "users" : users
            }

            first_row = {"create": {"_index": "depart", "_id": int(department_data["id"])}}

            dep_data.append(first_row)
            dep_data.append(depart)

        with open('./src/base/dep_data.json', 'w') as file:
            for row in dep_data:
                json.dump(row, file, ensure_ascii=False)
                file.write('\n')

        #print(dep_data)
        return {'status': True}

    def search(self, data):
        #сюда приходит словарь для поискового запроса по пользователям
        pass

    def show(self):
        #вывести по иерархии
        pass

