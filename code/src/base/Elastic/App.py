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



# elastic_client = Elasticsearch(hosts=["http://elasticsearch:9200"], basic_auth=('elastic', pswd), verify_certs=False, request_timeout=100)

# if elastic_client.ping():
#     LogsMaker().ready_status_message("✅ Успешное подключение Elasticsearch!")
# else:
#     LogsMaker().fatal_message("❌ Ошибка аутентификации Elasticsearch!")



def create_elastic_client():
    max_retries = 5
    retry_delay = 15
    
    for i in range(max_retries):
        try:
            elastic_client = Elasticsearch(hosts=["http://elasticsearch:9200"], basic_auth=('elastic', pswd), verify_certs=False, request_timeout=100)


            if elastic_client.ping():
                LogsMaker().ready_status_message("✅ Успешное подключение Elasticsearch!")
                return elastic_client
        except Exception as e:
            LogsMaker().warning_message(f"❌ Connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                LogsMaker().info_message(f"🕐 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    LogsMaker().fatal_message("❌ Ошибка аутентификации Elasticsearch!")

elastic_client = create_elastic_client()


with open('./src/base/sections.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)


def search_everywhere(key_word):  # , size_res: Optional[int] = 40
    result = []
    words = key_word.strip().split()
    
    # Формируем запрос для пользователей в зависимости от количества слов
    if len(words) >= 2:
        user_query = {
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
        }
    else:
        # Одно слово - обычный поиск
        user_query = {
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
        }
    
    res = elastic_client.search(
        index=["articles", "user"],
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {"term": {"_index": {"value": "articles"}}},
                                    {
                                        "bool": {
                                            "should": [
                                                # точный поиск
                                                {
                                                    "bool": {
                                                        "should": [
                                                            {"match": {"title": {"query": key_word, "boost": 10}}},
                                                            {"match": {"preview_text": {"query": key_word, "boost": 8}}},
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
                                    {"term": {"_index": {"value": "user"}}},
                                    user_query  # Используем твою улучшенную конфигурацию
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
                    },
                    "user_fio": {
                        "highlight_query": {
                            "bool": {
                                "should": [
                                    {"match": {"user_fio": key_word}},
                                    {"match": {"user_fio": {"query": key_word, "fuzziness": "AUTO"}}}
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
                if "authorId" in res_info["_source"].keys() and res_info["_source"]["authorId"] is not None:
                    art_info['authorId'] = res_info["_source"]["authorId"]
                elif "company" in res_info["_source"].keys() and res_info["_source"]["company"] is not None:
                    art_info['authorId'] = res_info["_source"]['company']
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