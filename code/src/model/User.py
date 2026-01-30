from ..base.B24 import B24
from ..model.File import File
from ..services.LogsMaker import LogsMaker
from ..services.SendMail import SendEmail

from fastapi import APIRouter, Body
# from fastapi.templating import Jinja2Templates
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

# templates = Jinja2Templates(directory="./front_jinja")

users_router = APIRouter(prefix="/users")


class User:
    def __init__(self, id=0, uuid=""):
        self.id = id
        self.uuid = uuid

        from ..base.pSQL.objects.UserModel import UserModel
        self.UserModel = UserModel()

        from ..base.Elastic.UserSearchModel import UserSearchModel
        self.UserSearchModel = UserSearchModel()

    async def fetch_users_data(self, session):
        data = await B24().getUsers()

        # if hasattr(data, '_asyncio_future_blocking'):  # Это Task
        #     data = await data  # ✅ Дожидаемся результата
        # else:
        #     data = data
        # кастомный прогрессбар
        logg = LogsMaker()

        # await File().index_user_photo()

        # отправить записи
        for usr_data in logg.progress(data, "Обработка информации о пользователях "):
            await self.UserModel.upsert_user(user_data=usr_data, session=session)
            await session.commit()

        status = await self.set_users_photo(session)
        await self.UserModel.create_new_user_view()
        # дампим данные в эластик
        await self.dump_users_data_es(session)

        return {"status": True}

    async def upload_one_user(self, user_data, session):
        await self.UserModel.upsert_user_some_data(user_data=user_data, session=session)
        await session.commit()

        status = await self.set_users_photo(session)
        # await self.UserModel.create_new_user_view()
        # дампим данные в эластик
        await self.dump_users_data_es(session)
        return {"status": True}

    async def search_by_id(self, session):
        self.UserModel.id = self.id
        res = await self.UserModel.find_by_id(session)
        if res['uuid']:
            vcard_file_url = await self.get_user_qr(user_uuid=res['uuid'])
            res['vcard_file_url'] = vcard_file_url
        return res

    async def search_by_id_all(self, session):
        self.UserModel.id = self.id
        res = await self.UserModel.find_by_id_all(session)
        return res

    # def get_dep_usrs(self):
    #     users_data = sorted(await B24().getUsers(), key=lambda d: int(d['ID']))
    #     #dep_data = b24.getDeps()
    #     result = [["id", "ФИО", "Должность", "Подразделение (по иерархии)"]]
    #     for usr in users_data:
    #         if usr["ACTIVE"] and ('WORK_POSITION' in usr and usr['WORK_POSITION'] != "") and ('UF_USR_1705744824758' in usr and usr['UF_USR_1705744824758'] != [] and usr['UF_USR_1705744824758'] != False) and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):
    #             line = [usr['ID'], f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}", usr['WORK_POSITION']]
    #             for dep in usr['UF_USR_1705744824758']:
    #                 line.append(dep)

    #             result.append(line)
    #     return result

    # async def get_uf_depart(self):
    #     return await self.UserModel.find_uf_depart()

    async def user_inf_by_uuid(self, session):
        self.UserModel.uuid = self.uuid
        usr_inf = await self.UserModel.find_by_uuid(session)
        return usr_inf

    async def set_users_photo(self, session):
        data = await B24().getUsers()

        # if hasattr(data, '_asyncio_future_blocking'):  # Это Task
        #     data = await data
        # кастомный прогрессбар
        logg = LogsMaker()
        for usr_data in logg.progress(data, "Загрузка фотографий пользователей "):
            # найдем фото пользователя, если у пользователя есть аватарка

            # if usr_data['ID'] in cool_users:
            uuid = usr_data['ID']
            # есть ли у пользователя есть фото в битре? есть ли пользователь в БД?
            self.UserModel.id = int(uuid)
            psql_user = await self.UserModel.find_by_id_all(session)
            if 'PERSONAL_PHOTO' in usr_data and 'id' in psql_user.keys():
                b24_url = usr_data['PERSONAL_PHOTO']
                # проверим url первоисточника текущей аватарки
                if psql_user['photo_file_id'] is None or psql_user['photo_file_b24_url'] != b24_url:
                    # срабатывает это условие и уходит в else
                    # cтарую фотку - в архив
                    if psql_user['photo_file_b24_url'] is not None and psql_user['photo_file_b24_url'] != b24_url:
                        old_file_id = psql_user['photo_file_id']
                        await File(id=old_file_id).delete_user_img(session)
                    # если есть несоответствие - скачать новую
                    file_data = await File().add_user_img(b24_url=b24_url, uuid=uuid, session=session)

                    if file_data is not False:
                        # обновить данные в pSQL
                        self.UserModel.uuid = uuid
                        await self.UserModel.set_user_photo(file_id=file_data['id'], session=session)
                else:
                    continue

        # вывести отчет по изменениях

        return True

    # def variant_users(self, key):
    #     return B24().variant_key_user(key)

    # def get_dep_usrs(self):
    #     users_data = B24().getUsers()
    #     dep_data = sorted(b24.getDeps(), key=lambda d: int(d['ID']))

    #     result = [["ID", "Название подраздедения", "ФИО руководителя", "ФИО сотрудника"]]
    #     for dep in dep_data:
    #         dep_ID = int(dep['ID'])
    #         if 'UF_HEAD' in dep and dep['UF_HEAD'] != '0':
    #             for usr in users_data:
    #                 if usr['ID'] == dep['UF_HEAD'] and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):
    #                     dep_head = f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}"
    #                     print(dep_ID, dep_head)

    #         for usr in users_data:
    #             if usr["ACTIVE"] and dep_ID in usr['UF_DEPARTMENT'] and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):

    #                 result.append([dep_ID, dep['NAME'], dep_head, f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}"])

    #     return result

    async def has_liked(self, art_id, session):
        from ..base.pSQL.objects.LikesModel import LikesModel
        return await LikesModel(user_id=self.id, art_id=art_id).has_liked(session)

    # день рождения
    async def get_birthday_celebrants(self, date, session):
        # from ..base.pSQL.objects import UserModel
        from ..services.Peer import Peer
        users = await self.UserModel.find_all_celebrants(date=date, session=session)
        # if users:
        #     for user in users:
        #         send_data = {
        #             "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
        #             "uuid_to": int(user['id']),
        #             "activities_id": 14, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
        #             "description": f"Поздравительные баллы. С днем рождения!"
        #         }
        #         send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
                # await session.commit()
        return users

    async def get_all_users(self, session):
        return await self.UserModel.all(session)

    # новые сотрудники
    async def get_new_workers(self, session):
        # from ..base.pSQL.objects import UserModel
        from ..services.Peer import Peer
        users = await self.UserModel.new_workers(session)
        # if users:
        #     for user in users:
        #         send_data = {
        #             "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
        #             "uuid_to": int(user['id']),
        #             "activities_id": 15, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
        #             "description": f"Добро пожаловать в ЭМК!"
        #         }
        #         send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
                # await session.commit()
        #         if send_point['status'] == 'info':
        #             self.UserModel.id = int(user['id'])
        #             user_info = await self.UserModel.find_by_id(session)
        #             if 'email' in user_info and user_info['email']:
        #                 data = {'sender': user_info['email']}
        #                 SendEmail(data=data).send_to_new_wrokers()

        return users

    async def anniversary_in_company(self, session):
        """
        Функция пробегает по всем сотрудникам. Смотрит на их date_register (временно, в будущем поставить поле дата трудоустройства)
        Функция проверяет прошел ли год с момента последней годовщины работы в компании.
        Или может быть наступил юбилей работы в компании
        Подставляет нужный айдишник активности, в случае юбилея отправляет письмо
        ID = 16 - это +год рабоыты в компании
        ID = 19 - это Юбилей 5 лет работы в компании
        ID = 20 - это Юбилей 10 лет работы в компании
        """
        from ..services.Peer import Peer
        from datetime import datetime
        LAUNCH_DATE_OF_CAPITAL_EMK = datetime.strptime("2026-02-01", '%Y-%m-%d')
        DESCRIPTIONS = {'16': "+ год вы с нами!", "19": "5 лет вы с нами!", "20": "10 лет вы с нами!"}
        TODAY = datetime.today().date() # 2026-01-20 00:00:00
        all_users = await self.UserModel.all(session)
        send_data = {
            "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
            "uuid_to": 0,
            "activities_id": 0, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
            "description": "", 
            # "date_register": "2025-03-11T04:00:00+04:00"
            "date_register": TODAY
        }
        for user in all_users:
            if user.active is True:
                if 'date_register' in user.indirect_data and user.indirect_data['date_register'] != '':
                    date_register = user.indirect_data['date_register']
                    if "T" in date_register:
                        date_register = date_register.split("T")[0]
                    convert_date_reg = datetime.strptime(date_register, '%Y-%m-%d')
                    if datetime.today().day == convert_date_reg.day and datetime.today().month == convert_date_reg.month:
                        # СРАНИВАЕМ ДАТЫ И БЕРЕМ СТРОГО ДАТУ ЗАПУСКА КАПИТАЛА ЭМК

                        # ставим для теста текущий год - 2027
                        # teset_date = datetime.strptime("2031-01-29", '%Y-%m-%d')

                        year_diff = abs(datetime.today().year - LAUNCH_DATE_OF_CAPITAL_EMK.year)
                        # year_diff = abs(teset_date.year - LAUNCH_DATE_OF_CAPITAL_EMK.year)
                        if year_diff >= 10:
                            LogsMaker().info_message(f'У пользователя {user.id} годовщина 10 лет')
                            send_data['activities_id'] = 20
                            send_data['description'] = "10 лет вы с нами!"
                            send_data['uuid_to'] = user.id
                            send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
                            # Добавить письмо
                            continue
                        elif year_diff >= 5:
                            LogsMaker().info_message(f'У пользователя {user.id} годовщина 5 лет')
                            send_data['activities_id'] = 19
                            send_data['description'] = "5 лет вы с нами!"
                            send_data['uuid_to'] = user.id
                            send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
                            # Добавить письмо
                            continue
                        elif year_diff >= 1:
                            LogsMaker().info_message(f'Пользователь {user.id} год с нами')
                            send_data['activities_id'] = 16
                            send_data['description'] = "+ год вы с нами!"
                            send_data['uuid_to'] = user.id
                            send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
                            continue
                        else:
                            LogsMaker().info_message(f'разница меньше года {user.id}')
                    else:
                        continue
                        # LogsMaker().info_message('Дата и месяц не совпадает')
                else:
                    continue
                    # LogsMaker().info_message(f'Отсутствует дата регистрации и пользователя {user.id}')



            # send_data = {
            #     "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
            #     "uuid_to": user['id'],
            #     "activities_id": activities_id, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
            #     "description": description, 
            #     # "date_register": "2025-03-11T04:00:00+04:00"
            #     "date_register": TODAY
            # }
            # send_point = await Peer(user_uuid=send_data['uuid_from']).send_auto_points(data=send_data, session=session)
        await session.commit()
        return True

    # дамп данных в эластик
    async def dump_users_data_es(self, session):
        return await self.UserSearchModel.dump(session)

    # для статистики
    def get_user_likes(self):
        from ..base.pSQL.objects.LikesModel import LikesModel
        return LikesModel(user_id=self.id).get_user_likes()

    # Обновляет данные конкретного пользователя
    async def update_inf_from_b24(self, session):
        try:
            res = await B24().getUser(self.id)
            if res:
                usr_data = res[0]
                
                # смотрим логи 
                await self.check_fields_to_update(session=session, b24_data=usr_data)
            
                await self.UserModel.upsert_user(user_data=usr_data, session=session)
                await session.commit()
                # usr_data["ACTIVE"] = False
                if "ACTIVE" in usr_data and usr_data["ACTIVE"] == True:
                    # загружаем фотку:
                    uuid = self.id
                    # есть ли у пользователя есть фото в битре? есть ли пользователь в БД?
                    self.UserModel.id = int(uuid)
                    psql_user = await self.UserModel.find_by_id_all(session)
                    if 'PERSONAL_PHOTO' in usr_data and 'id' in psql_user.keys():

                        b24_url = usr_data['PERSONAL_PHOTO']
                        # print(b24_url, psql_user['photo_file_b24_url'], 'РАЗНЫЕ ФОТКИ')
                        # b24_url = "https://portal.emk.ru/upload/main/b1c/32jhq9uakqf6z56wjku07klwpsde8cbt/Газинский И.В..jpg.png"
                        # проверим url первоисточника текущей аватарки
                        if psql_user['photo_file_id'] is None or psql_user['photo_file_b24_url'] != b24_url:
                            # срабатывает это условие и уходит в else
                            print('РАЗНЫЕ ФОТКИ')
                            # cтарую фотку - в архив
                            # if psql_user['photo_file_b24_url'] is not None and psql_user[
                            #     'photo_file_b24_url'] != b24_url:
                            #     old_file_id = psql_user['photo_file_id']
                            #     await File(id=old_file_id).go_user_photo_archive(session)
                            # если есть несоответствие - скачать новую
                            file_data = await File().add_user_img(b24_url=b24_url, uuid=uuid, session=session)

                            if file_data is not False:
                                # обновить данные в pSQL
                                self.UserModel.uuid = uuid
                                await self.UserModel.set_user_photo(file_id=file_data['id'], session=session)
                    # обновляем эластик
                    await self.update_user_elastic(session)
                return None
            else:
                # не скачиваем фотку у неактивных пользователей
                await self.UserSearchModel.delete_user_from_el_index(user_id=self.id)
            return LogsMaker().ready_status_message(f"Обновлена информация о пользователе с ID = {self.id}")
        except Exception as e:
            return LogsMaker().error_message(
                f'Ошибка при обновлении инф о пользователе update_inf_from_b24 с id = {self.id}: {e}')

    async def update_user_elastic(self, session):
        user_data = await self.search_by_id(session)
        result = await self.UserSearchModel.update_user_el_index(user_data=user_data, session=session)
        if result:
            return LogsMaker().ready_status_message(
                f"Обновлена информация о пользователе с ID = {self.id} в ElasticSearch")
        else:
            LogsMaker().warning_message(f"ElasticSearch не обновил данные пользователя с ID = {self.id}")

    async def find_by_email(self, email, session):
        return await self.UserModel.find_by_email(email, session)

    async def check_fields_to_update(self, session, b24_data):
        fields = [
            'ACTIVE', 'NAME', 'LAST_NAME', 'EMAIL', 'UF_DEPARTMENT', 'WORK_PHONE', 'WORK_POSITION', 'SECOND_NAME',
            'UF_PHONE_INNER', 'UF_USR_DEPARTMENT_MAIN', 'UF_USR_1586854037086',
            'UF_USR_1586861567149', 'UF_USR_1594879216192',
            'UF_USR_1679387413613', 'UF_USR_1696592324977',
            'UF_USR_1705744824758', 'UF_USR_1707225966581',
            'UF_USR_1586853958167'
        ]
        import datetime
        # time_now = datetime.now()
        LogsMaker().info_message(f'ОБНОВЛЯЕМ ИНФУ О ПОЛЬЗОВАТЕЛЕ User с id={self.id}')
        try:
            res = b24_data
            if res == []:
                #удалить у нас пользователя (сделать не активным)
                pass
            else:
                B24_data = res
                self.UserModel.id = int(self.id)
                psql_data = await self.UserModel.find_by_id_all(session)
                if psql_data and psql_data != []:
                    for field in fields:

                        # if field == 'PERSONAL_PHOTO':
                        #     if B24_data[field] == psql_data['photo_file_b24_url']:
                        #         LogsMaker().info_message(f'User с id={self.id} поле {field} не отличается')
                        #     elif B24_data[field] != psql_data['photo_file_b24_url']:
                        #         LogsMaker().info_message(f'User с id={self.id} поле {field} отличается, B24={B24_data[field]}, pSQL={psql_data[field.lower()]}')
                        #     continue
                        # else:
                        #     pass
                        
                        if field.lower() in psql_data['indirect_data']:
                            ind_data = psql_data['indirect_data']
                            if field.lower() in ind_data and field in B24_data:
                                if B24_data[field] == ind_data[field.lower()]:
                                    LogsMaker().info_message(f'User с id={self.id} поле {field} не отличается')
                                elif B24_data[field] != ind_data[field.lower()]:
                                    LogsMaker().info_message(f'User с id={self.id} поле {field} отличается, B24={B24_data[field]}, pSQL={ind_data[field.lower()]}')
                            elif field.lower() not in ind_data and field not in B24_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в pSQL и в B24_data')
                            elif field.lower() not in ind_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в pSQL, B24 = {B24_data[field]}')
                            elif field not in B24_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в B24_data')
                        else:
                            if field.lower() in psql_data and field in B24_data:
                                if B24_data[field] == psql_data[field.lower()]:
                                    LogsMaker().info_message(f'User с id={self.id} поле {field} не отличается')
                                elif B24_data[field] != psql_data[field.lower()]:
                                    LogsMaker().info_message(f'User с id={self.id} поле {field} отличается, B24={B24_data[field]}, pSQL={psql_data[field.lower()]}')
                            elif field.lower() not in psql_data and field not in B24_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в pSQL и в B24_data')
                            elif field.lower() not in psql_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в pSQL, B24 = {B24_data[field]}')
                            elif field not in B24_data:
                                LogsMaker().warning_message(f'Поля {field} нет у User с id={self.id} в B24_data')
                else:
                    LogsMaker().warning_message(f'Новый пользователь!')
                  
            return True 
        except Exception as e:
            return LogsMaker().error_message(f'Произошла ошибка при обновлении пользователя с id={self.id} из Б24: {e}')

    async def get_user_qr(self, user_uuid):
        import os
        from ..services.VCard import User_Vcard
        current_file_path = f'./vcard_db/{user_uuid}.png'
        file_exist = os.path.isfile(current_file_path)
        
        if file_exist:
            return f'https://intranet.emk.ru/api/vcard_files/{user_uuid}.png'
        else:
            filename = User_Vcard(user_uuid).create_qr()
            file_path = f'https://intranet.emk.ru/api/vcard_files/{filename}'
            return file_path

'''
    # def get(self, method="user.get", params={}):
    #     req = f"https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/{method}"
    #     if params != {}:
    #         req += "?"
    #         for parem_key in params.keys():
    #             req += f"&{parem_key}={params[parem_key]}"
    #     response = requests.get(req)
    #     return response.json()

    # def get_all(self, method, params={}):
    #     response = self.get(method)
    #     current = 50
    #     result = response["result"]
    #     keys = []
    #     while current < int(response["total"]):
    #         params["start"] = current
    #         response = self.get(method, params)
    #         curr_result = response["result"]
    #         for curr_keys in curr_result:
    #             for k in curr_keys:
    #                 if k not in keys:
    #                     keys.append(k)
    #                     #print(k)
    #         result = result + curr_result
    #         current += 50

    #     return (keys, result)
'''


# Пользоваетелей можно обновить
@users_router.put("/update", tags=["Пользователь", "Битрикс24"])
async def update_user(session: AsyncSession = Depends(get_async_db)):
    """
    ## Метод `user.get`

    > Метода вызывается один раз, в момент запуска сервиса для загрузки данных с прошлой версии сайта

    Возвращает список всех пользователей из системы Битрикс24 через API метод `user.get`.

    ### Входные параметры
    Метод не принимает параметров.

    ### Возвращаемые данные
    Возвращает список словарей с полными данными пользователей. Каждый пользователь содержит следующие поля (среди прочих):
    - `ID` (int) — уникальный идентификатор пользователя
    - `NAME` (string) — имя пользователя
    - `LAST_NAME` (string) — фамилия пользователя
    - `EMAIL` (string) — email адрес
    - `PERSONAL_PHOTO` (string) — URL фотографии профиля
    - `UF_DEPARTMENT` (list) — список ID подразделений
    - `ACTIVE` (boolean) — статус активности
    - Другие стандартные поля Битрикс24

    ---

    ## Функция `fetch_users_data()`

    Асинхронная функция для полного обновления данных пользователей в системе. Выполняет синхронизацию данных из Битрикс24, включая фотографии профилей и индексацию в Elasticsearch.

    ### Входные параметры
    | Параметр | Тип | Описание | Обязательный |
    |----------|-----|----------|--------------|
    | `session` | `AsyncSession` | Сессия базы данных для выполнения транзакций | Да |

    ### Возвращаемые данные
    ```
    {
        "status": true
    }
    ```

    """

    usr = User()
    return await usr.fetch_users_data(session)

@users_router.put("/update_user_info/{user_id}", tags=["Пользователь", "Битрикс24"])
async def update_user_info(user_id: int, session: AsyncSession = Depends(get_async_db)):
    """
        ## Метод `user.get?ID={ID}`

    Получает данные конкретного пользователя из Битрикс24 по его ID через API метод `user.get`.

    ### Входные параметры
    | Параметр | Тип | Описание | Обязательный |
    |----------|-----|----------|--------------|
    | `ID` | integer | Внутренний идентификатор пользователя в Битрикс24 | Да |

    ### Возвращаемые данные
    Возвращает список с одним элементом - словарем данных пользователя. Пользователь содержит следующие поля:
    - `ID` (int) — внутренний ID пользователя в Битрикс24
    - `NAME` (string) — имя пользователя
    - `LAST_NAME` (string) — фамилия пользователя
    - `EMAIL` (string) — email адрес
    - `PERSONAL_PHOTO` (string) — URL фотографии профиля
    - `ACTIVE` (boolean) — статус активности аккаунта
    - `WORK_POSITION` (string) — должность
    - `WORK_PHONE` (string) — рабочий телефон
    - `PERSONAL_MOBILE` (string) — мобильный телефон
    - `UF_DEPARTMENT` (list) — список ID подразделений
    - Другие стандартные поля пользователя Битрикс24

    ### Пример ответа
    ```json
    [
        {
            "ID": "123",
            "NAME": "Иван",
            "LAST_NAME": "Иванов",
            "EMAIL": "ivanov@company.com",
            "PERSONAL_PHOTO": "https://portal.example.ru/upload/user/123/photo.jpg",
            "ACTIVE": true,
            "WORK_POSITION": "Senior Developer",
            "WORK_PHONE": "+7 (495) 123-45-67",
            "PERSONAL_MOBILE": "+7 (916) 123-45-67",
            "UF_DEPARTMENT": [5, 12]
        }
    ]
    ```

    """
    return await User(id=user_id).update_inf_from_b24(session)
    # return await User(id=user_id).check_fields_to_update(session)
    # return True


# Пользователя можно выгрузить
@users_router.get("/find_by/{id}", tags=["Пользователь"])
async def find_by_user(id: int, session: AsyncSession = Depends(get_async_db)):
    return await User(id).search_by_id(session)

# Пользователя можно выгрузить
@users_router.get("/find_by_id_all/{id}", tags=["Пользователь"])
async def find_by_id_all(id: int, session: AsyncSession = Depends(get_async_db)):
    return await User(id).search_by_id_all(session)
# @users_router.get("/test_update_photo")
# def test_update_photo():
#     return User().set_users_photo()

# поиск по статьям еластик
@users_router.get("/search/full_search_users/{keyword}", tags=["Пользователь"])
def elastic_search(keyword: str):
    from ..base.Elastic.UserSearchModel import UserSearchModel
    return UserSearchModel().elasticsearch_users(key_word=keyword)


# поиск по статьям еластик
@users_router.get("/search/full_search_users_for_editor/{keyword}/{size_res}", tags=["Пользователь"])
def elastic_search(keyword: str, size_res: int):
    from ..base.Elastic.UserSearchModel import UserSearchModel
    return UserSearchModel().elasticsearch_users(key_word=keyword, size_res=size_res)


@users_router.get("/test_update_photo", tags=["Пользователь"])
async def test_update_photo(session: AsyncSession = Depends(get_async_db)):
    return await User().set_users_photo(session)


# запрос для получения списка пользователей у кого в эту дату ДР
@users_router.get("/get_birthday_celebrants/{day_month}", tags=["Пользователь"])
async def birthday_celebrants(day_month: str, session: AsyncSession = Depends(get_async_db)):
    return await User().get_birthday_celebrants(day_month, session=session)


@users_router.post("/test_send_mail", tags=["Пользователь"])
def send_test_mail(data=Body(...)):
    # {"reciever" : str, "title": str, "text": str, "file_url": str}
    return SendEmail(data=data).send_congratulations()

@users_router.post("/send_error", tags=["Пользователь"])
def send_error(data=Body(...)):
    # {"reciever" : str, "title": str, "text": str, "file_url": str}
    return SendEmail(data=data).send_error()

# лайки и просмотры для статистики
@users_router.get("/get_user_likes", tags=["Пользователь"])
async def get_user_likes(user_id: int, session: AsyncSession = Depends(get_async_db)):
    return await User(id=user_id).get_user_likes(session)

#Тестовая для проверки передачи баллов за годовщину
@users_router.get("/anniversary_in_company", tags=["Пользователь"])
async def anniversary_in_company(session: AsyncSession = Depends(get_async_db)):
    return await User().anniversary_in_company(session=session)

@users_router.get("/get_all_users", tags=["Пользователь"])
async def get_all_users(session: AsyncSession = Depends(get_async_db)):
    return await User().get_all_users(session=session)

@users_router.post("/upload_one_user", tags=["Пользователь"])
async def upload_one_user(data=Body(...), session: AsyncSession = Depends(get_async_db)):
    return await User().upload_one_user(user_data=data, session=session)

# @users_router.post("/search_indirect")
# def search_indirect(key_word):
#     #будет работать через elasticsearch
#     return UserSearchModel().search_indirect(key_word)


# @users_router.post("/search")
# def search_user(jsn=Body()):
#     #будет работать через elasticsearch
#     return UserSearchModel().search_model(jsn)

# Пользователя можно найти
# @users_router.post("/search/{username}")
# def search_user(username: str): # jsn=Body()
#     return UserSearchModel().search_by_name(username)

# загрузить дату в ES
# @users_router.put("/elastic_data")
# def upload_users_to_es():
#     return UserSearchModel().dump()


# лайки и просмотры для статистики
# @users_router.post("/has_liked")
# def has_liked(user_id: int, art_id: int):
#     return User(id=user_id).has_liked(art_id)

# @users_router.get("/get_user_uuid_likes")
# def get_user_uuid_likes(user_uuid: str):
#     return User(uuid=user_uuid).has_liked_by_uuid()