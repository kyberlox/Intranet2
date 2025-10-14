from .App import elastic_client, DOMAIN, helpers

from fastapi import HTTPException

from src.services.LogsMaker import LogsMaker


class UserSearchModel:
    def __init__(self):
        from ..pSQL.objects.UserModel import UserModel
        self.UserModel = UserModel()
        self.index = 'user'
        self.elastic_client = elastic_client

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
                            "min_gram": 4,
                            "max_gram": 7
                        }
                    }
                },
                "max_ngram_diff": "7"
            },
            "mappings": {
                "properties": {
                    # "last_name": {
                    #     "type": "text",
                    #     "analyzer": "GOD_PLEASE_FUZZY_V2",
                    #     "fields": {
                    #         "fuzzy": {
                    #             "type": "text",
                    #             "analyzer": "GOD_PLEASE"
                    #         }
                    #     }
                    # },
                    # "name": {
                    #     "type": "text",
                    #     "analyzer": "GOD_PLEASE_FUZZY_V2",
                    #     "fields": {
                    #         "fuzzy": {
                    #             "type": "text",
                    #             "analyzer": "GOD_PLEASE"
                    #         }
                    #     }
                    # },
                    # "second_name": {
                    #     "type": "text",
                    #     "analyzer": "GOD_PLEASE_FUZZY_V2",
                    #     "fields": {
                    #         "fuzzy": {
                    #             "type": "text",
                    #             "analyzer": "GOD_PLEASE"
                    #         }
                    #     }
                    # },
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
        index_name = self.index
        
        res = elastic_client.indices.create(index=self.index, body=mapping)
        return res
        # try:    

        #     if elastic_client.indices.exists(index=index_name):
        #         # Обновляем маппинг существующего индекса
        #         elastic_client.indices.put_mapping(index=index_name, body=mapping)#["mappings"])
        #         return {"status": "updated", "message": f"Mapping for {index_name} updated"}
        #     else:
        #         elastic_client.indices.create(index=index_name, body=mapping)
        #         return {"status": "created", "message": f"Index {index_name} created"}
            
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=500,
        #         detail=f"Index operation failed: {str(e)}"
        #     )

    def dump(self):
        from src.model.File import File
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
            # 'last_name', 'name', 'second_name', 
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
                    # data_row = dict()
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

        #             usr_data = data_row
        
        #             data_action = {
        #                 "_index": self.index,
        #                 "_op_type": "index",
        #                 "_id": user_id,
        #                 "_source": usr_data
        #             }

        #             users_data_ES.append(data_action)
        
        # success, errors = helpers.bulk(elastic_client, users_data_ES)

        # # print(success, errors)
        # LogsMaker().ready_status_message(f"в чем беда: {success} {errors}")
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

    def elasticsearch_users(self, key_word, size_res=1000):
        result = []

        words = key_word.strip().split()
    
        if len(words) >= 2:
            # Если несколько слов - используем более строгий поиск
            body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase": {
                                    "user_fio": {
                                        "query": key_word,
                                        "slop": 1,
                                        "boost": 30
                                    }
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "match": {
                                                "user_fio": {
                                                    "query": words[0],  # Первое слово (Игорь)
                                                    "boost": 5
                                                }
                                            }
                                        },
                                        {
                                            "match_phrase_prefix": {
                                                "user_fio": {
                                                    "query": " ".join(words[1:]),  # Остальные слова (Гази)
                                                    "boost": 10
                                                }
                                            }
                                        }
                                    ],
                                    "boost": 25
                                }
                            },
                            {
                                "match": {
                                    "user_fio": {
                                        "query": key_word,
                                        "operator": "and",
                                        "boost": 15
                                    }
                                }
                            }
                        ]
                    }
                },
                "size": size_res
            }
        else:
            # Одно слово - обычный поиск
            body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase_prefix": {
                                    "user_fio": {
                                        "query": key_word,
                                        "boost": 20
                                    }
                                }
                            },
                            {
                                "match": {
                                    "user_fio": {
                                        "query": key_word,
                                        "operator": "and",
                                        "boost": 10
                                    }
                                }
                            }
                        ]
                    }
                },
                "size": size_res
            }
        res = elastic_client.search(index=self.index, body=body)
        # res = elastic_client.search(
        #     index=self.index,
        #     body={
        #         "query": {
        #             "bool": {
        #                 "should": [
        #                     {
        #                         "bool": {
        #                             "should": [ 
        #                                 {"match": {"user_fio": {"query": key_word, "boost": 10}}}
        #                                 # {"match": {"last_name": {"query": key_word, "boost": 10}}},
        #                                 # {"match": {"name": {"query": key_word, "boost": 10}}},
        #                                 # {"match": {"second_name": {"query": key_word, "boost": 10}}}
        #                             ],
        #                             "_name": "true_search"
        #                         }
        #                     },
        #                     {
        #                         "multi_match": {
        #                             "query": key_word,
        #                             # "fields": ["last_name.fuzzy", "name.fuzzy", "second_name.fuzzy"],
        #                             # "fields": ["last_name", "name", "second_name"],
        #                             "fields": ["user_fio"],
        #                             # "fuzziness": "1",
        #                             "boost": 2
        #                         }
        #                     }
        #                 ]
        #             }
        #         },
        #         "size": size_res
        #     }
        # )
        users = []
        true_search_flag = False

        for res_info in res['hits']['hits']:
            if "matched_queries" in res_info.keys():
                true_search_flag = True
            user_info = {}
            # if res_info["_source"]['second_name'] is None:
            #     fio = f'{res_info["_source"]['last_name']} {res_info["_source"]['name']}'
            # else:
            #     fio = f'{res_info["_source"]['last_name']} {res_info["_source"]['name']} {res_info["_source"]['second_name']}'
            # user_info['name'] = fio
            user_info['name'] = res_info["_source"]['user_fio']
            user_info['sectionHref'] = "userPage"
            user_info['id'] = int(res_info["_id"])
            user_info['image'] = res_info["_source"]["photo_file_id"]
            # user_info['dep_id'] = res_info["_source"]["indirect_data"]["uf_department"][0]
            users.append(user_info)

        sec_user = {}
        sec_user['section'] = 'Пользователи'
        if true_search_flag is False:
            sec_user['msg'] = 'Точных совпадений не нашлось, возможно вы имели ввиду:'
        sec_user['content'] = users
        result.append(sec_user)
        return result  # result  res['hits']['hits']

    # поиск не только по фамилии, но и по телефону, должности и подразделению
    # def elasticsearch_users(self, key_word, size_res=1000):
    #     result = []
    #     res = elastic_client.search(
    #         index=self.index,
    #         body={
    #             "query": {
    #                 "bool": {
    #                     "should": [
    #                         {
    #                             "bool": {
    #                                 "should": [
    #                                     {"match": {"user_fio": {"query": key_word, "boost": 10}}},
    #                                     {"term": {"uf_phone_inner": {"value": key_word, "boost": 10}}},
    #                                     {
    #                                         "nested": {
    #                                             "path": "indirect_data",
    #                                             "query": {
    #                                                 "bool": {
    #                                                     "should": [
    #                                                         {"match":
    #                                                             {"indirect_data.work_position": {"query": key_word,
    #                                                                                             "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_1705744824758": {
    #                                                             "query": key_word, "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_1707225966581": {
    #                                                             "query": key_word, "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_1696592324977": {
    #                                                             "query": key_word, "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_1586853958167": {
    #                                                             "query": key_word, "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_department_main": {
    #                                                             "query": key_word, "boost": 5}}},
    #                                                         {"match": {"indirect_data.uf_usr_1586854037086": {
    #                                                             "query": key_word, "boost": 5}}}
    #                                                     ]
    #                                                 }
    #                                             }
    #                                         }
    #                                     }
    #                                 ],
    #                                 "_name": "true_search"
    #                             }
    #                         },
    #                         {
    #                             "multi_match": {
    #                                 "query": key_word,
    #                                 "fields": ["user_fio.fuzzy"],
    #                                 "fuzziness": "1",
    #                                 "boost": 2
    #                             }
    #                         },
    #                         {
    #                             "nested": {
    #                                 "path": "indirect_data",
    #                                 "query": {
    #                                     "multi_match": {
    #                                         "query": key_word,
    #                                         "fields": [
    #                                             "indirect_data.work_position.fuzzy",
    #                                             "indirect_data.uf_usr_1705744824758.fuzzy",
    #                                             "indirect_data.uf_usr_1707225966581.fuzzy",
    #                                             "indirect_data.uf_usr_1696592324977.fuzzy",
    #                                             "indirect_data.uf_usr_1586853958167.fuzzy",
    #                                             "indirect_data.uf_usr_department_main.fuzzy",
    #                                             "indirect_data.uf_usr_1586854037086.fuzzy"
    #                                         ],
    #                                         "fuzziness": "1",
    #                                         "boost": 1
    #                                     }
    #                                 },
    #                                 "score_mode": "max"
    #                             }
    #                         }
    #                     ]
    #                 }
    #             },
    #             "size": size_res
    #         }
    #     )
    #     users = []
    #     true_search_flag = False

    #     for res_info in res['hits']['hits']:
    #         if "matched_queries" in res_info.keys():
    #             true_search_flag = True
    #         user_info = {}
    #         user_info['name'] = res_info["_source"]["user_fio"]
    #         user_info['sectionHref'] = "userPage"
    #         user_info['id'] = int(res_info["_id"])
    #         user_info['image'] = res_info["_source"]["photo_file_id"]
    #         user_info['dep_id'] = res_info["_source"]["indirect_data"]["uf_department"][0]
    #         users.append(user_info)

    #     sec_user = {}
    #     sec_user['section'] = 'Пользователи'
    #     if true_search_flag is False:
    #         sec_user['msg'] = 'Точных совпадений не нашлось, возможно вы имели ввиду:'
    #     sec_user['content'] = users
    #     result.append(sec_user)
    #     return result  # result  res['hits']['hits']


    def update_user_el_index(self, user_data):
        important_list = ['email', 'personal_mobile', 'personal_city', 'personal_gender', 'personal_birthday', 'uf_phone_inner', "indirect_data", "photo_file_id"]
        data = user_data.__dict__
        result = None
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
                doc = {
                    "doc": data_row
                }
                result = elastic_client.update(index=self.index, id=user_id, body=doc)
        if result:
            return True
        else:
            return False
    
    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}

