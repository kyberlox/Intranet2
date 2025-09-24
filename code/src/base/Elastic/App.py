from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
from elasticsearch import helpers

from src.services.LogsMaker import LogsMaker

import json

from fastapi import APIRouter, Body
from fastapi import HTTPException

import os
from dotenv import load_dotenv

load_dotenv()



pswd = os.getenv('pswd')
DOMAIN = os.getenv('HOST')

search_router = APIRouter(prefix="/elastic", tags=["Поиск по тексту"])



elastic_client = Elasticsearch(hosts=["http://elasticsearch:9200"], basic_auth=('elastic', pswd), verify_certs=False, request_timeout=60)



if elastic_client.ping():
    LogsMaker().ready_status_message("✅ Успешное подключение Elasticsearch!")
else:
    LogsMaker().fatal_message("❌ Ошибка аутентификации Elasticsearch!")


with open('./src/base/sections.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)


def search_everywhere(key_word):  # , size_res: Optional[int] = 40
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
                                                # точный поиск
                                                {
                                                    "bool": {
                                                        "should": [
                                                            {"match": {"title": {"query": key_word, "boost": 10}}},
                                                            {"match": {
                                                                "preview_text": {"query": key_word, "boost": 8}}},
                                                            {"match": {"content_text": {"query": key_word, "boost": 6}}}
                                                        ],
                                                        "_name": "true_search"
                                                    }
                                                },
                                                # неточный поиск
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
                                                            {"term": {
                                                                "uf_phone_inner": {"value": key_word, "boost": 10}}},
                                                            {
                                                                "nested": {
                                                                    "path": "indirect_data",
                                                                    "query": {
                                                                        "bool": {
                                                                            "should": [
                                                                                {"match": {
                                                                                    "indirect_data.work_position": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_1705744824758": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_1707225966581": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_1696592324977": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_1586853958167": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_department_main": {
                                                                                        "query": key_word,
                                                                                        "boost": 5}}},
                                                                                {"match": {
                                                                                    "indirect_data.uf_usr_1586854037086": {
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
                # print(res_info)
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
                section_href = next(
                    (s.get('sectionHref') for s in sections if s['id'] == res_info["_source"]["section_id"]),
                    res_info["_source"]["section_id"])
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
    return result  # result  res['hits']['hits']