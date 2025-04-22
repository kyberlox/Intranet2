from src.base.B24 import B24
from src.base.pSQLmodels import SectionModel
from src.base.mongodb import FileModel

from src.model.Article import Article

from datetime import datetime

import json

from fastapi import APIRouter

section_router = APIRouter(prefix="/section", tags=["Разделы"])

class MainPage:
    """
    Класс для организации данных по секциям на главной странице
    """
    def __init__(self, page=0, sorted_list=[]):
        self.page = page
        self.sorted_list = sorted_list

    def page_32(self):
        second_page = {
            'id': self.page, 
            'type': 'singleBlock', 
            'title': 'Организационное развитие', 
            "href": "corpnews", 
            'images': [{'id': self.sorted_list[0][0], 'image': "https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg"}]
            }
        return second_page

    def page_31(self):
        second_page = {
            'id': self.page,
            'type': 'fullRowBlock',
            'title': 'Бизнес-новости',
            'href': 'actualnews',
            'images': []
        }

        business_news = []
        
        image_url = ''
        for i, row in enumerate(self.sorted_list):
            if i < 5:
                news = {}
                preview_pict = Section().get_preview(row[0])

                if preview_pict is None:
                    image_url = 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg'
                else:
                    image_url = preview_pict
                
                news['id'] = row[0]
                news['title'] = row[1]
                news['description'] = row[2]
                news['image'] = image_url
                # сюда реакции
                business_news.append(news)
        second_page['images'] = business_news
        return second_page

    def page_16(self):
        second_page = {
            'id': self.page,
            'type': 'fullRowBlock',
            'title': 'Интервью',
            'href': 'interview',
            'images': []
        }

        interview_news = []
        
        image_url = ''
        for i, row in enumerate(self.sorted_list):
            if i < 5:
                news = {}
                preview_pict = Section().get_preview(row[0])

                if preview_pict is None:
                    image_url = 'отсутствует превью'
                else:
                    image_url = preview_pict
                
                news['id'] = row[0]
                news['title'] = row[1]
                news['description'] = row[2]
                news['image'] = image_url
                # сюда реакции
                interview_news.append(news)
        second_page['images'] = interview_news
        return second_page
    
    def page_33(self):
        second_page = {
            'id': self.page,
            'type': 'fullRowBlock',
            'title': 'Видеорепортажи',
            'href': 'videonews',
            'images': []
        }

        video_news = []
        
        image_url = ''
        for i, row in enumerate(self.sorted_list):
            if i < 5:
                news = {}
                preview_pict = Section().get_preview(row[0])

                if preview_pict is None:
                    image_url = 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg'
                else:
                    image_url = preview_pict
                
                news['id'] = row[0]
                news['title'] = row[1]
                news['description'] = row[2]
                news['image'] = image_url
                # сюда реакции
                video_news.append(news)
        second_page['images'] = video_news
        return second_page

    def page_51(self, afisha):
        second_page = {
            'id': 9,
            'type': 'mixedRowBlock',
            'content': []
        }
        corpevents = {
            'id': self.page,
            'type': "fullRowBlock",
            'title': "Корпоративные события",
            'href': "corpevents",
            'images': []
        }
        image_url = ''
        corpevents_news = []
        for i, row in enumerate(self.sorted_list):
            if i < 5:
                news = {}
                preview_pict = Section().get_preview(row[0])

                if preview_pict is None:
                    image_url = 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg'
                else:
                    image_url = preview_pict
                
                news['id'] = row[0]
                news['title'] = row[1]
                news['description'] = row[2]
                news['image'] = image_url
                # сюда реакции
                corpevents_news.append(news)

        corpevents['images'] = corpevents_news
        second_page['content'] = [afisha, corpevents]
        return second_page

class Section:
    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def load(self):
        #загрузить из JSON
        section_data_file = open("./src/base/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        return SectionModel().upload(section_data)

    def get_all(self):
        section_data_file = open("./src/base/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        return section_data

    def get_preview(self, id):
        res = FileModel(id).find_all_by_art_id()
        mongo_list = []
        preview_inf = []
        one_preview_inf = []
        for result in res:
            mongo_list.append(result)

        if len(mongo_list) > 1:

            for info in mongo_list:
                one_preview_inf.append(info['b24_id'])
                one_preview_inf.append(info['file_url'])
                preview_inf.append(one_preview_inf)

            # сортируем по b24_id если фоток много и берем с наименьшим b24_id
            sorted_list = sorted(preview_inf, key=lambda x: x[0], reverse=True)

            preview_inf = sorted_list[0][1]
            return preview_inf
        elif len(mongo_list) == 0:
            return None
        else:
            return mongo_list[0]['file_url']


    def find_by_id(self):
        if self.id == "0":
            main_page = [32, 31, 16, 33, 51] # список доступных секций для отображения на главной странце
            
            page_view = []

            new_workers = {
                'id': 1,
                'type': 'singleBlock',
                'title': 'Новые сотрудники',
                'images': [{
                    "id": 1,
                    "image": "фотки чела нет",
                }],
                'href': 'newWorkers',
            } # словарь-заглушка для будущей секции "новые сотрудники"

            birthday = {
                'id': 2,
                'type': 'singleBlock',
                'title': 'С днем рождения!',
                'images': [{
                    "id": 1,
                    "image": "фотки именниника нет",
                    "href": "/"
                }],
                'href': 'birthdays',
            } # словарь-заглушка для будущей секции "С днем рождения!"

            idea_block = {
                'id': 4,
                'type': 'singleBlock',
                'title': 'Предложить идею',
                'images': [{
                    "id": 1,
                    "image": "ноль идей",
                    "href": "/"
                }],
                'modifiers': ['outline'],
                'href': 'ideasPage'
            }# словарь-заглушка для будущей секции "Предложить идею"

            emk_competition = {
                'id': 5,
                'type': 'singleBlock',
                'title': 'Конкурсы ЭМК',
                'images': [{
                    "id": 1,
                    "image": "нет конкурсов",
                    "href": "vacancies"
                }],
                '// href': '/'
            } # словарь-заглушка для будущей секции "Конкурсы ЭМК"

            afisha = {
                'type': "singleBlock",
                'title': "Афиша",
                'images': [
                    {
                        'id': 1,
                        'image': "https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg",
                        'href': "home"
                    },
                    {
                        'id': 2,
                        'image': "https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg",
                        'href': "home"
                    }
                ]
            } # словарь-заглушка для будущей секции "Афиша"
        

            page_view.append(new_workers) # заглушка (в будущем дописать функцию в класс MainPage) 
            page_view.append(birthday) # заглушка (в будущем дописать функцию в класс MainPage)

            for page in main_page: # проходимся по каждой секции
                second_page = {} # словарь для секций и ее статей
                date_list = [] # список для сортировки по дате
                page_value = Article(section_id = page).search_by_section_id() # список всех статей, новостей и тд

                for value in page_value:
                    values = value.__dict__
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_value.append(values["name"])
                    date_value.append(values["preview_text"])
                    date_value.append(values["date_creation"])
                    date_list.append(date_value) # получили список с необходимыми данными

                # сортируем по дате
                sorted_list = sorted(date_list, key=lambda x: x[3], reverse=True)
                

                if page == 32:
                    second_page = MainPage(page, sorted_list).page_32()
                    page_view.append(second_page)

                    page_view.append(idea_block) # заглушка (в будущем дописать функцию в класс MainPage)
                    page_view.append(emk_competition) # заглушка (в будущем дописать функцию в класс MainPage)

                elif page == 31:
                    second_page = MainPage(page, sorted_list).page_31()
                    page_view.append(second_page)
                
                elif page == 16: 
                    second_page = MainPage(page, sorted_list).page_16()
                    page_view.append(second_page)

                elif page == 33:
                    second_page = MainPage(page, sorted_list).page_33()
                    page_view.append(second_page)

                elif page == 51:
                    second_page = MainPage(page, sorted_list).page_51(afisha) # afisha - заглушка (в будущем дописать функцию в класс MainPage)
                    page_view.append(second_page)

            return page_view
        else:
            return SectionModel(id = self.id).search_by_id()

    def find_by_parent_id(self):
        return SectionModel(parent_id = self.parent_id).search_by_parent_id()


#загрузить разделы из json файла
@section_router.put("")
def upload_sections():
    return Section().load()

#получить все разделы
@section_router.get("/all")
def get_all_sections():
    return Section().get_all()

#получить раздел по id
@section_router.get("/{ID}")
def get_section(ID):
    return Section(id = ID).find_by_id()

#получить подразделы раздела
@section_router.get("/subsection/{ID}")
def get_subsection(ID):
    return Section(parent_id = ID).find_by_parent_id()