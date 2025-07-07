from locust import HttpUser, task, between
import random

# Пример данных для POST-запросов (подставьте свои)
SAMPLE_PAYLOADS = [
    {"login":"kyberlox","password":"#"},
    {"login":"","password":"#"},
    {"login":"kyberlox","password":""},
    {"login":"root","password":"root"},
]

FILES_PAYLOADS = [
    "user_files/IMG_2607.jpg.png",
    "compress_image/68550faa2d7b5901125e0cf5.png",
    "compress_image/68550fbd2d7b5901125e0d29.png",
    "compress_image/68550f982d7b5901125e0cb7.jpg",
    "compress_image/68550fb82d7b5901125e0d25.png",
    "compress_image/68550cc12d7b5901125e055d.png"
]

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)  # Пауза между запросами (1–3 сек)

    # Тестируем GET-эндпоинт
    @task(3)  # Частота вызова (3 к 1 относительно POST)
    def get_home(self):
        payload = random.choice(FILES_PAYLOADS)
        self.client.get("/api/{payload}")

    # Тестируем POST-эндпоинт с JSON
    @task
    def post_data(self):
        payload = random.choice(SAMPLE_PAYLOADS)
        self.client.post("/api/auth_router/auth", json=payload)