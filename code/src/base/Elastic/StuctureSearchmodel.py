from .App import elastic_client, helpers
from .App import DOMAIN




def get_info_by_obj(obj, parent_path_depart):
    from ..pSQL.objects.UsDepModel import UsDepModel
    from ..pSQL.objects.UserModel import UserModel

    if obj.id == 53:
        path_depart = "53"
    else:
        path_depart = parent_path_depart + f".{obj.id}"

    dep_data = dict()
    dep_data['id'] = obj.id
    dep_data['name'] = obj.name
    dep_data['user_head_id'] = obj.user_head_id
    dep_data['father_id'] = obj.father_id
    dep_data['path_depart'] = path_depart

    users_list = []
    
    usdep_modelo = UsDepModel()
    usdep_modelo.id =obj.id
    users = usdep_modelo.find_user_by_dep_id()  # берём id всех пользователей департамента
    if isinstance(users, list):
        for usr_id in users:
            user = UserModel(Id=usr_id).find_by_id()
            if user:
                user_data = {}
                if user['active'] is True:
                    user_data['id'] = user['id']

                    if user['second_name'] is not None or user['second_name'] != '':
                        user_data['name'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                    else:
                        user_data['name'] = f'{user['last_name']} {user['name']}'

                    if 'work_position' in user['indirect_data'].keys() and user['indirect_data']['work_position'] != '':
                        user_data['user_position'] = user['indirect_data']['work_position']
                    else:
                        pass

                    if user['photo_file_id']:
                        photo_inf = File(id=user['photo_file_id']).get_users_photo()
                        url = photo_inf['URL']
                        user_data['image'] = f"{DOMAIN}{url}"
                    else:
                        user_data['image'] = None

                    users_list.append(user_data)
            else:
                continue
    dep_data['users'] = users_list
    data_action = {
        "_index": 'departs',
        "_op_type": "index",
        "_id": obj.id,
        "_source": dep_data
    }
    return data_action


class StructureSearchModel:
    def __init__(self):
        from ..pSQL.objects.DepartmentModel import DepartmentModel
        self.DepartmentModel = DepartmentModel()

        # from ..pSQL.objects.UsDepModel import UsDepModel
        # self.UsDepModel = UsDepModel()

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

        # list_for_deps = []
        dep_data_ES = [] # список для bulk
        dep_data = {}  # словарь для данных

        parents=[]  #родители - по ним собираем
        children=[] #дети - их собираем
        parent_path_depart = dict()
        roots = dict()
        #иду по слоям
        for i in range(8):
            #первый слой - верхушка
            if i == 0:
                children.insert(i, self.DepartmentModel.find_deps_by_father_id(None)[0])
                # parent_path_depart = "53"
                parent_path_depart = {
                    53 : "."
                }
                roots = {
                    53 : 53
                }
            else:
                #дети становятся родителями
                parents = children
                children = []
                
                #для каждого родителя
                for father in parents:
                    #получаем его детей
                    for child in self.DepartmentModel.find_deps_by_father_id(father.id):
                        #и всех детей кидаем в один слой
                        children.append(child)
                        roots[child.id] = father.id
                        

            
            #заполняю вывод
            for obj in children:
                layer = get_info_by_obj(obj, parent_path_depart[roots[obj.id]])
                parent_path_depart[obj.id] = layer["_source"]['path_depart']
                dep_data_ES.append(layer)


        helpers.bulk(elastic_client, dep_data_ES)
        return {"status": True}




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
                        {"match": {"name": {"query": word ,"boost": 10}}},
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