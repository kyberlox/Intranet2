import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid
import json
import logging

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests

from ..base.RedisStorage import RedisStorage
from src.services.LogsMaker import LogsMaker
#ROOT
import re
from ..model.User import User
from sqlalchemy.ext.asyncio import AsyncSession
from ..base.pSQL.objects.App import get_async_db

# Загрузка переменных окружения
load_dotenv()

auth_router = APIRouter(prefix="/auth_router")



class AuthService: 
    def __init__(self):
        # Настройки Redis
        redis_host = "redis"
        redis_port = 6379
        redis_db = 0
        redis_username = os.getenv("user")
        redis_password = os.getenv("pswd")

        self.redis = RedisStorage()
        
        # Конфигурация Bitrix24 OAuth
        self.client_id = os.getenv("BITRIX_CLIENT_ID", "local.6942c425a760a9.02715487")
        self.client_secret = os.getenv("BITRIX_CLIENT_SECRET", "IbJibGiElhqSaem40Z6DWA6TJOI5KYsvYG9O9xnYJxC5EOuY4T")
        self.redirect_uri = os.getenv("BITRIX_REDIRECT_URI", "https://intranet.emk.ru/api/auth_router/auth")
        self.bitrix_domain = os.getenv("BITRIX_DOMAIN", "https://portal.emk.ru")
        
        # Время жизни токенов и сессий
        self.access_token_ttl = timedelta(hours=1)  # Время жизни access_token в Bitrix24
        self.refresh_token_ttl = timedelta(days=30)  # Время жизни refresh_token
        self.session_ttl = timedelta(days=7)  # Время жизни сессии
        self.session_sliding_window = timedelta(minutes=15)  # Интервал для скользящего обновления сессии

    async def get_auth_url(self, state: str = None) -> str:
        """Генерация URL для авторизации в Bitrix24"""
        if not state:
            state = str(uuid.uuid4())
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "user",
            "state": state
        }
        
        auth_url = f"{self.bitrix_domain}/oauth/authorize/"
        return f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    async def exchange_code_for_tokens(self, code: str) -> Optional[Dict[str, Any]]:
        """Обмен кода авторизации на токены"""
        token_url = "https://oauth.bitrix24.tech/oauth/token/"
        
        params = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            response = requests.get(token_url, params=params)
            response.raise_for_status()
            tokens = response.json()
            
            # Добавляем время истечения токенов
            tokens["access_token_expires_at"] = (
                datetime.now() + self.access_token_ttl
            ).isoformat()
            tokens["refresh_token_expires_at"] = (
                datetime.now() + self.refresh_token_ttl
            ).isoformat()
            
            return tokens
            
        except requests.RequestException as e:
            LogsMaker().error_message(f"Token exchange failed: {str(e)}")
            return None

    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Обновление access_token с помощью refresh_token"""
        token_url = f"{self.bitrix_domain}/oauth/token/"
        
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token
        }
        
        try:
            response = requests.get(token_url, params=params)
            response.raise_for_status()
            tokens = response.json()
            
            # Обновляем время истечения
            tokens["access_token_expires_at"] = (
                datetime.now() + self.access_token_ttl
            ).isoformat()
            
            # Если пришел новый refresh_token, обновляем его время
            if "refresh_token" in tokens:
                tokens["refresh_token_expires_at"] = (
                    datetime.now() + self.refresh_token_ttl
                ).isoformat()
            
            return tokens
            
        except requests.RequestException as e:
            LogsMaker().error_message(f"Token refresh failed: {str(e)}")
            return None

    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе из Bitrix24"""
        user_info_url = f"{self.bitrix_domain}/rest/user.current.json"
        
        params = {
            "auth": access_token
        }
        print(access_token, 'access_token')
        try:
            response = requests.get(user_info_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if "result" in result:
                return result["result"]
            return None
            
        except requests.RequestException as e:
            LogsMaker().error_message(f"Failed to get user info: {str(e)}")
            return None

    async def create_session(self, tokens: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Создание новой сессии"""
        session_id = str(uuid.uuid4())
        session_expires_at = datetime.now() + self.session_ttl
        session_data = {
            "session_id": session_id,
            "user_id": tokens["user_id"],
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "access_token_expires_at": tokens["access_token_expires_at"],
            "refresh_token_expires_at": tokens["refresh_token_expires_at"],
            "session_expires_at": session_expires_at.isoformat(),
            "user_info": user_info,
            "last_activity": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "member_id": tokens["member_id"]
        }
        # Сохраняем сессию в Redis
        self.redis.save_session(
            key=session_id,
            data=session_data,
            ttl=int(self.session_ttl.total_seconds())
        )
        
        # Также сохраняем связь user_id -> session_id для поиска
        user_sessions_key = f"user_sessions:{tokens['user_id']}"
        self.redis.add_to_set(user_sessions_key, session_id)
        
        return {
            "session_id": session_id,
            "session_expires_at": session_expires_at.isoformat(),
            "user": user_info,
            "member_id": tokens["member_id"]
        }

    def get_user_by_seesion_id(self, session_id: str):
        session = AuthService().validate_and_refresh_session(session_id)
        if not session:
            return None
        return session

    def validate_and_refresh_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Проверка и обновление сессии при необходимости"""
        session_data = self.redis.get_session(session_id)
        
        if not session_data:
            return None
        
        now = datetime.now()
        session_expires_at = datetime.fromisoformat(session_data["session_expires_at"])
        
        # Проверяем истекла ли сессия
        if now > session_expires_at:
            self.delete_session(session_id)
            return None
        
        # Проверяем access_token
        access_token_expires_at = datetime.fromisoformat(
            session_data["access_token_expires_at"]
        )
        
        # Если access_token истек или скоро истекает (менее 5 минут), обновляем его
        if now > access_token_expires_at - timedelta(minutes=5):
            refreshed_tokens = self.refresh_access_token_sync(
                session_data["refresh_token"]
            )
            
            if refreshed_tokens:
                # Обновляем токены в сессии
                session_data["access_token"] = refreshed_tokens["access_token"]
                session_data["access_token_expires_at"] = refreshed_tokens["access_token_expires_at"]
                session_data["member_id"] = refreshed_tokens["member_id"]
                
                if "refresh_token" in refreshed_tokens:
                    session_data["refresh_token"] = refreshed_tokens["refresh_token"]
                    session_data["refresh_token_expires_at"] = refreshed_tokens["refresh_token_expires_at"]
                
                # Обновляем сессию в Redis
                self.redis.save_session(
                    key=session_id,
                    data=session_data,
                    ttl=int(self.session_ttl.total_seconds())
                )
            else:
                # Не удалось обновить токен - удаляем сессию
                self.delete_session(session_id)
                return None
        
        # Применяем скользящее окно для сессии
        last_activity = datetime.fromisoformat(session_data["last_activity"])
        
        if now > last_activity + self.session_sliding_window:
            # Обновляем время последней активности и продлеваем сессию
            session_data["last_activity"] = now.isoformat()
            session_data["session_expires_at"] = (now + self.session_ttl).isoformat()
            
            self.redis.save_session(
                key=session_id,
                data=session_data,
                ttl=int(self.session_ttl.total_seconds())
            )
        
        return session_data

    def refresh_access_token_sync(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Синхронная версия обновления токена"""
        token_url = f"{self.bitrix_domain}/oauth/token/"
        
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token
        }
        
        try:
            response = requests.get(token_url, params=params)
            response.raise_for_status()
            tokens = response.json()
            
            tokens["access_token_expires_at"] = (
                datetime.now() + self.access_token_ttl
            ).isoformat()
            
            if "refresh_token" in tokens:
                tokens["refresh_token_expires_at"] = (
                    datetime.now() + self.refresh_token_ttl
                ).isoformat()
            
            return tokens
            
        except requests.RequestException as e:
            LogsMaker().error_message(f"Token refresh failed: {str(e)}")
            return None

    def delete_session(self, session_id: str) -> None:
        """Удаление сессии"""
        session_data = self.redis.get_session(session_id)
        
        if session_data and "user_id" in session_data:
            # Удаляем session_id из списка сессий пользователя
            user_sessions_key = f"user_sessions:{session_data['user_id']}"
            self.redis.remove_from_set(user_sessions_key, session_id)
        
        self.redis.delete_session(session_id)

    async def authenticate_user(self, code: str) -> Optional[Dict[str, Any]]:
        """Полная аутентификация пользователя через Bitrix24 OAuth"""
        # Получаем токены
        tokens = await self.exchange_code_for_tokens(code)
        
        if not tokens:
            return None
        
        # Получаем информацию о пользователе
        user_info = await self.get_user_info(tokens["access_token"])
        
        if not user_info:
            return None
        
        # Создаем сессию
        session = await self.create_session(tokens, user_info)
        return session
        
    #ROOT
    async def root_authenticate(self, username: str, password: str, sess) -> Optional[Dict[str, Any]]:
        b24_ans = try_b24(login=username, password=password)
        
        if b24_ans['status'] == 'success':
            user_id = b24_ans['data']['USER_ID']
            
            res = await User(id=user_id).search_by_id(session=sess)
        
            user_uuid = res["uuid"]

        else:
            return LogsMaker().error_message("Auth error! Invalid login or password!")
        
        session_id = str(uuid.uuid4())

        # Получаем дополнительные данные пользователя (замените на ваш метод)
        user_data = await User(uuid=user_uuid).user_inf_by_uuid(sess)
        # user_data_string = json.dump(user_data)
        # print(user_data_string)


        session_expires_at = datetime.now() + self.session_ttl
       
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "access_token_expires_at": session_expires_at.isoformat(),
            "refresh_token_expires_at": None,
            "session_expires_at": session_expires_at.isoformat(),
            "user_info": user_data,
            "last_activity": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "member_id": None
        }
        print(session_data)

        # если пользователь валидный проверяем, нет ли его сессии в Rdis
        ses_find = self.redis.get_session(session_id)
        if ses_find is None:
            self.redis.save_session(key=session_id, data=session_data, ttl=int(self.session_ttl.total_seconds()))
        
        else:
            session_id = ses_find[8:]
        return {
            "session_id": session_id,
            "user_id" : user_id,
            "user": session_data
        }

#ROOT
def extract_auth_data(html_content):
    """
    Извлекает USER_ID и bitrix_sessid из HTML
    """
    # Ищем USER_ID
    user_id_match = re.search(r'"USER_ID":"(\d+)"', html_content)
    # Ищем bitrix_sessid
    sessid_match = re.search(r'"bitrix_sessid":"([a-f0-9]+)"', html_content)

    user_id = user_id_match.group(1) if user_id_match else None
    bitrix_sessid = sessid_match.group(1) if sessid_match else None

    return {
        "USER_ID": user_id,
        "bitrix_sessid": bitrix_sessid
    }

#ROOT
def try_b24(login, password):
    # URL для авторизации
    auth_url = "https://portal.emk.ru/?login=yes"

    # Данные формы
    form_data = {
        "AUTH_FORM": "Y",
        "TYPE": "AUTH",
        "backurl": "/",
        "Login": "Войти",
        "USER_LOGIN": login,
        "USER_PASSWORD": password
    }

    # Заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        # Отправляем POST запрос
        response = requests.post(auth_url, data=form_data, headers=headers)
        response.raise_for_status()

        # Проверяем заголовок страницы с помощью регулярного выражения
        title_match = re.search(r'<title>\s*(.*?)\s*</title>', response.text, re.IGNORECASE)
        title_text = title_match.group(1) if title_match else ""

        # Если в title есть "Авторизация" - неудачная авторизация
        if "Авторизация" in title_text:
            return {
                "status": "failed",
                "message": "Неверный логин или пароль"
            }

        # Если авторизация успешна - извлекаем данные
        auth_data = extract_auth_data(response.text)

        if auth_data["USER_ID"] and auth_data["bitrix_sessid"]:
            return {
                "status": "success",
                "data": auth_data
            }
        else:
            return {
                "status": "failed",
                "message": "Авторизация прошла, но не удалось извлечь данные пользователя"
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "message": f"Ошибка сети: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка: {str(e)}"
        }


# Dependency для получения текущей сессии
async def get_current_session(request: Request, auth_service: AuthService = Depends(lambda: AuthService())) -> Dict[str, Any]:
    """Получение текущей сессии пользователя"""
    # Ищем session_id в куках или заголовках
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("session_id")
        if auth_header:# and auth_header.startswith("Bearer "):
            session_id = auth_header#[7:]
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Проверяем и обновляем сессию
    session_data = auth_service.validate_and_refresh_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return session_data



@auth_router.get("/login", tags=["Авторизация"])
async def login_to_bitrix24():
    """Перенаправление на страницу авторизации Bitrix24"""
    auth_service = AuthService()
    auth_url = await auth_service.get_auth_url()
    return RedirectResponse(url=auth_url)

#ROOT
@auth_router.post("/root_auth", tags=["Авторизация"])
async def root_auth(response: Response, data=Body(), sess: AsyncSession = Depends(get_async_db)):
    if "login" in data and "password" in data:  # login : str, password : str,
        login = data["login"]
        password = data["password"]
    else:
        # return await LogsMaker().warning_message(message="Login or Password has missing")
        return LogsMaker().warning_message(message="Login or Password has missing")

    session = await AuthService().root_authenticate(login, password, sess)
    
    if not session:
        # return await LogsMaker().warning_message(message="Invalid credentials")
        return LogsMaker().warning_message(message="Invalid credentials")
    elif "err" in session.keys() or "error" in session.keys():
        # return await LogsMaker().warning_message(message=session["err"])

        return LogsMaker().warning_message(message=session)

    if "session_id" in session:

        session_id = session["session_id"]
        user_id = session["user_id"]
        
        # Устанавливаем session_id в куки
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=int(AuthService().session_ttl.total_seconds())
        )

        # Устанавливаем session_id в куки
        response.set_cookie(
            key="user_id",
            value=user_id,
            max_age=int(AuthService().session_ttl.total_seconds())
        )

        # return JSONResponse(content=session, headers=response.headers)
        return session
    else:

        return session


@auth_router.get("/auth", tags=["Авторизация", "Битрикс24"], description = """
## OAuth 2.0 Аутентификация через Битрикс24

Система аутентификации пользователей через OAuth 2.0 протокол Битрикс24. Обеспечивает безопасный вход и управление сессиями.

---

## Методы
    - /oauth/authorize/ - для авторизации через Битрикс24 по логину и паролю, 
    - oauth.bitrix24.tech - для обмена кода авторизации на токены,
    - user.current.json - для полученя данных авторизованного в Битрикс24 пользователя

Выполняет обмен кода авторизации на access и refresh токены через OAuth 2.0 endpoint Битрикс24.

### Входные параметры
| Параметр | Тип | Описание | Обязательный |
|----------|-----|----------|--------------|
| `code` | string | Временный код авторизации, полученный от Битрикс24 после редиректа | Да |

### Возвращаемые данные
При успехе возвращает словарь с токенами и метаданными:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ...",
    "refresh_token": "def50200f3a8d7b7e8f9a6c5d4e3f2a1b0c9d8e7f...",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": "user,bizproc,calendar",
    "user_id": "123",
    "member_id": "portal.emk.ru",
    "domain": "portal.emk.ru",
    "access_token_expires_at": "2024-01-15T11:30:00+03:00",
    "refresh_token_expires_at": "2024-02-14T10:30:00+03:00"
}
""")
async def bitrix24_callback(code: str, state: Optional[str] = None, response: Response = None):
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code is missing"
        )
    
    auth_service = AuthService()
    session = await auth_service.authenticate_user(code)
    
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with Bitrix24"
        )
    
    redirect_url = f"https://intranet.emk.ru/" # auth/{code}/{session['member_id']}
    
    # Создаем RedirectResponse
    response = RedirectResponse(url=redirect_url, status_code=302)

    # Для API возвращаем JSON, для веб-приложения можно сделать редирект
    # response = JSONResponse(content={
    #     "status": "success",
    #     "session_id": session["session_id"],
    #     "user": session["user"],
    #     "expires_at": session["session_expires_at"]
    # })

    # Устанавливаем session_id в куки
    response.set_cookie(
        key="session_id",
        value=session["session_id"],
        max_age=int(AuthService().session_ttl.total_seconds())
    )
    # Устанавливаем session_id в куки
    response.set_cookie(
        key="user_id",
        value=session["user"]['ID'],
        max_age=int(AuthService().session_ttl.total_seconds())
    )

    return response


@auth_router.get("/check", tags=["Авторизация"])
async def check_session(session_data: Dict[str, Any] = Depends(get_current_session)):
    """Проверка валидности сессии"""
    return {
        "authenticated": True,
        "user": session_data.get("user_info"),
        "session_expires_at": session_data.get("session_expires_at")
    }


@auth_router.post("/refresh", tags=["Авторизация"])
async def refresh_session(request: Request, auth_service: AuthService = Depends(lambda: AuthService())):
    """Принудительное обновление сессии"""
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("session_id")
        if auth_header:# and auth_header.startswith("Bearer "):
            session_id = auth_header#[7:]
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_data = auth_service.validate_and_refresh_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return {
        "status": "success",
        "session_id": session_id,
        "session_expires_at": session_data.get("session_expires_at")
    }


@auth_router.post("/logout", tags=["Авторизация"])
async def logout(request: Request, response: Response, auth_service: AuthService = Depends(lambda: AuthService())):
    """Выход из системы"""
    session_id = request.cookies.get("session_id")
    
    if session_id:
        auth_service.delete_session(session_id)
    
    # Удаляем куку
    response.delete_cookie("session_id")
    
    return {"status": "success", "message": "Logged out successfully"}


@auth_router.get("/regconf", tags=["Авторизация"])
async def regconf(request: Request, session_data: Dict[str, Any] = Depends(get_current_session), response: Response = None):
    #проверка на авторизацию
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with Bitrix24"
        )
    # получаю данные пользователя
    user_info = {
        'uuid': session_data['user_info']['XML_ID'][3:],
        'fio': [session_data['user_info']['LAST_NAME'], session_data['user_info']['NAME'], session_data['user_info']['SECOND_NAME']],
        'department': session_data['user_info']['UF_USR_1696592324977']
    }
    
    res = requests.post(url='https://regconf.emk.ru/api/auth', json=user_info)
    token = res.json()

    redirect_url = f"https://regconf.emk.ru/"
     # Создаем RedirectResponse
    response = RedirectResponse(url=redirect_url, status_code=302)

    # Устанавливаем session_id в куки
    response.set_cookie(
        key="session_id",
        value=token["token"],
        max_age=int(AuthService().session_ttl.total_seconds())
    )

    return response
    
@auth_router.get("/tepconf", tags=["Авторизация"])
async def regconf(request: Request, session_data: Dict[str, Any] = Depends(get_current_session), response: Response = None):
    #проверка на авторизацию
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with Bitrix24"
        )
    # получаю данные пользователя
    user_info = {
        'uuid': session_data['user_info']['XML_ID'][3:],
        'fio': [session_data['user_info']['LAST_NAME'], session_data['user_info']['NAME'], session_data['user_info']['SECOND_NAME']],
        'department': session_data['user_info']['UF_USR_1696592324977']
    }
    
    res = requests.post(url='https://tepconf.emk.ru/login', json=user_info)
    token = res.json()

    redirect_url = f"https://tepconf.emk.ru/{token}"
     # Создаем RedirectResponse
    response = RedirectResponse(url=redirect_url, status_code=302)

    # Устанавливаем session_id в куки
    response.set_cookie(
        key="session_id",
        value=token["token"],
        max_age=int(AuthService().session_ttl.total_seconds())
    )

    return response

@auth_router.get("/gpt", tags=["Авторизация"])
async def regconf(request: Request, session_data: Dict[str, Any] = Depends(get_current_session), response: Response = None):
    #проверка на авторизацию
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with Bitrix24"
        )
    # получаю данные пользователя
    print(session_data['user_info'])
    if 'XML_ID' in session_data['user_info']:
        user_info = {
            'uuid': session_data['user_info']['XML_ID'][3:],
            'fio': [session_data['user_info']['LAST_NAME'], session_data['user_info']['NAME'], session_data['user_info']['SECOND_NAME']],
            'department': session_data['user_info']['UF_USR_1696592324977']
        }
    else:
        user_info = session_data['user_info']
    
    
    cookies = { 'session_id': session_data["session_id"]}
    res = requests.post(url='https://gpt.emk.ru/login', json=user_info, cookies=cookies)

    # redirect_url = f"https://gpt.emk.ru/{token}"
    #  # Создаем RedirectResponse
    # response = RedirectResponse(url=redirect_url, status_code=302)

    # Устанавливаем session_id в куки
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=int(AuthService().session_ttl.total_seconds())
    )

    return response
