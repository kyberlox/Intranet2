# Intranet2.0

## Процесс установки и запуска проекта на сервере
```
git pull
nano .env
docker-compose up -d --build
chmod -R 777 ./
docker-compose restart elasticsearch
docker-compose logs -f elasticsearch
bash reset.sh
```