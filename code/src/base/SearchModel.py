from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers

from src.base.pSQLmodels import UserModel
from src.base.pSQLmodels import DepartmentModel
from src.base.pSQLmodels import UsDepModel
from src.base.pSQLmodels import ArticleModel
from src.model.File import File

import json

from typing import Optional

from fastapi import APIRouter, Body
from fastapi import HTTPException

import os
from dotenv import load_dotenv

load_dotenv()


pswd = os.getenv('pswd')
DOMAIN = os.getenv('HOST')

search_router = APIRouter(prefix="/elastic", tags=["Поиск по тексту"])

'''
elastic_client = Elasticsearch(
    hosts=[f"{DOMAIN[:-5]}:9200"],
    #basic_auth=('elastic', pswd),
    verify_certs=False,
    request_timeout=30,
    retry_on_timeout=True,
    max_retries=3
)
'''

elastic_client = Elasticsearch(hosts=["http://elasticsearch:9200"], verify_certs=False)

if elastic_client.ping():
    print("✅ Успешное подключение!")
else:
    print("❌ Ошибка аутентификации!")

with open('./src/base/sections.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

class UserSearchModel:
    def __init__(self):
        self.UserModel = UserModel
        self.index = 'user'

    def create_index(self):
        mapping = {
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
                        },
                        "GOD_PLEASE_FUZZY_V2": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stemming"
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
                            "max_gram": 7
                        }
                    }
                },
                "max_ngram_diff": "7"
            },
            "mappings": {
                "properties": {
                    "user_fio": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE_FUZZY_V2",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE"
                            }
                        }
                    },
                    "email": {
                        "type": "text",
                        "fields": {
                            "keyword": { "type": "keyword" }
                        }
                    },
                    "phone": {
                        "type": "integer"
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
                        "type": "integer"
                    },
                    "photo_file_id": {
                        "type": "text"
                    },
                    "indirect_data": {
                        "type": "nested",
                        "dynamic": "true",
                        "properties": {
                            "work_position": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            },
                            "uf_usr_1696592324977": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "keyword": { "type": "keyword" },
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            },
                            "uf_usr_1705744824758": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "keyword": { "type": "keyword" },
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            },
                            "uf_usr_1707225966581": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "keyword": { "type": "keyword" },
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            },
                            "uf_usr_1586853958167": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "keyword": { "type": "keyword" },
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            },
                            "uf_usr_department_main": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY_V2",
                                "fields": {
                                    "keyword": { "type": "keyword" },
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE"
                                    }
                                }
                            }
                        }
                    }

                },
                "dynamic_templates": [
                    {
                        "nested_string_values": {
                            "path_match": "indirect_data.*",
                            "match_mapping_type": "string",
                            "mapping": {
                                "type": "text"
                            }
                        }
                    },
                    {
                        "integer_values": {
                            "match_mapping_type": "long",
                            "path_match": "indirect_data.*",
                            "mapping": {
                                "type": "float",
                                "ignore_malformed": "true"
                            }
                        }
                    },
                    {
                        "boolean_values": {
                            "match_mapping_type": "boolean",
                            "path_match": "indirect_data.*",
                            "mapping": {
                                "type": "boolean",
                                "ignore_malformed": "true"
                            }
                        }
                    },
                    {
                        "date_values": {
                            "match_mapping_type": "date",
                            "path_match": "indirect_data.*",
                            "mapping": {
                                "type": "date",
                                "ignore_malformed": "true"
                            }
                        }
                    }
                ]
            }
        }
        print("Я тут!")
        index_name = self.index
        try:
            if elastic_client.indices.exists(index=index_name):
                # Обновляем маппинг существующего индекса
                elastic_client.indices.put_mapping(index=index_name, body=mapping["mappings"])
                return {"status": "updated", "message": f"Mapping for {index_name} updated"}
            else:
                elastic_client.indices.create(index=index_name, body=mapping)
                return {"status": "created", "message": f"Index {index_name} created"}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Index operation failed: {str(e)}"
            )

    def dump(self):
        try:
            self.delete_index()
        except:
            pass
        self.create_index()  # создаем индекс перед dump-ом / ВОпрос: надо ли удалять предыдущий индекс на вский случай ?
        
        users_data = self.UserModel().all()
        users_data_ES = []
        for user in users_data:
            
            important_list = ['email', 'personal_mobile', 'personal_city', 'personal_gender', 'personal_birthday',
                            'uf_phone_inner', "indirect_data", "photo_file_id"]

            data = user.__dict__
            if data['id'] == 1:
                pass
            else:
                if data['active']:
                    if data['second_name'] is None:
                        fio = f'{data['last_name']} {data['name']}'
                    else:
                        fio = f'{data['last_name']} {data['name']} {data['second_name']}'
                    data_row = {"user_fio": fio}
                    for param in important_list:
                        if param in data.keys():
                            if param == "photo_file_id" and data['photo_file_id'] is not None:
                                file_inf = File(data['photo_file_id']).get_users_photo()
                                data_row[param] = f"{DOMAIN}{file_inf['URL']}"
                            else:
                                data_row[param] = data[param]
                        else:
                            continue

                    user_id = int(data['id'])

                    elastic_client.index(index=self.index, id=user_id, body=data_row)

        return {"status": True}

    # def search_by_name(self, name):
    #     res = elastic_client.search(
    #         index='user',
    #         query={
    #             "bool": {
    #                 "should": [
    #                     {
    #                         "match": {
    #                             "user_fio": {
    #                                 "query": name,
    #                                 # "boost": 2  
    #                             }
    #                         }
    #                     },
    #                     {
    #                         "match": {
    #                             "user_fio.fuzzy": {
    #                                 "query": name,
    #                                 "fuzziness": "AUTO",
    #                                 # "prefix_length": 2,  
    #                                 # "boost": 1
    #                             }
    #                         }
    #                     }
    #                 ]
    #             }
    #         },
    #         size=1000
    #     )

    #     return res['hits']['hits']

    # def search_model(self, jsn):
    #     res = elastic_client.search(
    #         index=self.index,
    #         query=jsn
    #         )
    #     return res['hits']['hits']
    
    # def search_indirect(self, key_word):
    #     res = elastic_client.search(
    #         index=self.index,
    #         query={
    #             "nested": {
    #                 "path": "indirect_data",
    #                 "query": {
    #                     "bool": {
    #                         "should": [
    #                             {"match": {"indirect_data.work_position": key_word}},
    #                             {"match": {"indirect_data.uf_usr_1705744824758": key_word}}
    #                         ]
    #                     }
    #                 }
    #             }
    #         }
    #     )
    #     return res['hits']['hits']

    def elasticsearch_users(self, key_word, size_res):
        result = []
        res = elastic_client.search(
            index=self.index,
            body={
                "query": {
                    "bool": {
                        "should": [
                            {
                                "bool": {
                                    "should": [
                                        {"match": {"user_fio": {"query": key_word, "boost": 10}}},
                                        {"term": {"uf_phone_inner": {"value": key_word, "boost": 10}}},
                                        {
                                            "nested": {
                                                "path": "indirect_data",
                                                "query": {
                                                    "bool": {
                                                        "should": [
                                                            {"match": {"indirect_data.work_position": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1705744824758": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1707225966581": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1696592324977": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1586853958167": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_department_main": {"query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1586854037086": {"query": key_word, "boost": 5}}}
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    ],
                                    "_name": "true_search"
                                }
                            },
                            {
                                "multi_match": {
                                    "query": key_word,
                                    "fields": ["user_fio.fuzzy"],
                                    "fuzziness": "AUTO",
                                    "boost": 2  
                                }
                            },
                            {
                                "nested": {
                                    "path": "indirect_data",
                                    "query": {
                                        "multi_match": {
                                            "query": key_word,
                                            "fields": [
                                                "indirect_data.work_position.fuzzy",
                                                "indirect_data.uf_usr_1705744824758.fuzzy",
                                                "indirect_data.uf_usr_1707225966581.fuzzy",
                                                "indirect_data.uf_usr_1696592324977.fuzzy",
                                                "indirect_data.uf_usr_1586853958167.fuzzy",
                                                "indirect_data.uf_usr_department_main.fuzzy",
                                                "indirect_data.uf_usr_1586854037086.fuzzy"
                                            ],
                                            "fuzziness": "AUTO",
                                            "boost": 1
                                        }
                                    },
                                    "score_mode": "max"
                                }
                            }
                        ]
                    }
                },
                "size": size_res
            }
        )
        users = []
        true_search_flag = False
        
        for res_info in res['hits']['hits']:
            if "matched_queries" in res_info.keys():
                true_search_flag = True
            #print(res_info)
            user_info = {}
            user_info['name'] = res_info["_source"]["user_fio"]
            user_info['sectionHref'] = "userPage"
            user_info['id'] = int(res_info["_id"])
            user_info['image'] = res_info["_source"]["photo_file_id"]
            users.append(user_info)
        
        sec_user = {}
        sec_user['section'] = 'Пользователи'
        if true_search_flag is False:
            sec_user['msg'] = 'Точных совпадений не нашлось, возможно вы имели ввиду:'
        sec_user['content'] = users
        result.append(sec_user)
        return result  #result  res['hits']['hits'] 



    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}


class StructureSearchModel:
    def __init__(self):
        #self.DepartmentModel = DepartmentModel
        #self.UsDepModel = UsDepModel
        #self.UserModel = UserModel
        self.index = 'departs'

    def create_index(self):
        request_body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "GOD_PLEASE_FUZZY": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemming",
                                "myngram"
                            ]
                        },
                        "GOD_PLEASE": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stemming"
                            ]
                        },
                        "DEPART__FILTER": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemming"
                            ]
                        },
                        "id_depart": {
                            "type": "custom",
                            "tokenizer": "path_tokenizer"
                        }
                    },
                    "tokenizer": {
                        "path_tokenizer": {
                        "type": "pattern",
                        "pattern": "\\."
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
                            "max_gram": 7
                        }
                    }
                },
                "max_ngram_diff": "10"
            },
            "mappings": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "DEPART__FILTER"
                            }
                        }
                    },
                    "user_head_id": {
                        "type": "integer"
                    },
                    "father_id": {
                        "type": "integer"
                    },
                    "path_depart": {
                        "type": "text",
                        "analyzer": "id_depart"
                    },
                    "users": {
                        "type": "nested",  # изменили тип с object
                        "properties": {
                            "user_id": {
                                "type": "integer"
                            },
                            "user_fio": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE",
                                "fields": {
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE_FUZZY"
                                    }
                                }
                            },
                            "user_position": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE",
                                "fields": {
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "DEPART__FILTER"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        responce = elastic_client.indices.create(index=self.index, body=request_body)
        return responce

    def dump(self):
        try:
            self.delete_index()
        except:
            pass
        self.create_index()

        #list_for_deps = []
        dep_data_ES = [] # список для bulk
        dep_data = {}  # словарь для данных
        usr_sql_data = UserModel().all()
        
        """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления верхушки айсберга⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
        # находим верхушку айсберга, ее father_id будет None
        #list_children = DepartmentModel().find_deps_by_father_id(53)
        N_0 = DepartmentModel().find_deps_by_father_id(None)[0]
        path_N_0_depart = str(N_0.id) # путь для департамента
        dep_data['id'] = N_0.id
        dep_data['name'] = N_0.name
        dep_data['user_head_id'] = N_0.user_head_id
        dep_data['father_id'] = N_0.father_id
        dep_data['path_depart'] = path_N_0_depart
        """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
        users_list = []
        users = UsDepModel(id=N_0.id).find_user_by_dep_id()  # берём id всех пользователей департамента
        if isinstance(users, list):
            for usr in usr_sql_data:
                user = usr.__dict__
                if user['id'] in users:
                    user_data = {}
                    if user['active'] is True:
                        user_data['user_id'] = user['id']

                        if user['second_name'] is not None or user['second_name'] != '':
                            user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                        else:
                            user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                        if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                            'work_position'] != '':
                            user_data['user_position'] = user['indirect_data']['work_position']
                        else:
                            pass

                        if user['photo_file_id']:
                            photo_inf = File(id=user['photo_file_id']).get_users_photo()
                            url = photo_inf['URL']
                            user_data['photo'] = f"{DOMAIN}{url}"
                            print(DOMAIN)
                            print(pswd)
                        else:
                            user_data['photo'] = None

                        users_list.append(user_data)
        """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
        dep_data['users'] = users_list
        

        data_action = {
                    "_index": self.index,
                    "_op_type": "index",
                    "_id": N_0.id,
                    "_source": dep_data
        }
        dep_data_ES.append(data_action)
        """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
        #print(dep_data_ES) 
        """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления первого разветвления⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
        N_1_list = DepartmentModel().find_deps_by_father_id(N_0.id)
        for N_1 in N_1_list:
            path_N_1_depart = str(N_1.id)
            dep_data = {}
            dep_data['id'] = N_1.id
            dep_data['name'] = N_1.name
            dep_data['user_head_id'] = N_1.user_head_id
            dep_data['father_id'] = N_1.father_id
            dep_data['path_depart'] = path_N_0_depart + '.' + path_N_1_depart
            """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
            users_list = []
            users = UsDepModel(id=N_1.id).find_user_by_dep_id()  # берём id всех пользователей департамента
            if isinstance(users, list):
                for usr in usr_sql_data:
                    user = usr.__dict__
                    if user['id'] in users:
                        user_data = {}
                        if user['active'] is True:
                            user_data['user_id'] = user['id']

                            if user['second_name'] is not None or user['second_name'] != '':
                                user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                            else:
                                user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                            if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                'work_position'] != '':
                                user_data['user_position'] = user['indirect_data']['work_position']
                            else:
                                pass
                            if user['photo_file_id']:
                                photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                url = photo_inf['URL']
                                user_data['photo'] = f"{DOMAIN}{url}"
                            else:
                                user_data['photo'] = None

                            users_list.append(user_data)
            """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
            dep_data['users'] = users_list
            data_action = {
                    "_index": self.index,
                    "_op_type": "index",
                    "_id": N_1.id,
                    "_source": dep_data
            }
            dep_data_ES.append(data_action)
            #второе разветвление
            N_2_list = DepartmentModel().find_deps_by_father_id(N_1.id)
            if N_2_list == []:
                continue
            else:
                for N_2 in N_2_list:
                    path_N_2_depart = str(N_2.id)
                    dep_data = {}
                    dep_data['id'] = N_2.id
                    dep_data['name'] = N_2.name
                    dep_data['user_head_id'] = N_2.user_head_id
                    dep_data['father_id'] = N_2.father_id
                    dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart
                    """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                    users_list = []
                    users = UsDepModel(id=N_2.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                    if isinstance(users, list):
                        for usr in usr_sql_data:
                            user = usr.__dict__
                            if user['id'] in users:
                                user_data = {}
                                if user['active'] is True:
                                    user_data['user_id'] = user['id']

                                    if user['second_name'] is not None or user['second_name'] != '':
                                        user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                    else:
                                        user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                    if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                        'work_position'] != '':
                                        user_data['user_position'] = user['indirect_data']['work_position']
                                    else:
                                        pass
                                    
                                    if user['photo_file_id']:
                                        photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                        url = photo_inf['URL']
                                        user_data['photo'] = f"{DOMAIN}{url}"
                                    else:
                                        user_data['photo'] = None

                                    users_list.append(user_data)
                    """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                    dep_data['users'] = users_list
                    data_action = {
                            "_index": self.index,
                            "_op_type": "index",
                            "_id": N_2.id,
                            "_source": dep_data
                    }
                    dep_data_ES.append(data_action)

                    #третье разветвление
                    N_3_list = DepartmentModel().find_deps_by_father_id(N_2.id)
                    if N_3_list == []:
                        continue
                    else:
                        for N_3 in N_3_list:
                            path_N_3_depart = str(N_3.id)
                            dep_data = {}
                            dep_data['id'] = N_3.id
                            dep_data['name'] = N_3.name
                            dep_data['user_head_id'] = N_3.user_head_id
                            dep_data['father_id'] = N_3.father_id
                            dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart + '.' + path_N_3_depart
                            """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                            users_list = []
                            users = UsDepModel(id=N_3.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                            if isinstance(users, list):
                                for usr in usr_sql_data:
                                    user = usr.__dict__
                                    if user['id'] in users:
                                        user_data = {}
                                        if user['active'] is True:
                                            user_data['user_id'] = user['id']

                                            if user['second_name'] is not None or user['second_name'] != '':
                                                user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                            else:
                                                user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                            if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                'work_position'] != '':
                                                user_data['user_position'] = user['indirect_data']['work_position']
                                            else:
                                                pass
                                            
                                            if user['photo_file_id']:
                                                photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                                url = photo_inf['URL']
                                                user_data['photo'] = f"{DOMAIN}{url}"
                                            else:
                                                user_data['photo'] = None

                                            users_list.append(user_data)
                            """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                            dep_data['users'] = users_list
                            data_action = {
                                    "_index": self.index,
                                    "_op_type": "index",
                                    "_id": N_3.id,
                                    "_source": dep_data
                            }
                            dep_data_ES.append(data_action)
                            N_4_list = DepartmentModel().find_deps_by_father_id(N_3.id)
                            if N_4_list == []:
                                continue
                            else:
                                for N_4 in N_4_list:
                                    path_N_4_depart = str(N_4.id)
                                    dep_data = {}
                                    dep_data['id'] = N_4.id
                                    dep_data['name'] = N_4.name
                                    dep_data['user_head_id'] = N_4.user_head_id
                                    dep_data['father_id'] = N_4.father_id
                                    dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart + '.' + path_N_3_depart + '.' + path_N_4_depart
                                    """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                                    users_list = []
                                    users = UsDepModel(id=N_4.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                    if isinstance(users, list):
                                        for usr in usr_sql_data:
                                            user = usr.__dict__
                                            if user['id'] in users:
                                                user_data = {}
                                                if user['active'] is True:
                                                    user_data['user_id'] = user['id']

                                                    if user['second_name'] is not None or user['second_name'] != '':
                                                        user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                                    else:
                                                        user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                                    if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                        'work_position'] != '':
                                                        user_data['user_position'] = user['indirect_data']['work_position']
                                                    else:
                                                        pass

                                                    if user['photo_file_id']:
                                                        photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                                        url = photo_inf['URL']
                                                        user_data['photo'] = f"{DOMAIN}{url}"
                                                    else:
                                                        user_data['photo'] = None

                                                    users_list.append(user_data)
                                    """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                                    dep_data['users'] = users_list
                                    data_action = {
                                            "_index": self.index,
                                            "_op_type": "index",
                                            "_id": N_4.id,
                                            "_source": dep_data
                                    }
                                    dep_data_ES.append(data_action)
                                    N_5_list = DepartmentModel().find_deps_by_father_id(N_4.id)
                                    if N_5_list == []:
                                        continue
                                    else:
                                        for N_5 in N_5_list:
                                            path_N_5_depart = str(N_5.id)
                                            dep_data = {}
                                            dep_data['id'] = N_5.id
                                            dep_data['name'] = N_5.name
                                            dep_data['user_head_id'] = N_5.user_head_id
                                            dep_data['father_id'] = N_5.father_id
                                            dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart + '.' + path_N_3_depart + '.' + path_N_4_depart + '.' + path_N_5_depart
                                            """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                                            users_list = []
                                            users = UsDepModel(id=N_5.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                            if isinstance(users, list):
                                                for usr in usr_sql_data:
                                                    user = usr.__dict__
                                                    if user['id'] in users:
                                                        user_data = {}
                                                        if user['active'] is True:
                                                            user_data['user_id'] = user['id']

                                                            if user['second_name'] is not None or user['second_name'] != '':
                                                                user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                                            else:
                                                                user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                                            if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                                'work_position'] != '':
                                                                user_data['user_position'] = user['indirect_data']['work_position']
                                                            else:
                                                                pass
                                                                
                                                            if user['photo_file_id']:
                                                                photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                                                url = photo_inf['URL']
                                                                user_data['photo'] = f"{DOMAIN}{url}"
                                                            else:
                                                                user_data['photo'] = None

                                                            users_list.append(user_data)
                                            """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                                            dep_data['users'] = users_list
                                            data_action = {
                                                    "_index": self.index,
                                                    "_op_type": "index",
                                                    "_id": N_5.id,
                                                    "_source": dep_data
                                            }
                                            dep_data_ES.append(data_action)
                                            N_6_list = DepartmentModel().find_deps_by_father_id(N_5.id)
                                            if N_6_list == []:
                                                continue
                                            else:
                                                for N_6 in N_6_list:
                                                    path_N_6_depart = str(N_6.id)
                                                    dep_data = {}
                                                    dep_data['id'] = N_6.id
                                                    dep_data['name'] = N_6.name
                                                    dep_data['user_head_id'] = N_6.user_head_id
                                                    dep_data['father_id'] = N_6.father_id
                                                    dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart + '.' + path_N_3_depart + '.' + path_N_4_depart + '.' + path_N_5_depart + '.' + path_N_6_depart
                                                    """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                                                    users_list = []
                                                    users = UsDepModel(id=N_6.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                                    if isinstance(users, list):
                                                        for usr in usr_sql_data:
                                                            user = usr.__dict__
                                                            if user['id'] in users:
                                                                user_data = {}
                                                                if user['active'] is True:
                                                                    user_data['user_id'] = user['id']

                                                                    if user['second_name'] is not None or user['second_name'] != '':
                                                                        user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                                                    else:
                                                                        user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                                                    if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                                        'work_position'] != '':
                                                                        user_data['user_position'] = user['indirect_data']['work_position']
                                                                    else:
                                                                        pass
                                                                    
                                                                    if user['photo_file_id']:
                                                                        photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                                                        url = photo_inf['URL']
                                                                        user_data['photo'] = f"{DOMAIN}{url}"
                                                                    else:
                                                                        user_data['photo'] = None

                                                                    users_list.append(user_data)
                                                    """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                                                    dep_data['users'] = users_list
                                                    data_action = {
                                                            "_index": self.index,
                                                            "_op_type": "index",
                                                            "_id": N_6.id,
                                                            "_source": dep_data
                                                    }
                                                    dep_data_ES.append(data_action)
                                                    N_7_list = DepartmentModel().find_deps_by_father_id(N_6.id)
                                                    if N_7_list == []:
                                                        continue
                                                    else:
                                                        for N_7 in N_7_list:
                                                            path_N_7_depart = str(N_7.id)
                                                            dep_data = {}
                                                            dep_data['id'] = N_7.id
                                                            dep_data['name'] = N_7.name
                                                            dep_data['user_head_id'] = N_7.user_head_id
                                                            dep_data['father_id'] = N_7.father_id
                                                            dep_data['path_depart'] = path_N_1_depart + '.' + path_N_2_depart + '.' + path_N_3_depart + '.' + path_N_4_depart + '.' + path_N_5_depart + '.' + path_N_6_depart + '.' + path_N_7_depart
                                                            """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления юезров которые относятся к этому департаменту⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
                                                            users_list = []
                                                            users = UsDepModel(id=N_7.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                                            if isinstance(users, list):
                                                                for usr in usr_sql_data:
                                                                    user = usr.__dict__
                                                                    if user['id'] in users:
                                                                        user_data = {}
                                                                        if user['active'] is True:
                                                                            user_data['user_id'] = user['id']

                                                                            if user['second_name'] is not None or user['second_name'] != '':
                                                                                user_data['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                                                            else:
                                                                                user_data['user_fio'] = f'{user['last_name']} {user['name']}'

                                                                            if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                                                'work_position'] != '':
                                                                                user_data['user_position'] = user['indirect_data']['work_position']
                                                                            else:
                                                                                pass
                                                                            
                                                                            if user['photo_file_id']:
                                                                                photo_inf = File(id=user['photo_file_id']).get_users_photo()
                                                                                url = photo_inf['URL']
                                                                                user_data['photo'] = f"{DOMAIN}{url}"
                                                                            else:
                                                                                user_data['photo'] = None

                                                                            users_list.append(user_data)
                                                            """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                                                            dep_data['users'] = users_list
                                                            data_action = {
                                                                    "_index": self.index,
                                                                    "_op_type": "index",
                                                                    "_id": N_7.id,
                                                                    "_source": dep_data
                                                            }
                                                            dep_data_ES.append(data_action)
        helpers.bulk(elastic_client, dep_data_ES)
        return {"status": True}
        

            
        # article_action = {
        #                 "_index": self.index,
        #                 "_op_type": "index",
        #                 "_id": int(article_data['id']),
        #                 "_source": data_row
        #             }

        #     else:
        #         pass

        #     article_data_ES.append(article_action)

        # helpers.bulk(elastic_client, article_data_ES)

    def get_full_structure(self):
        result = []
        res = elastic_client.search(
            index=self.index,
            query={
                "match_all": {}
            },
            # sort=[
            #     {
            #         "id": {
            #             "order": "asc"  # "desc" использовать если хотим по убыванию
            #         }
            #     }
            # ],
            size=1000
        )
        for re in res['hits']['hits']:
            result.append(re['_source'])
        return result


    def get_structure_by_parent_id(self, parent_id=None): 
        result = []
        query = {"match": {"path_depart": parent_id}}
        res = elastic_client.search(index=self.index, query=query, size=1000)
        for re in res['hits']['hits']:
            depart = {}
            users_id = []
            depart['id'] = re['_source']['id']
            depart['name'] = re['_source']['name']
            depart['user_head_id'] = re['_source']['user_head_id']
            depart['father_id'] = re['_source']['father_id']
            # for user in re['_source']['users']:
            #     users_id.append(user['user_id'])
            # depart['users'] = users_id
            depart['users'] = re['_source']['users']
            result.append(depart)
        return result

    def get_structure_by_name(self, word):
        result = []
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {"match": {"name": {"query": word,"boost": 10}}},
                        {"multi_match": {"query": word, "fields": ["name"], "fuzziness": "AUTO", "boost": 2}}
                    ]
                }
            }
        )
        for re in res['hits']['hits']:
            depart = {}
            users_id = []
            depart['id'] = re['_source']['id']
            depart['name'] = re['_source']['name']
            depart['user_head_id'] = re['_source']['user_head_id']
            depart['father_id'] = re['_source']['father_id']
            # for user in re['_source']['users']:
            #     users_id.append(user['user_id'])
            # depart['users'] = users_id
            depart['users'] = re['_source']['users']
            result.append(depart)
        return result

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}


class ArticleSearchModel:

    def __init__(self):
        self.ArticleModel = ArticleModel
        self.index = "articles"

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
                                "lowercase",
                                "ru_stemming"
                            ]
                        },
                        "GOD_PLEASE_V2": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemming"
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
                            "max_gram": 10
                        }
                    }
                },
                "max_ngram_diff": "10"
            },
            "mappings": {
                "properties": {
                    "section_id": {
                        "type": "integer"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE_V2",
                        "term_vector": "with_positions_offsets",
                        "index_options": "offsets"
                        # "fields": {
                        #     "fuzzy": {
                        #         "type": "text",
                        #         "analyzer": "GOD_PLEASE",
                        #         "term_vector": "with_positions_offsets"
                        #     }
                        # }
                    },
                    "preview_text": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE_V2",
                        "term_vector": "with_positions_offsets",
                        "index_options": "offsets"
                        # "fields": {
                        #     "fuzzy": {
                        #         "type": "text",
                        #         "analyzer": "GOD_PLEASE",
                        #         "term_vector": "with_positions_offsets"
                        #     }
                        # }
                    },
                    "content_text": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE_V2",
                        "term_vector": "with_positions_offsets",
                        "index_options": "offsets"
                        # "fields": {
                        #     "fuzzy": {
                        #         "type": "text",
                        #         "analyzer": "GOD_PLEASE",
                        #         "term_vector": "with_positions_offsets"
                        #     }
                        # }
                    },
                    "content_type": {
                        "type": "text"
                    },
                    "preview_url": {
                        "type": "text"
                    }
                }
            }
        }
        responce = elastic_client.indices.create(index=self.index, body=request_body)
        return responce

    def dump(self):
        try:
            # в самом начале нет индекса, поэтому вылезает ошибка при первой попытке дампа
            self.delete_index()
        except:
            pass
        self.create_index()

        article_SQL_data = ArticleModel().all()
        article_data_ES = []
        article_action = {}
        for article_data in article_SQL_data:
            data_row = {}
            if article_data['active'] and article_data['section_id'] != 6 and article_data['section_id'] != 41:
                
                if isinstance(article_data['indirect_data'], str):
                    article_data['indirect_data'] = json.loads(article_data['indirect_data'])
                # if article_data['section_id'] == 16:
                #     print(article_data['id'], type(article_data['indirect_data']))
                #     article_data['indirect_data'] = json.loads(article_data['indirect_data'])

                # обрабатываем случай с интервью Еленой Земской
                if article_data['section_id']  == 16 and ("PROPERTY_1025" not in article_data['indirect_data'] or article_data['indirect_data']['PROPERTY_1025'] is None):
                    continue
                else:
                    preview_photo = None
                    #обработка превью
                    files = File(art_id = article_data['id']).get_files_by_art_id()
                    for file in files:
                        if file["is_preview"]:
                            url = file["file_url"]
                            #внедряю компрессию
                            if article_data['section_id'] == 18: #отдельный алгоритм для памятки новому сотруднику
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image/yowai_mo"
                                url = '/'.join(preview_link)
                            else:
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image"
                                url = '/'.join(preview_link)
                            
                            preview_photo = f"{DOMAIN}{url}"

                    #находим любую картинку, если она есть
                    for file in files:
                        if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                            url = file["file_url"]
                            #внедряю компрессию
                            if article_data['section_id'] == 18: #отдельный алгоритм для памятки новому сотруднику
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image/yowai_mo"
                                url = '/'.join(preview_link)
                            else:
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image"
                                url = '/'.join(preview_link)
                            
                            preview_photo = f"{DOMAIN}{url}"
                    
                    data_row["section_id"] = article_data["section_id"]
                    if article_data["section_id"] == 15:
                        data_row["authorId"] = article_data["indirect_data"]["author_uuid"]
                    data_row["title"] = article_data["name"]
                    data_row["preview_text"] = article_data["preview_text"]
                    data_row["content_text"] = article_data["content_text"]
                    data_row["content_type"] = article_data["content_type"]
                    data_row["preview_photo"] = preview_photo
                    
                    article_action = {
                        "_index": self.index,
                        "_op_type": "index",
                        "_id": int(article_data['id']),
                        "_source": data_row
                    }

            else:
                pass

            article_data_ES.append(article_action)

        helpers.bulk(elastic_client, article_data_ES)

        return {"status": True}

       
    def elasticsearch_article(self, key_word, size_res: Optional[int] = 20):
        result = []
        res = elastic_client.search(
            index=self.index,
            body={
                "query": {
                    "bool": {
                        "should": [
                            #точный поиск
                            {
                                "bool": {
                                    "should": [
                                        {"match": {"title": {"query": key_word,"boost": 10}}},
                                        {"match": {"preview_text": {"query": key_word,"boost": 8}}},
                                        {"match": {"content_text": {"query": key_word,"boost": 6}}}
                                    ],
                                    "_name": "true_search"
                                }
                            },
                            #неточный поиск
                            {
                                "multi_match": {
                                    "query": key_word,
                                    "fields": ["title", "preview_text", "content_text"],
                                    "fuzziness": "AUTO",
                                    "boost": 2  
                                }
                            }, 
                        ]
                    }
                },
                "highlight": {  
                    "type": "unified",
                    "fields": {
                        "title": {
                            "highlight_query": { 
                                "bool": {
                                    "should": [
                                        {"match": {"title": key_word}},
                                        {"match": {"title": {"query": key_word, "fuzziness": "AUTO"}}}  

                                    ]
                                }
                            }
                        },
                        "preview_text": {
                            "highlight_query": { 
                                "bool": {
                                    "should": [
                                        {"match": {"preview_text": key_word}},
                                        {"match": {"preview_text": {"query": key_word, "fuzziness": "AUTO"}}} 

                                    ]
                                }
                            }
                        },
                        "content_text": {
                            "highlight_query": { 
                                "bool": {
                                    "should": [
                                        {"match": {"content_text": key_word}},
                                        {"match": {"content_text": {"query": key_word, "fuzziness": "AUTO"}}}

                                    ]
                                }
                            }
                        }
                    }
                },
                "size": size_res
            }
        )
        articles = []
        true_search_flag = False
        
        for res_info in res['hits']['hits']:
            if "matched_queries" in res_info.keys():
                true_search_flag = True
            art_info = {}
            art_info['name'] = res_info["_source"]["title"]
            section_href = next((s.get('sectionHref') for s in sections if s['id'] == res_info["_source"]["section_id"]), res_info["_source"]["section_id"])
            art_info['sectionHref'] = section_href
            art_info['id'] = int(res_info["_id"])
            if "authorId" in res_info["_source"].keys():
                art_info['authorId'] = res_info["_source"]["authorId"]
            art_info['image'] = res_info["_source"]["preview_photo"]
            art_info['coincident'] = res_info['highlight']
            articles.append(art_info)
        
        sec_art = {}
        sec_art['section'] = 'Контент'
        if true_search_flag is False:
            sec_art['msg'] = 'Точных совпадений не нашлось, возможно вы имели ввиду:'
        
        
        sec_art['content'] = articles
        result.append(sec_art)

        return result #res['hits']['hits'] result

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}



def search_everywhere(key_word): # , size_res: Optional[int] = 40
    result = []
    res = elastic_client.search(
        index=["articles", "user"],
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {"terms": {"_index": ["articles"]}},
                                    {
                                        "bool": {
                                            "should": [
                                                #точный поиск
                                                {
                                                    "bool": {
                                                        "should": [
                                                            {"match": {"title": {"query": key_word,"boost": 10}}},
                                                            {"match": {"preview_text": {"query": key_word,"boost": 8}}},
                                                            {"match": {"content_text": {"query": key_word,"boost": 6}}}
                                                        ],
                                                        "_name": "true_search"
                                                    }
                                                },
                                                #неточный поиск
                                                {
                                                    "multi_match": {
                                                        "query": key_word,
                                                        "fields": ["title", "preview_text", "content_text"],
                                                        "fuzziness": "AUTO",
                                                        "boost": 2  
                                                    }
                                                }, 
                                            ]
                                        }
                                    }
                                    
                                ]
                            }
                        },
                        {
                        "bool": {
                            "must": [
                                {"term": {"_index": "user"}},
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "bool": {
                                                    "should": [
                                                        
                                                        {
                                                            "match": {
                                                            "user_fio": {
                                                                "query": key_word,
                                                                "boost": 10,
                                                                "_name": "true_search"
                                                            }
                                                            }
                                                        },
                                                        {"term": {"uf_phone_inner": {"value": key_word, "boost": 10}}},
                                                        {
                                                            "nested": {
                                                                "path": "indirect_data",
                                                                "query": {
                                                                    "bool": {
                                                                        "should": [
                                                                            {"match": {"indirect_data.work_position": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_1705744824758": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_1707225966581": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_1696592324977": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_1586853958167": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_department_main": {"query": key_word, "boost": 5}}},
                                                                            {"match": {"indirect_data.uf_usr_1586854037086": {"query": key_word, "boost": 5}}}
                                                                        ]
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    ],
                                                    "_name": "true_search"
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": key_word,
                                                    "fields": ["user_fio.fuzzy"],
                                                    "fuzziness": "AUTO",
                                                    "boost": 2  
                                                }
                                            },
                                            {
                                                "nested": {
                                                    "path": "indirect_data",
                                                    "query": {
                                                        "multi_match": {
                                                            "query": key_word,
                                                            "fields": [
                                                                "indirect_data.work_position.fuzzy",
                                                                "indirect_data.uf_usr_1705744824758.fuzzy",
                                                                "indirect_data.uf_usr_1707225966581.fuzzy",
                                                                "indirect_data.uf_usr_1696592324977.fuzzy",
                                                                "indirect_data.uf_usr_1586853958167.fuzzy",
                                                                "indirect_data.uf_usr_department_main.fuzzy",
                                                                "indirect_data.uf_usr_1586854037086.fuzzy"
                                                            ],
                                                            "fuzziness": "AUTO",
                                                            "boost": 1
                                                        }
                                                    },
                                                    "score_mode": "max"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        },
        "highlight": {  
            "type": "unified",
            "fields": {
                "title": {
                    "highlight_query": { 
                        "bool": {
                            "should": [
                                {"match": {"title": key_word}},
                                {"match": {"title": {"query": key_word, "fuzziness": "AUTO"}}}  

                            ]
                        }
                    }
                },
                "preview_text": {
                    "highlight_query": { 
                        "bool": {
                            "should": [
                                {"match": {"preview_text": key_word}},
                                {"match": {"preview_text": {"query": key_word, "fuzziness": "AUTO"}}} 

                            ]
                        }
                    }
                },
                "content_text": {
                    "highlight_query": { 
                        "bool": {
                            "should": [
                                {"match": {"content_text": key_word}},
                                {"match": {"content_text": {"query": key_word, "fuzziness": "AUTO"}}}

                            ]
                        }
                    }
                }
            }
        },
        "size": 1000
        }
    )
   
    users = []
    articles = []
    true_user_search_flag = False
    true_art_search_flag = False
    count_users = 0
    count_art = 0
    for res_info in res['hits']['hits']:
        if res_info["_index"] == 'user':
            count_users += 1
            if count_users <= 10:
                if "matched_queries" in res_info.keys():
                    true_user_search_flag = True
                #print(res_info)
                user_info = {}
                user_info['name'] = res_info["_source"]["user_fio"]
                user_info['sectionHref'] = "userPage"
                user_info['id'] = int(res_info["_id"])
                user_info['image'] = res_info["_source"]["photo_file_id"]
                users.append(user_info)
        elif res_info["_index"] == 'articles':
            count_art += 1
            if count_art <= 10:
                if "matched_queries" in res_info.keys():
                    true_art_search_flag = True
                art_info = {}
                art_info['name'] = res_info["_source"]["title"]
                section_href = next((s.get('sectionHref') for s in sections if s['id'] == res_info["_source"]["section_id"]), res_info["_source"]["section_id"])
                art_info['sectionHref'] = section_href
                art_info['id'] = int(res_info["_id"])
                if "authorId" in res_info["_source"].keys():
                    art_info['authorId'] = res_info["_source"]["authorId"]
                art_info['image'] = res_info["_source"]["preview_photo"]
                art_info['coincident'] = res_info['highlight']
                articles.append(art_info)
    
    sec_user = {}
    sec_art = {}
    sec_user['section'] = 'Пользователи'
    if true_user_search_flag is False:
        sec_user['msg'] = 'Точных совпадений по пользователям не нашлось, возможно вы имели ввиду:'
    sec_user['content'] = users
    sec_art['section'] = 'Контент'
    if true_art_search_flag is False:
        sec_art['msg'] = 'Точных совпадений по контенту не нашлось, возможно вы имели ввиду:'
    sec_art['content'] = articles
    result.append(sec_user)
    result.append(sec_art)
    return result    #result  res['hits']['hits'] 