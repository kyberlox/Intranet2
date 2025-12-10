import redis
from datetime import timedelta
from typing import Optional, Dict, Any
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class RedisStorage:
    def __init__(self):
        redis_host = "redis"
        redis_port = 6379
        redis_db = 0
        redis_password = os.getenv("pswd")

        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )
        self.check_connection()

    def check_connection(self):
        try:
            return self.client.ping()
        except redis.RedisError as e:
            logging.error(f"Redis connection error: {e}")
            raise

    def save_session(self, key: str, data: Dict[str, Any], ttl: int = None) -> bool:
        """
        Сохранение данных в Redis
        
        :param key: Ключ для сохранения
        :param data: Данные для сохранения
        :param ttl: Время жизни в секундах
        :return: True если успешно
        """
        try:
            if ttl:
                self.client.setex(key, ttl, json.dumps(data))
            else:
                self.client.set(key, json.dumps(data))
            return True
        except redis.RedisError as e:
            logging.error(f"Error saving to Redis: {e}")
            return False

    def get_session(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Получение данных из Redis
        
        :param key: Ключ
        :return: Данные или None
        """
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except (redis.RedisError, json.JSONDecodeError) as e:
            logging.error(f"Error getting from Redis: {e}")
            return None

    def delete_session(self, key: str) -> bool:
        """
        Удаление данных из Redis
        
        :param key: Ключ
        :return: True если успешно
        """
        try:
            return bool(self.client.delete(key))
        except redis.RedisError as e:
            logging.error(f"Error deleting from Redis: {e}")
            return False

    def update_session_ttl(self, key: str, ttl: int) -> bool:
        """
        Обновление времени жизни ключа
        
        :param key: Ключ
        :param ttl: Время жизни в секундах
        :return: True если успешно
        """
        try:
            return bool(self.client.expire(key, ttl))
        except redis.RedisError as e:
            logging.error(f"Error updating TTL: {e}")
            return False

    def add_to_set(self, key: str, value: str) -> bool:
        """
        Добавление значения в множество
        
        :param key: Ключ множества
        :param value: Значение
        :return: True если успешно
        """
        try:
            return bool(self.client.sadd(key, value))
        except redis.RedisError as e:
            logging.error(f"Error adding to set: {e}")
            return False

    def remove_from_set(self, key: str, value: str) -> bool:
        """
        Удаление значения из множества
        
        :param key: Ключ множества
        :param value: Значение
        :return: True если успешно
        """
        try:
            return bool(self.client.srem(key, value))
        except redis.RedisError as e:
            logging.error(f"Error removing from set: {e}")
            return False

    def close(self):
        """Закрытие соединения"""
        if hasattr(self, 'client'):
            self.client.close()