from .App import elastic_client, helpers, json, sections
from .App import DOMAIN

from src.services.LogsMaker import LogsMaker


class ArticleSearchModel:

    def __init__(self):
        from ..pSQL.objects.ArticleModel import ArticleModel
        self.ArticleModel = ArticleModel()
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
        from src.model.File import File

        LogsMaker().info_message("Тут всё может пойти не по плану")
        try:
            # в самом начале нет индекса, поэтому вылезает ошибка при первой попытке дампа
            self.delete_index()
        except:
            pass
        LogsMaker().ready_status_message("ВСЁ ХОРОШО! 👍")
        
        self.create_index()
        


        article_SQL_data = self.ArticleModel.all()

        article_data_ES = []
        article_action = {}
        for article_data in article_SQL_data:
            art_id = article_data['id']
            LogsMaker().info_message(f"Загрузка данных о статье {art_id} в Эластика")
            data_row = {}
            if article_data['active'] and article_data['section_id'] != 6 and article_data['section_id'] != 41:

                if isinstance(article_data['indirect_data'], str):
                    article_data['indirect_data'] = json.loads(article_data['indirect_data'])
                # if article_data['section_id'] == 16:
                #     print(article_data['id'], type(article_data['indirect_data']))
                #     article_data['indirect_data'] = json.loads(article_data['indirect_data'])

                # обрабатываем случай с интервью Еленой Земской
                if article_data['section_id']  == 16 and \
                        ("PROPERTY_1025" not in article_data['indirect_data'] or article_data['indirect_data'][
                    'PROPERTY_1025'] is None):
                    continue
                else:
                    preview_photo = None
                    # обработка превью
                    files = File(art_id=article_data['id']).get_files_by_art_id()
                    
                    for file in files:
                        if file["is_preview"]:
                            url = file["file_url"]
                            # внедряю компрессию
                            if article_data['section_id'] == 18:  # отдельный алгоритм для памятки новому сотруднику
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image/yowai_mo"
                                url = '/'.join(preview_link)
                            else:
                                preview_link = url.split("/")
                                preview_link[-2] = "compress_image"
                                url = '/'.join(preview_link)

                            preview_photo = f"{DOMAIN}{url}"

                    # находим любую картинку, если она есть
                    for file in files:
                        
                        if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file[
                            "original_name"] or "png" in file["original_name"]:
                            url = file["file_url"]
                            LogsMaker().info_message(f"Найден файл URL={url}")
                            # внедряю компрессию
                            if article_data['section_id'] == 18:  # отдельный алгоритм для памятки новому сотруднику
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

                    article_data_ES.append(article_action)

        LogsMaker().ready_status_message("Осталось только задампиить данные в Эластик")
        helpers.bulk(elastic_client, article_data_ES)

        return {"status": True}

    def elasticsearch_article(self, key_word):
        from src.model.Section import Section

        sections = Section().get_all()
        result = []
        res = elastic_client.search(
            index=self.index,
            body={
                "query": {
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
                "size": 200
            }
        )
        articles = []
        true_search_flag = False

        for res_info in res['hits']['hits']:
            if "matched_queries" in res_info.keys():
                true_search_flag = True
            art_info = {}
            art_info['name'] = res_info["_source"]["title"]
            section_href = next(
                (s.get('sectionHref') for s in sections if s['id'] == res_info["_source"]["section_id"]),
                res_info["_source"]["section_id"])
            art_info['sectionHref'] = section_href
            art_info['id'] = int(res_info["_id"])
            if "authorId" in res_info["_source"].keys() and res_info["_source"]["authorId"] is not None:
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

        return result  # res['hits']['hits'] result

    def delete_index(self):
        elastic_client.indices.delete(index=self.index)
        return {'status': True}

