import redis
from datetime import timedelta
from typing import Optional, Dict, Any
import json
import logging

import os
from dotenv import load_dotenv


# Загрузка переменных окружения
load_dotenv()

class RedisStorage:
    def __init__(self):
        """
        Инициализация подключения к Redis

        :param host: Хост Redis
        :param port: Порт Redis
        :param db: Номер базы данных
        :param username: Имя пользователя Redis (опционально)
        :param password: Пароль Redis (опционально)
        """
        # Настройки Redis из .env
        redis_host = "redis"
        redis_port = 6379
        redis_db = 0
        #redis_username = os.getenv("user")
        redis_password = os.getenv("pswd")

        # Инициализация Redis с аутентификацией
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            #username=redis_username,
            password=redis_password,
            decode_responses=True
        )
        self.check_connection()

    def check_connection(self):
        """Проверка подключения к Redis"""
        try:
            if not self.client.ping():
                raise ConnectionError("Redis connection failed")
        except redis.AuthenticationError as e:
            logging.error(f"Redis authentication error: {e}")
            raise
        except redis.ConnectionError as e:
            logging.error(f"Redis connection error: {e}")
            raise
        return True

    def save_session(self, session_id: str, data: Dict[str, Any], ttl: Optional[timedelta] = None) -> bool:
        """
        Сохранение сессии в Redis

        :param session_id: Идентификатор сессии
        :param data: Данные для сохранения
        :param ttl: Время жизни сессии
        :return: True если успешно сохранено
        """
        try:
            key = f"session:{session_id}"
            self.client.hset(key, mapping=data)
            if ttl:
                self.client.expire(key, int(ttl.total_seconds()))
            return True
        except redis.RedisError as e:
            logging.error(f"Error saving session to Redis: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Получение данных сессии

        :param session_id: Идентификатор сессии
        :return: Словарь с данными сессии или None
        """
        try:
            key = f"session:{session_id}"
            data = self.client.hgetall(key)
            return data if data else None
        except redis.RedisError as e:
            logging.error(f"Error getting session from Redis: {e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """
        Удаление сессии

        :param session_id: Идентификатор сессии
        :return: True если успешно удалено
        """
        try:
            key = f"session:{session_id}"
            return bool(self.client.delete(key))
        except redis.RedisError as e:
            logging.error(f"Error deleting session from Redis: {e}")
            return False

    def update_session_ttl(self, session_id: str, ttl: timedelta) -> bool:
        """
        Обновление времени жизни сессии

        :param session_id: Идентификатор сессии
        :param ttl: Новое время жизни
        :return: True если успешно обновлено
        """
        try:
            key = f"session:{session_id}"
            return bool(self.client.expire(key, int(ttl.total_seconds())))
        except redis.RedisError as e:
            logging.error(f"Error updating session TTL: {e}")
            return False

    def close(self):
        """Закрытие соединения с Redis"""
        if hasattr(self, 'client'):
            self.client.close()