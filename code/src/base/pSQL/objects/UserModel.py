from sqlalchemy import text, update
from sqlalchemy.sql.expression import func, select
from sqlalchemy.orm import Session

from bson.objectid import ObjectId

from datetime import datetime




from .DepartmentModel import DepartmentModel

import json

from sqlalchemy.exc import SQLAlchemyError
from .App import get_db
db_gen = get_db()
database = next(db_gen)

#!!!!!!!!!!!!!!!
#from src.model.File import File
from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Пользователей")
#!!!!!!!!!!!!!!!



class UserModel:
    def __init__(self, Id=None, uuid=None):
        self.id = Id
        self.uuid = uuid
        from ..models.User import User
        self.user = User#.__table__
        #self.inspector = inspect(engine)

        # from .App import db
        # database = db
    
    def create_new_user_view(self ):
        from .App import engine
        try:
            # тут создать представление
            view = text(f"CREATE VIEW NewUsers AS\n"
            f"SELECT users.id,\n"
                f"users.active,\n"
                f"users.last_name,\n"
                f"users.name,\n"
                f"users.second_name,\n"
                f"to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) AS dat,\n"
                f"users.indirect_data,\n"
                f"users.photo_file_id\n"
            f"FROM users\n"
            f"WHERE users.active = true AND to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) >= (date_trunc('week'::text, CURRENT_DATE::timestamp with time zone) - '14 days'::interval)\n"
            # f"WHERE users.active = true AND to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) >= (CURRENT_DATE - INTERVAL '14 days')\n"
            f"ORDER BY (to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text));"
            )

            with engine.connect() as connection:
                connection.execute(view)
                connection.commit()
                connection.close()
            
            LogsMaker().info_message("Создано представление для получения новых сотрудников")

        except SQLAlchemyError as e:
            database.rollback()
            LogsMaker().error_message(str(e))

    def upsert_user(self, user_data : dict):
        from .App import engine
        """
        Добавляет или обновляет запись в таблице.
        user_data: словарь с данными пользователя
        """

        #валидация
        new_user_data = dict()
        for key in user_data.keys():
            # валидация
            if key == 'ID':
                new_user_data["id"] = int(user_data[key])
            elif key == 'XML_ID':
                new_user_data["uuid"] = user_data["XML_ID"][3:]
            else:
                new_user_data[key.lower()] = user_data[key]
        user_data = new_user_data

        #проверить по id есть ли такой пользователь
        try:
            #usr = db.query(self.user).get(user_data['id'])
            #usr = db.query(User).filter(self.user.id == user_data['id']).first()

            q = database.query(self.user).filter(self.user.id == user_data["id"])
            usr = database.query(q.exists()).scalar()  # returns True or False

            DB_columns = ['uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']

            #если есть - проверить необходимость обновления
            if usr:
                #user = db.query(self.user).filter(User.id == user_data["id"]).first()
                user = database.query(self.user).get(user_data['id'])

                #проверить есть ли изменения
                need_update = False

                #проверка основных параметров
                new_params = []
                for column in DB_columns:
                    if user_data.get(column) != user.__dict__[column]:
                        if column == 'personal_birthday':
                            # обработка дат
                            if user_data.get('personal_birthday') != "":
                                dt_new = datetime.strptime(user_data.get('personal_birthday').split('T')[0], '%Y-%m-%d').date()
                                cur_dt = f"\'{datetime.strptime(user_data.get('personal_birthday').split('T')[0], '%Y-%m-%d').date()}  04:00:00\'"
                            else:
                                dt_new = None

                            if user.personal_birthday is not None:
                                dt_old = user.personal_birthday.date()
                            else:
                                dt_old = user.personal_birthday

                            if dt_new != dt_old:
                                need_update = True
                                new_params.append(column)
                                user.__dict__[column] = dt_new
                                #print(user.id , column, dt_new)
                        else:
                            need_update = True
                            new_params.append(column)
                            if user_data.get(column) == "":
                                user.__dict__[column] = "NULL"
                            else:
                                user.__dict__[column] = f"\'{user_data.get(column)}\'"
                            #print(user.id, column, user_data.get(column))

                # если есть изменения - внести
                if need_update:
                    for cls in new_params:
                        sql = text(f"UPDATE {self.user.__tablename__} SET {cls} = {user.__dict__[cls]} WHERE id = {user.id}")
                        with engine.connect() as connection:
                            connection.execute(sql, user_data)
                            connection.commit()
                    
                    LogsMaker().info_message(f"Внесены изменения в данные пользователя с id = {user.id}")


                # проверить есть ли изменения
                need_update_indirect_data = False
                #проверка доп. параметров
                for key in user_data.keys():
                    if key not in DB_columns:
                        if (key not in user.indirect_data) or (user_data[key] != user.indirect_data[key]):
                            #изменить, если требуется
                            need_update_indirect_data = True
                            user.indirect_data[key] = user_data[key]
                            #print(key, user.indirect_data[key])

                # если есть изменения - внести
                if need_update_indirect_data:
                    indirect_jsnb = json.dumps(user.indirect_data)
                    sql = text(f"UPDATE {self.user.__tablename__} SET indirect_data = \'{indirect_jsnb}\' WHERE id = {user.id}")
                    with engine.connect() as connection:
                        connection.execute(sql, user_data)
                        connection.commit()
                
                LogsMaker().info_message(f"Внесены изменения в данные пользователя с id = {user.id}")



            #если нет - добавить
            else:
                # Формируем SQL-запрос
                columns = "id"
                values = f"{user_data['id']}"
                meta = dict()
                # Все данные пользователя
                for key in user_data.keys():
                    #если это обязательные поля
                    if key in DB_columns:
                        #отдельно обработаем active так это не строковый формат
                        if key == 'active':
                            columns += f", active"
                            values += f", {user_data[key]}"
                        #если дата - пустая строка
                        elif key == 'personal_birthday' and user_data[key] == "":
                            columns += f", {key}"
                            values += f", NULL"
                        #потом остальные
                        else:
                            columns += f", {key}"
                            values += f", \'{user_data[key]}\'"

                    #оставшиеся - в метаданные
                    else:
                        meta[key] = user_data[key]



                columns += f", indirect_data"
                indirect_jsnb = json.dumps(meta)
                values += f", \'{indirect_jsnb}\'"
                # Запрос
                sql = text(f"INSERT INTO {self.user.__tablename__} ({columns}) VALUES ({values})")

                # Выполняем SQL-запрос
                with engine.connect() as connection:
                    connection.execute(sql, user_data)
                    connection.commit()
                user_id = user_data["id"]
                LogsMaker().info_message(f"Создан пользователь с id = {user_id}")

            
            
        except SQLAlchemyError as e:
            database.rollback()
            #print(f"An error occurred: {e}")
            LogsMaker().error_message(str(e))


    def find_by_id_all(self):
        from src.model.File import File
        from .App import DOMAIN
        """
        Ищет пользователя по id
        """
        user = database.query(self.user).filter(self.user.id == self.id).first()
        result = dict()
        DB_columns = ['id', 'uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']
        
        if user is not None:
            for key in DB_columns:
                result[key] = user.__dict__[key]

            indirect_data = user.indirect_data
            list_departs = []
            list_departs_id = []
            if len(indirect_data['uf_department']) != 0:
                for dep in indirect_data['uf_department']:
                    dedep = DepartmentModel(dep).find_dep_by_id()
                    if type(dedep) == type(dict()):
                        if 'name' in dedep:
                            list_departs.append(dedep['name'])
                            list_departs_id.append(dedep['id'])
                        else:
                            print(dedep)
                    else: #если объект
                        for dp in dedep:
                            list_departs.append(dp.__dict__['name'])
                            list_departs_id.append(dp.__dict__['id'])

            if "uf_usr_department_main" in indirect_data:
                #print(indirect_data["uf_usr_department_main"])
                dedep = DepartmentModel(Id=indirect_data["uf_usr_department_main"]).find_dep_by_id()
                #print(dedep)
                indirect_data["uf_usr_department_main"] = dedep[0].name

            indirect_data['uf_department'] = list_departs
            indirect_data['uf_department_id'] = list_departs_id
            result['indirect_data'] = indirect_data
            
            #информация о фото
            #вывод ID фотографии пользователя
            result['photo_file_id'] = user.__dict__['photo_file_id']
            if 'photo_file_id' in user.__dict__.keys() and user.__dict__['photo_file_id'] is not None:
                photo_inf = File(id=user.__dict__['photo_file_id']).get_users_photo()

                #вывод URL фотографии пользователя
                url = photo_inf['URL']
                result['photo_file_url'] = f"{DOMAIN}{url}"
                
                result['photo_file_b24_url'] = photo_inf['b24_url']
            else:
                result['photo_file_id'] = None
                result['photo_file_url'] = None
                result['photo_file_b24_url'] = None
  
            return result
        else:

            LogsMaker().warning_message(f"Invalid user id = {self.id}")
            return None

    def find_by_id(self):
        from src.model.File import File
        from .App import DOMAIN
        """
        Ищет пользователя по id
        """
        user = database.query(self.user).filter(self.user.id == self.id, self.user.active == True).first()
        result = dict()
        DB_columns = ['id', 'uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']
        
        if user is not None:
            for key in DB_columns:
                result[key] = user.__dict__[key]

            indirect_data = user.indirect_data
            list_departs = []
            list_departs_id = []
            if len(indirect_data['uf_department']) != 0:
                for dep in indirect_data['uf_department']:
                    dedep = DepartmentModel(dep).find_dep_by_id()
                    if type(dedep) == type(dict()):
                        if 'name' in dedep:
                            list_departs.append(dedep['name'])
                            list_departs_id.append(dedep['id'])
                        else:
                            print(dedep)
                    else: #если объект
                        for dp in dedep:
                            list_departs.append(dp.__dict__['name'])
                            list_departs_id.append(dp.__dict__['id'])

            if "uf_usr_department_main" in indirect_data:
                #print(indirect_data["uf_usr_department_main"])
                dedep = DepartmentModel(Id=indirect_data["uf_usr_department_main"]).find_dep_by_id()
                #print(dedep)
                indirect_data["uf_usr_department_main"] = dedep[0].name

            indirect_data['uf_department'] = list_departs
            indirect_data['uf_department_id'] = list_departs_id
            result['indirect_data'] = indirect_data
            
            #информация о фото
            #вывод ID фотографии пользователя
            result['photo_file_id'] = user.__dict__['photo_file_id']
            if 'photo_file_id' in user.__dict__.keys() and user.__dict__['photo_file_id'] is not None:
                photo_inf = File(id=user.__dict__['photo_file_id']).get_users_photo()

                #вывод URL фотографии пользователя
                url = photo_inf['URL']
                result['photo_file_url'] = f"{DOMAIN}{url}"
                
                result['photo_file_b24_url'] = photo_inf['b24_url']
            else:
                result['photo_file_id'] = None
                result['photo_file_url'] = None
                result['photo_file_b24_url'] = None
  
            return result

        else:

            LogsMaker().warning_message(f"Invalid user id = {self.id}")
            '''
            user_not_found = {
                "id": 9999999,
                "uuid": "",
                "active": True,
                "name": "Не",
                "last_name": "Пользователь",
                "second_name": "Найден",
                "email": "",
                "personal_mobile": "",
                "uf_phone_inner": "",
                "personal_city": "",
                "personal_gender": "M",
                "personal_birthday": "2025-07-04T04:00:00",
                "photo_file_id": None,
                "photo_file_url": None,
                "photo_file_b24_url": None,
                "indirect_data": {
                    "id": 2375,
                    "title": "",
                    "work_fax": "",
                    "work_www": "",
                    "work_zip": "",
                    "is_online": "N",
                    "time_zone": "Europe/Saratov",
                    "user_type": "employee",
                    "work_city": "",
                    "last_login": "",
                    "work_notes": "",
                    "work_pager": "",
                    "work_phone": "",
                    "work_state": "",
                    "timestamp_x": {},
                    "work_street": "",
                    "personal_fax": "",
                    "personal_icq": "",
                    "personal_www": "",
                    "personal_zip": "",
                    "work_company": "",
                    "work_country": "0",
                    "work_mailbox": "",
                    "work_profile": "",
                    "date_register": "",
                    "uf_department": [],
                    "work_position": "Не определено",
                    "personal_notes": "",
                    "personal_pager": "",
                    "personal_phone": "",
                    "personal_photo": "",
                    "personal_state": "",
                    "personal_street": "",
                    "work_department": "",
                    "personal_country": "0",
                    "personal_mailbox": "",
                    "time_zone_offset": "0",
                    "last_activity_date": {},
                    "uf_employment_date": "",
                    "personal_profession": "",
                    "uf_usr_1586854037086": "",
                    "uf_usr_1586861567149": "",
                    "uf_usr_1594879216192": "",
                    "uf_usr_1679387413613": [],
                    "uf_usr_1696592324977": [""],
                    "uf_usr_1705744824758": [""],
                    "uf_usr_1707225966581": False
                }
            }
            '''
            return None

    def find_by_uuid(self):
        try:
            user = database.query(self.user).filter(self.user.uuid == self.uuid).first()

            if user is not None:
                return {
                    "ID": user.id,
                    "email" : user.email,
                    "full_name" : f"{user.second_name} {user.name} {user.last_name}"
                }
            else:
                return LogsMaker().warning_message("Invalid user uuid")
        except Exception as e:
            LogsMaker().error_message(str(e))

    #временно для авторизации
    def find_by_email(self, email):
        user_uuid = database.query(self.user.uuid).filter(self.user.email == email).scalar()
        return user_uuid
    
    def all(self):
        result = database.query(self.user).all()

        return result
    
    def set_user_photo(self, file_id):
        from .App import engine

        #update(User).values({"photo_file_id": file_id, "photo_file_url" : file_url}).where(User.id == self.id)
        with Session(engine) as session:
            stmt = update(self.user).where(self.user.id == self.id).values(photo_file_id=str(file_id))
            result = session.execute(stmt)
            session.commit()
            session.close()

            return result
    
    def find_all_celebrants(self, date):
        from src.model.File import File
        from .App import DOMAIN
        """
        Выводит список пользователей, у кого день рождение в этот день (date)
        Важно! Не выводит пользователей, у кого департамент Аксиома и у кого нет фото
        """
        normal_list = []
        users = database.query(self.user).filter(func.to_char(self.user.personal_birthday, 'DD.MM') == date).all()
        for usr in users:
            user = usr.__dict__
            if 112 in user['indirect_data']['uf_department']:
                pass
            else:
                if user['active'] and user['photo_file_id'] is not None:
                # if user['active']:
                    user_info = {}
                    indirect_data = user['indirect_data']
                    list_departs = []
                    if len(indirect_data['uf_department']) != 0:
                        for dep in indirect_data['uf_department']:
                            if isinstance(dep, int):
                                dep_str = DepartmentModel(dep).find_dep_by_id()
                                for de in dep_str:
                                    list_departs.append(de.__dict__['name'])
                    
                            
                    indirect_data['uf_department'] = list_departs
                    # добавляем только нужную информацию
                    user_info = {}
                    user_image = File(id = ObjectId(user['photo_file_id'])).get_users_photo()
                    user_info['id'] = user['id']
                    if user['second_name'] == '' or user['second_name'] is None:
                        user_info['user_fio'] = f'{user["last_name"]} {user["name"]}'
                    else:
                        user_info['user_fio'] = f'{user["last_name"]} {user["name"]} {user["second_name"]}'
                    user_info['position'] = indirect_data['work_position']
                    user_info['department'] = indirect_data['uf_department']
                    if "uf_usr_department_main" in indirect_data:
                        dedep = DepartmentModel(indirect_data["uf_usr_department_main"]).find_dep_by_id()
                        user_info['uf_usr_department_main'] = dedep[0].name
                    user_info['image'] =  f'{DOMAIN}{user_image["URL"]}'
                    
                    normal_list.append(user_info)

        return normal_list

    def new_workers(self):
        from src.model.File import File
        from .App import DOMAIN
        from .App import NewUser
        # query = select().select_from(demo_view).order_by(demo_view.c.created_at)
        result = database.execute(select(NewUser)).fetchall() # приносит кортеж, где индекс(0) - id, индекс(1) - active, индекс(2) - last_name, индекс(3) - name, индекс(4) - second_name,
        # индекс(5) - dat, индекс(6) - indirect_data, индекс(7) - photo_file_id
        
        users = []
        for res in result:
            
            user = list(res)
            if 112 in user[6]['uf_department']:
                pass
            else:
                if user[1] and user[7] is not None:
                    user_info = {}
                    indirect_data = user[6]
                    list_departs = []
                    if len(indirect_data['uf_department']) != 0:
                        for dep in indirect_data['uf_department']:
                            dep_str = DepartmentModel(dep).find_dep_by_id()
                            for de in dep_str:
                                list_departs.append(de.__dict__['name'])
                    if "uf_usr_department_main" in indirect_data:
                        dedep = DepartmentModel(indirect_data["uf_usr_department_main"]).find_dep_by_id()
                        indirect_data["uf_usr_department_main"] = dedep[0].name
                    indirect_data['uf_department'] = list_departs
                    # добавляем только нужную информацию
                    user_info = {}
                    user_image = File(user[7]).get_users_photo()
                    
                    user_info['id'] = user[0]
                    if user[4] == '' or user[4] is None:
                        user_info['user_fio'] = f'{user[2]} {user[3]}'
                    else:
                        user_info['user_fio'] = f'{user[2]} {user[3]} {user[4]}'
                    user_info['position'] = indirect_data['work_position']
                    user_info['department'] = indirect_data['uf_department']
                    user_info['image'] = f'{DOMAIN}{user_image["URL"]}'
                    users.append(user_info)

        return users
    


    """
    def put_uf_depart(self, usr_dep):
        
        Выводит пользователей и их uf_department
        
        all_users = []
        print('Выполняю запрос')
        users = database.execute(select(self.user)).scalars().all()
        print('Запрос выполнен')
        for user in users:
            
            if user is not None:
                result = dict()
                user_id = getattr(user, 'id', None)
                user_indirict = getattr(user, 'indirect_data')
                result['id'] = user_id
                result['uf_department'] = user_indirict['uf_department']
                for deps_id in result:
                    #проверка
                    #если пользователь есть
                    #если нет - добавить
                # if len(result['uf_department']) > 1:
                #     print(f'у чувака {user_id} НЕСКОЛЬКО ({len(result['uf_department'])}) департаментов')
                # elif len(result['uf_department']) == 0:
                #     print(f'у чувака {user_id} 0 департаментов')
                all_users.append(result)
            else:
                return f'пустой'
        return all_users """