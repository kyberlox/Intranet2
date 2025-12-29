from fastapi import APIRouter

from fastapi import FastAPI, Request, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
from typing import Optional
import json

from pydantic import BaseModel

from ..model.User import User

import requests

import httpx

app = FastAPI()
ai_router = APIRouter(prefix="/ai", tags=["GPT"])

# Базовый URL целевого сервера
TARGET_BASE_URL = "https://gpt.emk.ru"

class Dialog(BaseModel):
    ID : str
    name: str
    user_uuid: str
    messages: dict

class History:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dialog = Dialog()
    
    #получить диалоги по uuid

    #получить диалог

    #переименовать диалог

    #создать диалог

    #изменить диалог (добавить сообщение)

    #удалить диалог

class GPT:
    def __init__(self ):
        #self.token = "0WnS5hZAYRDpVP7NMTl^n8@XRxYEO4lR"
        self.domain = "gpt.emk.ru"
    
    async def send_to_gpt(self, messages):
        #проверить доступ
        #проксировать запросы
        #вернуть ответ
        #сохранить в историю
        pass

async def get_current_user(request: Request):
    """
    Здесь реализуйте вашу логику аутентификации
    """
    # Пример: получаем токен из заголовка
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # В реальном приложении здесь будет проверка токена
    # и получение данных пользователя
    return {"id": user_id, "session_id": session_id}


@app.api_route("/proxy/{path:path}", methods=["POST", "GET", "PATCH"])
async def proxy_request(
    path: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Универсальный прокси для всех POST/GET/PATCH запросов
    """
    # Формируем целевой URL
    target_url = f"{TARGET_BASE_URL}/{path}"
    
    try:
        # Получаем тело запроса
        body = await request.body()
        
        # Получаем заголовки
        headers = dict(request.headers)
        
        # Удаляем/заменяем ненужные заголовки
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # Добавляем заголовки авторизации для целевого сервера
        # Здесь можно добавить токен или другую авторизацию
        response.set_cookie(
            key="session_id",
            value=current_user["session_id"],
            max_age=int(AuthService().session_ttl.total_seconds())
        )

        # Устанавливаем session_id в куки
        response.set_cookie(
            key="user_id",
            value=current_user["user_id"],
            max_age=int(AuthService().session_ttl.total_seconds())
        )
        
        # Определяем Content-Type
        content_type = request.headers.get("content-type", "")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Отправляем запрос на целевой сервер
            if "multipart/form-data" in content_type:
                # Для multipart/form-data с файлами
                form_data = await request.form()
                
                # Преобразуем FormData в формат для httpx
                files = {}
                data = {}
                
                for key, value in form_data.items():
                    if isinstance(value, UploadFile):
                        files[key] = (value.filename, await value.read(), value.content_type)
                    else:
                        data[key] = value
                
                if files:
                    response = await client.request(
                        method=request.method,
                        url=target_url,
                        files=files,
                        data=data,
                        headers=headers
                    )
                else:
                    response = await client.request(
                        method=request.method,
                        url=target_url,
                        data=data,
                        headers=headers
                    )
            else:
                # Для JSON или других типов контента
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    content=body,
                    headers=headers
                )
            
            # Возвращаем ответ как есть
            return StreamingResponse(
                content=response.aiter_bytes(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Target server timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Target server error: {str(e)}")