from .App import elastic_client, helpers
from .App import UserModel, DepartmentModel, UsDepModel
from .App import DOMAIN


class StructureSearchModel:
    def __init__(self):
        # self.DepartmentModel = DepartmentModel
        # self.UsDepModel = UsDepModel
        # self.UserModel = UserModel
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
        usr_sql_data = UserModel().all()

        """⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇Блок для добавления верхушки айсберга⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇"""
        # находим верхушку айсберга, ее father_id будет None
        # list_children = DepartmentModel().find_deps_by_father_id(53)
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
        # print(dep_data_ES)
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
            """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
            dep_data['users'] = users_list
            data_action = {
                "_index": self.index,
                "_op_type": "index",
                "_id": N_1.id,
                "_source": dep_data
            }
            dep_data_ES.append(data_action)
            # второе разветвление
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
                    """⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆"""
                    dep_data['users'] = users_list
                    data_action = {
                        "_index": self.index,
                        "_op_type": "index",
                        "_id": N_2.id,
                        "_source": dep_data
                    }
                    dep_data_ES.append(data_action)

                    # третье разветвление
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
                            users = UsDepModel \
                                (id=N_3.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                            if isinstance(users, list):
                                for usr in usr_sql_data:
                                    user = usr.__dict__
                                    if user['id'] in users:
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
                                    users = UsDepModel \
                                        (id=N_4.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                    if isinstance(users, list):
                                        for usr in usr_sql_data:
                                            user = usr.__dict__
                                            if user['id'] in users:
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
                                            users = UsDepModel \
                                                (id=N_5.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                            if isinstance(users, list):
                                                for usr in usr_sql_data:
                                                    user = usr.__dict__
                                                    if user['id'] in users:
                                                        user_data = {}
                                                        if user['active'] is True:
                                                            user_data['id'] = user['id']

                                                            if user['second_name'] is not None or user['second_name'] != '':user_data['name'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                                                            else:
                                                                user_data['name'] = f'{user['last_name']} {user['name']}'

                                                            if 'work_position' in user['indirect_data'].keys() and user['indirect_data'][
                                                                'work_position'] != '':
                                                                user_data['user_position'] = user['indirect_data']['work_position']
                                                            else:
                                                                pass

                                                            if user['photo_file_id']:
                                                                photo_inf = File \
                                                                    (id=user['photo_file_id']).get_users_photo()
                                                                url = photo_inf['URL']
                                                                user_data['image'] = f"{DOMAIN}{url}"
                                                            else:
                                                                user_data['image'] = None

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
                                                    users = UsDepModel \
                                                        (id=N_6.id).find_user_by_dep_id()  # берём id всех пользователей департамента
                                                    if isinstance(users, list):
                                                        for usr in usr_sql_data:
                                                            user = usr.__dict__
                                                            if user['id'] in users:
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
                                                                                photo_inf = File(id=user
                                                                                    ['photo_file_id']).get_users_photo()
                                                                                url = photo_inf['URL']
                                                                                user_data['image'] = f"{DOMAIN}{url}"
                                                                            else:
                                                                                user_data['image'] = None

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