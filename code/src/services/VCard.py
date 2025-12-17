from fastapi import APIRouter, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ..base.B24 import B24

from transliterate import translit
import qrcode
import vobject
import base64
import requests
import os


vcard_app = APIRouter(prefix="/vcard")

vcard_app.mount("/vcard_static", StaticFiles(directory="./vcard_db"), name="vcard_static")

def cyrillic_to_latin(text: str) -> str:
    return translit(text, 'ru', reversed=True)

class User_Vcard:
    def __init__(self, uuid=""):
        self.uuid = uuid
    
    def findByIDdepart(self, id):
        return B24().getDepartByID(id)

    def finfByUuid(self):
        titles_to_change = {'UF_USR_1696592324977' : 'Direction', 'UF_USR_1705744824758' : 'Division', 'UF_USR_1707225966581' : 'Combination'}
        search = B24().getUsersByUuid(f"ad|{self.uuid}")
        if search:
            for title, new_title in titles_to_change.items():
                if title in search[0].keys():
                    value = search[0].pop(title)
                    search[0][new_title] = value

            departments_id = search[0]["UF_DEPARTMENT"]
            num_to_word = []
            for department in departments_id:
                depart = self.findByIDdepart(department)
                name = depart[0]["NAME"]
                num_to_word.append(name)
            search[0]["UF_DEPARTMENT"] = num_to_word
            return search[0]
        return None

    

    def create_qr(self):
        data = f'https://intranet.emk.ru/api/vcard/by_uuid/{self.uuid}'
        filename = f'{self.uuid}.png'
        img = qrcode.make(data)
        img.save(f'./vcard_db/{filename}')
        return filename

    def create_vcs(self):
        user_info = self.finfByUuid()
        filename = f'{cyrillic_to_latin(user_info['LAST_NAME'])}-{cyrillic_to_latin(user_info['NAME'])}-{cyrillic_to_latin(user_info['SECOND_NAME'])}.vcf'

        important_param = ['NAME', 'LAST_NAME', 'SECOND_NAME', 'EMAIL', "PERSONAL_MOBILE", 'WORK_PHONE', 'WORK_POSITION','Direction', "PERSONAL_PHOTO"]

        vcard = vobject.vCard()
        vcard.add("FN").value = f"{user_info['LAST_NAME']} {user_info['NAME']} {user_info['SECOND_NAME']}"
        vcard.add("N").value = vobject.vcard.Name(
            family=user_info['LAST_NAME'],
            given=user_info['NAME'],
            additional=user_info['SECOND_NAME']
        )
        user_depart = None
        user_position = None
        user_company = None
        for key in important_param:
            if key in user_info.keys():
                if key == "PERSONAL_MOBILE":                    
                    vcard.add("TEL").value = user_info["PERSONAL_MOBILE"]
                    vcard.add("TEL").type_param = "CELL"

                elif key == 'WORK_PHONE':                    
                    vcard.add("TEL").value = user_info['WORK_PHONE']
                    vcard.add("TEL").type_param = "WORK"
                
                elif key == "EMAIL":
                    vcard.add("EMAIL").value = user_info["EMAIL"]
                    domen = user_info["EMAIL"].split("@")
                    if domen[-1] == 'emk.ru':
                        user_company = 'АО "НПО "ЭМК"'

                elif key == 'Direction':                    
                    user_depart = user_info["Direction"][0]
                    
                elif key == "WORK_POSITION":
                    user_position = user_info["WORK_POSITION"]
                    
                elif key == "PERSONAL_PHOTO":
                    if user_info['PERSONAL_PHOTO'] != "":
                        user_url = user_info['PERSONAL_PHOTO']
                        response = requests.get(user_url)
                        if response.status_code == 200:
                            photo = base64.b64encode(response.content).decode("utf-8")
                            vcard.add("PHOTO").value = photo
                            vcard.add("PHOTO").type_param = "PNG"
                        else:
                            print(response.status_code)
            else:
                pass
        
        if len(user_company) != 0:
            if len(user_position) != 0 and len(user_depart) != 0:
                vcard.add("TITLE").value = f'{user_company} - {user_depart}, {user_position}'
            elif len(user_position) != 0 and len(user_depart) == 0:
                vcard.add("TITLE").value = f"{user_company} - {user_position}"
            elif len(user_depart) != 0 and len(user_position) == 0:
                vcard.add("TITLE").value = f"{user_company} - {user_depart}"
        else:
            if len(user_position) != 0 and len(user_depart) != 0:
                vcard.add("TITLE").value = f'{user_depart}, {user_position}'
                print(3)
            elif len(user_position) != 0 and len(user_depart) == 0:
                vcard.add("TITLE").value = user_position
                print(2)
            elif len(user_depart) != 0 and len(user_position) == 0:
                vcard.add("TITLE").value = user_depart
                print(1)


        content = vcard.serialize()
        
        return content, filename



@vcard_app.get("/by_uuid/{uuid}", tags=["VCard", "Битрикс24"])
def root(uuid):
    """
    ## Метод `user.search`

    Выполняет поиск пользователя в Битрикс24 по уникальному идентификатору (XML_ID) через API метод `user.search`.

    ### Входные параметры
    | Параметр | Тип | Описание | Обязательный |
    |----------|-----|----------|--------------|
    | `uuid` | string | Уникальный идентификатор пользователя (XML_ID в Битрикс24) | Да |

    ### Возвращаемые данные
    Возвращает список найденных пользователей. Каждый пользователь содержит следующие поля:
    - `ID` (int) — внутренний ID пользователя в Битрикс24
    - `XML_ID` (string) — уникальный идентификатор пользователя
    - `NAME` (string) — имя пользователя
    - `LAST_NAME` (string) — фамилия пользователя
    - `EMAIL` (string) — email адрес
    - `PERSONAL_PHOTO` (string) — URL фотографии профиля
    - `WORK_POSITION` (string) — должность
    - `WORK_PHONE` (string) — рабочий телефон
    - `PERSONAL_MOBILE` (string) — мобильный телефон
    - `UF_DEPARTMENT` (list) — список ID подразделений
    - `UF_SKYPE` (string) — Skype
    - `UF_TWITTER` (string) — Twitter
    - `UF_FACEBOOK` (string) — Facebook
    - `UF_LINKEDIN` (string) — LinkedIn
    - `UF_SKILLS` (string) — навыки и компетенции

    ### Пример ответа
    ```json
    [
    {
        "ID": "123",
        "XML_ID": "employee_12345",
        "NAME": "Иван",
        "LAST_NAME": "Иванов",
        "EMAIL": "ivanov@company.com",
        "WORK_POSITION": "Senior Developer",
        "PERSONAL_PHOTO": "https://bitrix24.com/upload/user/123/photo.jpg",
        "WORK_PHONE": "+7 (495) 123-45-67",
        "PERSONAL_MOBILE": "+7 (916) 123-45-67"
    }
    ]
    """
    return User_Vcard(uuid).finfByUuid()

@vcard_app.get("/{uuid}/qr", tags=["VCard"])
def dowload_file(uuid):
    current_file_path = f'./vcard_db/{uuid}.png'
    file_exist = os.path.isfile(current_file_path)
    
    if file_exist:
        return FileResponse(current_file_path, media_type="image/png")
    else:
        
        filename = User_Vcard(uuid).create_qr()
        file_path = f'./vcard_db/{filename}'
        return FileResponse(file_path, media_type="image/png")

@vcard_app.get("/get/{uuid}", tags=["VCard"])
def download_contact(uuid):
    content, filename = User_Vcard(uuid).create_vcs() 
    return Response(content=content, media_type="text/vcard",  headers={"Content-Disposition": f"attachment; filename={filename}"})

