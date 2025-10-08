import os
from dotenv import load_dotenv
import redis
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid
from pydantic import BaseModel

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from ..base.RedisStorage import RedisStorage
from src.services.LogsMaker import LogsMaker
from ..model.User import User

import json


auth_router = APIRouter(prefix="/auth_router", tags=["Авторизвция"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Загрузка переменных окружения
load_dotenv()



# class UserSession(BaseModel):
#     ID : srt
#     user_uuid: str
#     username: str
#     email: str
#     full_name: str
#     expires_at: str



class AuthService:
    def __init__(self):
        # Настройки Redis из .env
        redis_host = "redis"
        redis_port = 6379
        redis_db = 0
        redis_username = os.getenv("user")
        redis_password = os.getenv("pswd")

        # Инициализация Redis с аутентификацией
        self.redis = RedisStorage()

        # Настройки Active Directory из .env
        self.ldap_server = os.getenv("LDAP_SERVER")
        self.ldap_domain = os.getenv("LDAP_DOMAIN")

        self.session_ttl = timedelta(minutes=240)

    async def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:

        LogsMaker().info_message(f"login = {username}, password = {password}")

        """Аутентификация пользователя"""
        # Проверка подключения к Redis
        if not self.redis.check_connection():
            return LogsMaker().fatal_message("Cannot connect to Redis")

        # Проверяем учетные данные в AD
        user_uuid = self.check_ad_credentials(username, password)
        if user_uuid is not None and "GUID" in user_uuid:
            user_uuid = user_uuid['GUID']
        else:
            return LogsMaker.error_message("Auth error! Invalid login or password!")
        
        

        # Получаем дополнительные данные пользователя (замените на ваш метод)
        user_data = self.get_user_data(user_uuid)
        # print(user_data, user_uuid)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! есть пользователи без UUID
        #if user_data is None:
            #получаю ID по GUID или по почте
            #плучаю данные по ID
            #сохраняю в БД GUID


        session_id = str(uuid.uuid4())
        dt = datetime.now() + self.session_ttl
        # session_data = UserSession(
        #     #ID=user_data.get("ID", ""),
        #     user_uuid=user_uuid,
        #     username=username,
        #     email=user_data.get("email", ""),
        #     full_name=user_data.get("full_name", ""),
        #     expires_at=dt.strftime('%Y-%m-%d %H:%M:%S')
        # ).dict()

        session_data = {
            "ID" : user_data.get("ID", ""),
            "user_uuid" : user_uuid,
            "username" : username,
            "email" : user_data.get("email", ""),
            "full_name" : user_data.get("full_name", ""),
            "expires_at" : dt.strftime('%Y-%m-%d %H:%M:%S')
        }

        #print(session_data)

        # если пользователь валидный проверяем, нет ли его сессии в Rdis
        ses_find = self.redis.find_session_id(user_uuid, username)
        if ses_find is None:
            self.redis.save_session(session_id, session_data)
        else:
            session_id = ses_find[8:]

        return {
            "session_id": session_id,
            "user": session_data
        }

    '''
    def check_ad_credentials(self, username: str, password: str) -> Optional[str]:
        """Проверка учетных данных в AD"""
        try:

            #доступ админа
            if username in os.getenv("user") and password == os.getenv("pswd"):
                return {'GUID': "c97f2043-7e8a-4b0f-9bf7-e6bfcf9fccb6"}

            server = Server(self.ldap_server, get_info=ALL)
            conn = Connection(
                server,
                user=f"{username}@{self.ldap_domain}",
                password=password,
                authentication="SIMPLE"
            )

            if not conn.bind():
                return None

            search_filter = f"(sAMAccountName={username})"
            search_base = f"dc=imp,dc=int"
            conn.search(
                search_base,
                search_filter,
                search_scope=SUBTREE,
                attributes=[
                    'cn',
                    'mail',
                    'displayName',
                    'sAMAccountName',
                    'objectGUID',
                    'objectSID',
                    'userPrincipalName',
                    'distinguishedName',
                    'uidNumber',
                    'employeeID',
                    'employeeNumber',
                ]
            )

            if len(conn.entries) > 0:
                user_entry = conn.entries[0]

                # Преобразуем objectGUID
                object_guid = user_entry.objectGUID.value
                user_uuid = str(object_guid)[1:-1]

                # Преобразуем objectSID
                object_sid = user_entry.objectSID.value
                user_sid = str(object_sid)

                user_details = {
                    'cn': user_entry.cn.value,
                    'mail': user_entry.mail.value,
                    'displayName': user_entry.displayName.value,
                    'sAMAccountName': user_entry.sAMAccountName.value,
                    'GUID': user_uuid,
                    'SID': user_sid,
                    'userPrincipalName': user_entry.userPrincipalName.value,
                    'distinguishedName': user_entry.distinguishedName.value,
                    'uidNumber': user_entry.uidNumber.value if 'uidNumber' in user_entry else None,
                    'employeeID': user_entry.employeeID.value if 'employeeID' in user_entry else None,
                    'employeeNumber': user_entry.employeeNumber.value if 'employeeNumber' in user_entry else None,
                }

            else:
                return {"err" : "Пользователь не найден"}

            if not conn.entries:
                return None

            return user_details #str(conn.entries[0].objectGUID.value)

        except Exception as e:
            print(f"AD error: {e}")
            return None
        finally:
            if 'conn' in locals() and conn.bound:
                conn.unbind()
    '''

    #ЗАГЛУШКА
    def check_ad_credentials(self, username, password):
        #хватаю из json пользователей по логину для демки и возваращаю GUID
        user_data_file = open("./src/base/test_AD_users.json", "r")
        user_json = json.load(user_data_file)
        user_data_file.close()
        
        for user_data in user_json:
            if username == user_data["login"]:
                log_str = f"!!!!!!!!!!!! {username} подключился к серверу!!!!!!!!!!!!"
                # ret_str = "#"*len(log_str)
                LogsMaker().ready_status_message(f"{log_str}")
                return user_data
        
        return None
    

    # def check_admin_credentials(self, username, password):
    #     #хватаю из json пользователей по логину для демки и возваращаю GUID
    #     user_data_file = open("./src/base/admin_users.json", "r")
    #     user_json = json.load(user_data_file)
    #     user_data_file.close()
        
    #     for user_data in user_json:
    #         if username == user_data["login"] and password == ["password"]:
    #             log_str = f"!!!!!!!!!!!! ADMIN {username} подключился к серверу!!!!!!!!!!!!"
    #             # ret_str = "#"*len(log_str)
    #             LogsMaker().ready_status_message(f"{log_str}")
    #             return user_data
        
    #     return None
    

    #ЗАГЛУШКА2
    def check_ad_credentials(self, username, password):
        #хватаю uuid пользователя по логину
        user_uuid = User().find_by_email(username)
        if user_uuid:
            log_str = f"!!!!!!!!!!!! {username} подключился к серверу!!!!!!!!!!!!"
            # ret_str = "#"*len(log_str)
            LogsMaker().ready_status_message(f"{log_str}")
            user_data = {"login": username, "GUID": user_uuid}
            return user_data
        
        return None
    


    def get_user_data(self, user_uuid: str):
        # Хватаем данные из pSQL
        return User(uuid = user_uuid).user_inf_by_uuid()

    def validate_session(self, session_id: str) -> dict :#Optional[UserSession]:
        """
        Проверка валидности сессии

        :param session_id: Идентификатор сессии
        :return: Данные сессии или None если сессия недействительна
        """
        if not session_id:
            return None


        # Получаем данные сессии
        session_data = self.redis.get_session(session_id)

        if not session_data:
            return False

        try:
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            if datetime.now() > expires_at:
                self.redis.delete_session(session_id)
                return False

            # Обновляем TTL сессии (скользящее окно)
            self.redis.update_session_ttl(session_id, self.session_ttl)

            #return UserSession(**session_data)
            return session_data

        except (KeyError, ValueError) as e:
            logging.error(f"Invalid session data format: {e}")
            self.redis.delete_session(session_id)
            return False

    def logout(self, session_id: str) -> None:
        """
        Завершение сессии

        :param session_id: Идентификатор сессии
        """
        self.redis.delete_session(session_id)

    def get_user_by_seesion_id(self, session_id : str):
        session  = AuthService().validate_session(session_id)
        if not session :
            return None
        return session


import smtplib

server_mail_host = "smtp.emk.ru:587"

def try_mail(login, password):
    try:
        server = smtplib.SMTP(server_mail_host)
        server.starttls()
        server.login(login, password)
        

        status = server.noop()[0]
        server.quit()
        if status == 250:
            return True
    except smtplib.SMTPAuthenticationError as e:
        return False
    except smtplib.SMTPException as e:
        return False
    except Exception as e:
        return False

@auth_router.post("/auth")
async def authentication(response : Response, data = Body()):
    if "login" in data and "password" in data: #login : str, password : str,
        login = data["login"]
        password = data["password"]
    else:
        # return await LogsMaker().warning_message(message="Login or Password has missing")
        return LogsMaker().warning_message(message="Login or Password has missing")
    
    # ВРЕМЕННО ПО ПОЧТЕ !!!!!!!!!!!!!!!!!!
    check_email = try_mail(login, password)
    if check_email == False:
        # return await LogsMaker().warning_message(message="Invalid credentials")
        LogsMaker().info_message(f"login = {login}, password = {password} Пользователя у которого не получилось зайти")
        return LogsMaker().warning_message(message="Invalid credentials")
    # ВРЕМЕННО ПО ПОЧТЕ !!!!!!!!!!!!!!!!!!

    session = await AuthService().authenticate(login, password)
    if not session :
        # return await LogsMaker().warning_message(message="Invalid credentials")
        return LogsMaker().warning_message(message="Invalid credentials")
    elif "err" in session.keys():
        # return await LogsMaker().warning_message(message=session["err"])
        return LogsMaker().warning_message(message=session["err"])
    access_token = session["session_id"]

    #response.headers["Authorization"] = access_token

    response.set_cookie(key="Authorization", value=access_token)

    #return JSONResponse(content=session, headers=response.headers)
    return session
        
@auth_router.get("/check")
async def check_token(request : Request):
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")

    session  = AuthService().validate_session(token)
    if not session :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    return session
