from .App import elastic_client, DOMAIN

from fastapi import HTTPException

from src.model.File import File

class UserSearchModel:
    def __init__(self):
        from ..pSQL.objects.UserModel import UserModel
        self.UserModel = UserModel()
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

        users_data = self.UserModel.all()
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

    '''
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
    '''

    def elasticsearch_users(self, key_word):
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
                                                            {"match":
                                                                {"indirect_data.work_position": {"query": key_word,
                                                                                                "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1705744824758": {
                                                                "query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1707225966581": {
                                                                "query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1696592324977": {
                                                                "query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1586853958167": {
                                                                "query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_department_main": {
                                                                "query": key_word, "boost": 5}}},
                                                            {"match": {"indirect_data.uf_usr_1586854037086": {
                                                                "query": key_word, "boost": 5}}}
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
                "size": 1000
            }
        )
        users = []
        true_search_flag = False

        for res_info in res['hits']['hits']:
            if "matched_queries" in res_info.keys():
                true_search_flag = True
            user_info = {}
            user_info['name'] = res_info["_source"]["user_fio"]
            user_info['sectionHref'] = "userPage"
            user_info['id'] = int(res_info["_id"])
            user_info['image'] = res_info["_source"]["photo_file_id"]
            user_info['dep_id'] = res_info["_source"]["indirect_data"]["uf_department"][0]
            users.append(user_info)

        sec_user = {}
        sec_user['section'] = 'Пользователи'
        if true_search_flag is False:
            sec_user['msg'] = 'Точных совпадений не нашлось, возможно вы имели ввиду:'
        sec_user['content'] = users
        result.append(sec_user)
        return result  # result  res['hits']['hits']

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}

