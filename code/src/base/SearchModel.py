from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers

from src.base.pSQLmodels import UserModel
from src.base.pSQLmodels import DepartmentModel
from src.base.pSQLmodels import UsDepModel
from src.base.pSQLmodels import ArticleModel
from src.model.File import File

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
                "max_ngram_diff": "20"
            },
            "mappings": {
                "properties": {
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
                    "email": {
                        "type": "text"
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
                    "indirect_data": {
                        "type": "nested",
                        "dynamic": "true"
                    },
                    "usr_photo": {
                        "type": "text"
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

        responce = elastic_client.indices.create(index=self.index, body=request_body)
        return responce

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
                                data_row[param] = f"http://intranet.emk.org.ru{file_inf['URL']}"
                            else:
                                data_row[param] = data[param]
                        else:
                            continue

                    user_id = int(data['id'])

                    elastic_client.index(index=self.index, id=user_id, body=data_row)

        return {"status": True}

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

    def search_model(self, jsn):
        res = elastic_client.search(
            index=self.index,
            query=jsn
            )
        return res['hits']['hits']
    
    def search_indirect(self, key_word):
        res = elastic_client.search(
            index=self.index,
            query={
                "nested": {
                    "path": "indirect_data",
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {"indirect_data.work_position": key_word}},
                                {"match": {"indirect_data.uf_usr_1705744824758": key_word}}
                            ]
                        }
                    }
                }
            }
        )
        return res['hits']['hits']

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}


class StructureSearchModel:
    def __init__(self):
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
                "max_ngram_diff": "20"
            },
            "mappings": {
                "properties": {
                    "join_field": {
                        "type": "join",
                        "relations": {
                            "department": "section_of_theese_depart"
                        }
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
                    },
                    "dep_id_for_sort": {
                        "type": "integer"
                    },
                    "user_head_id": {
                        "type": "integer"
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
                                "search_analyzer": "standard",
                                "fields": {
                                    "fuzzy": {
                                        "type": "text",
                                        "analyzer": "GOD_PLEASE_FUZZY"
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

        list_for_deps = []

        dep_data = []  # список
        dep_sql_data = self.DepartmentModel().all()
        for dep in dep_sql_data:
            users_list = []
            department_data = dep.__dict__
            list_for_deps.append(department_data['id'])
            users = self.UsDepModel(
                id=department_data['id']).find_user_by_dep_id()  # берём id всех пользователей департамента
            if isinstance(users, list):
                for usr in users:
                    user_data = {}
                    user = self.UserModel(Id=usr).find_by_id()
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

                        users_list.append(user_data)
                    else:
                        pass
            else:
                pass
            depart = {
                "join_field": {"name": "department", "parent": department_data["father_id"]},
                # поле "name" забиваем "department"
                # если этот департамент чей-то родитель и "section_of_theese_depart" если он ребеноки подотделов больше нет
                "name": department_data["name"],
                "dep_id_for_sort": department_data['id'],
                "user_head_id": department_data["user_head_id"],
                "users": users_list
            }

            elastic_client.index(index=self.index, id=department_data['id'], body=depart)

        return {'status': True}

    async def index_structure_dep(department_id: str):
        # Получаем данные из PostgreSQL
        department = await DepartmentModel(self.id).find_dep_by_id()
        if "user_head_id" in department.keys() and department["user_head_id"] is not None:
            user = await UserModel(department["user_head_id"]).find_by_id()
            full_name = f"{user['second_name']} {user['name']} {user['last_name']}"
            leader = {
                "id": user['id'],
                "name": full_name,
                "photo_url": user['photo_file_url']
            }

        user_dep_relations = UsDepModel(department['id']).find_user_by_dep_id()
        users = []
        for relation in user_dep_relations:
            # тут сложности из-за неочевидной структуры в случае когда один пользователь занимает несколько должностей
            user = await UserModel(relation).find_user_by_dep_id()

            full_name = f"{user['second_name']} {user['name']} {user['last_name']}"
            # position = 
            users.append({
                "id": user['id'],
                "name": full_name,
                # "position" : position
            })

    def search_by_username(self, name):
        res = elastic_client.search(
            index=self.index,
            query={
                "nested": {
                    "path": "users",
                    "query": {
                        "match": {
                            "users.user_fio": name
                        }
                    },
                    "inner_hits": {}
                }
            },
            size=10
        )
        return res['hits']['hits']

    def search_by_position(self, pos):
        res = elastic_client.search(
            index=self.index,
            query={
                "nested": {
                    "path": "users",
                    "query": {
                        "match": {
                            "users.user_position": pos
                        }
                    },
                    "inner_hits": {}
                }
            },
            size=10
        )
        return res['hits']['hits']

    def get_structure(self):
        res = elastic_client.search(
            index=self.index,
            query={
                "match_all": {}
            },
            sort=[
                {
                    "dep_id_for_sort": {
                        "order": "asc"  # "desc" использовать если хотим по убыванию
                    }
                }
            ],
            size=1000
        )
        return res['hits']['hits']

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
                                "ru_stemming"
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
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "section_id": {
                        "type": "integer"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
                    },
                    "preview_text": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
                    },
                    "content_text": {
                        "type": "text",
                        "analyzer": "GOD_PLEASE",
                        "fields": {
                            "fuzzy": {
                                "type": "text",
                                "analyzer": "GOD_PLEASE_FUZZY"
                            }
                        }
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
        for art in article_SQL_data:
            data_row = {}
            article_data = art.__dict__
            if article_data['active']:
                preview_photo = None
                #обработка превью
                files = File(art_id = article_data['id']).get_files_by_art_id()
                for file in files:
                    if file["is_preview"]:
                        url = file["file_url"]
                        #внедряю компрессию
                        if article_data['section_id'] == "18": #отдельный алгоритм для памятки новому сотруднику
                            preview_link = url.split("/")
                            preview_link[-2] = "compress_image/yowai_mo"
                            url = '/'.join(preview_link)
                        else:
                            preview_link = url.split("/")
                            preview_link[-2] = "compress_image"
                            url = '/'.join(preview_link)
                        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
                        preview_photo = f"http://intranet.emk.org.ru{url}"
                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                #находим любую картинку, если она есть
                for file in files:
                    if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                        url = file["file_url"]
                        #внедряю компрессию
                        if article_data['section_id'] == "18": #отдельный алгоритм для памятки новому сотруднику
                            preview_link = url.split("/")
                            preview_link[-2] = "compress_image/yowai_mo"
                            url = '/'.join(preview_link)
                        else:
                            preview_link = url.split("/")
                            preview_link[-2] = "compress_image"
                            url = '/'.join(preview_link)
                        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
                        preview_photo = f"http://intranet.emk.org.ru{url}"
                
                data_row["section_id"] = article_data["section_id"]
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

    def search_by_title(self, words):
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "title": {
                                    "query": words,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "wildcard": {
                                "title": {
                                    "value": f"{words}*",
                                    "case_insensitive": True
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=100
        )

        return res['hits']['hits']

    def search_by_preview(self, preview):
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "preview_text": {
                                    "query": preview,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "wildcard": {
                                "preview_text": {
                                    "value": f"{preview}*",
                                    "case_insensitive": True
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=100
        )

        return res['hits']['hits']

    def search_by_text(self, text):
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "content_text": {
                                    "query": text,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "wildcard": {
                                "content_text": {
                                    "value": f"{text}*",
                                    "case_insensitive": True
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=100
        )

        return res['hits']['hits']
        res = elastic_client.search(
            index=self.index,
            query={
                "bool": {
                    "should": [
                        {
                            "match": {
                                "content_text": {
                                    "query": text,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                    # "boost": 2  
                                }
                            }
                        },
                        {
                            "wildcard": {
                                "content_text": {
                                    "value": f"{text}*",
                                    "case_insensitive": True
                                    # "prefix_length": 2,  
                                    # "boost": 1
                                }
                            }
                        }
                    ]
                }
            },
            size=100
        )

        return res['hits']['hits']

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}



def search_everywhere(key_word):
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
                                        "multi_match": {
                                            "query": key_word,
                                            "fields": ["title", "preview_text", "content_text"]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "bool": {
                                "must": [
                                    {"terms": {"_index": ["user"]}},
                                    {
                                        "bool": {
                                            "should": [
                                                {
                                                    "multi_match": {
                                                        "query": key_word,
                                                        "fields": ["user_fio", "email", "uf_phone_inner"]
                                                    }
                                                },
                                                {
                                                    "nested": {
                                                        "path": "indirect_data",
                                                        "query": {
                                                            "multi_match": {
                                                                "query": key_word,
                                                                "fields": [
                                                                    "indirect_data.work_position",
                                                                    "indirect_data.uf_usr_1705744824758",
                                                                    "indirect_data.uf_usr_1586854037086",
                                                                    "indirect_data.uf_usr_1696592324977"
                                                                ]
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
            }
        },
        size=10
    )
    users = []
    articles = []
    for res_info in res['hits']['hits']:
        if res_info["_index"] == 'user':
            user_info = {}
            user_info['name'] = res_info["_source"]["user_fio"]
            user_info['href'] = "userPage"
            user_info['id'] = int(res_info["_id"])
            user_info['image'] = res_info["_source"]["photo_file_id"]
            users.append(user_info)
        elif res_info["_index"] == 'articles':
            art_info = {}
            art_info['name'] = res_info["_source"]["title"]
            art_info['href'] = res_info["_source"]["section_id"]
            art_info['id'] = int(res_info["_id"])
            art_info['image'] = res_info["_source"]["preview_photo"]
            articles.append(art_info)
    sec_user = {}
    sec_art = {}
    sec_user['section'] = 'Пользователи'
    sec_user['content'] = users
    sec_art['section'] = 'Контент'
    sec_art['content'] = articles
    result.append(sec_user)
    result.append(sec_art)

    return result