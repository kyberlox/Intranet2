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

# Загрузка переменных окружения
load_dotenv()

auth_router = APIRouter(prefix="/auth_router", tags=["Авторизация"])

 
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
        self.client_id = os.getenv("BITRIX_CLIENT_ID", "local.6936c2c4e28141.22464163")
        self.client_secret = os.getenv("BITRIX_CLIENT_SECRET", "jgXugnqtLI0IZf1iJvvAIi2aWi183EM2nBEr3SGHIZRa0f6Pg9")
        self.redirect_uri = os.getenv("BITRIX_REDIRECT_URI", "https://intranet.emk.ru/api/auth_router/auth")
        self.bitrix_domain = os.getenv("BITRIX_DOMAIN", "https://test-portal.emk.ru")
        
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
            "created_at": datetime.now().isoformat()
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
            "user": user_info
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


# Dependency для получения текущей сессии
async def get_current_session(
    request: Request,
    auth_service: AuthService = Depends(lambda: AuthService())
) -> Dict[str, Any]:
    """Получение текущей сессии пользователя"""
    # Ищем session_id в куках или заголовках
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_id = auth_header[7:]
    
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


@auth_router.get("/login")
async def login_to_bitrix24():
    """Перенаправление на страницу авторизации Bitrix24"""
    auth_service = AuthService()
    auth_url = await auth_service.get_auth_url()
    return RedirectResponse(url=auth_url)


@auth_router.get("/auth")
async def bitrix24_callback(
    code: str,
    state: Optional[str] = None,
    error: Optional[str] = None,
    response: Response = None
):
    
    """Callback endpoint для Bitrix24 OAuth"""
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authorization failed: {error}"
        )
    
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
    
    # Устанавливаем session_id в куки
    if response:
        response.set_cookie(
            key="session_id",
            value=session["session_id"],
            max_age=int(AuthService().session_ttl.total_seconds())
        )
        print("записываю куки", session["session_id"])
        response.set_cookie(key="Authorization", value=session["session_id"])
    
    # Для API возвращаем JSON, для веб-приложения можно сделать редирект
    return JSONResponse(content={
        "status": "success",
        "session_id": session["session_id"],
        "user": session["user"],
        "expires_at": session["session_expires_at"]
    })


@auth_router.get("/check")
async def check_session(
    session_data: Dict[str, Any] = Depends(get_current_session)
):
    """Проверка валидности сессии"""
    return {
        "authenticated": True,
        "user": session_data.get("user_info"),
        "session_expires_at": session_data.get("session_expires_at")
    }


@auth_router.post("/refresh")
async def refresh_session(
    request: Request,
    auth_service: AuthService = Depends(lambda: AuthService())
):
    """Принудительное обновление сессии"""
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_id = auth_header[7:]
    
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


@auth_router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(lambda: AuthService())
):
    """Выход из системы"""
    session_id = request.cookies.get("session_id")
    
    if session_id:
        auth_service.delete_session(session_id)
    
    # Удаляем куку
    response.delete_cookie("session_id")
    
    return {"status": "success", "message": "Logged out successfully"}


# # Middleware для автоматического обновления сессии
# @app.middleware("http")
# async def session_middleware(request: Request, call_next):
#     """Middleware для обработки сессий"""
#     auth_service = AuthService()
#     session_id = request.cookies.get("session_id")
    
#     if session_id:
#         # Проверяем и обновляем сессию
#         session_data = auth_service.validate_and_refresh_session(session_id)
        
#         if session_data:
#             # Если сессия была обновлена, устанавливаем новые куки
#             response = await call_next(request)
            
#             # Проверяем, не нужно ли обновить куки (скользящее окно)
#             last_activity = datetime.fromisoformat(session_data["last_activity"])
#             if datetime.now() > last_activity + auth_service.session_sliding_window:
#                 response.set_cookie(
#                     key="session_id",
#                     value=session_id,
#                     httponly=True,
#                     secure=True,
#                     samesite="lax",
#                     max_age=int(auth_service.session_ttl.total_seconds())
#                 )
            
#             return response
    
#     return await call_next(request)