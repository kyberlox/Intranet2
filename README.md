# Intranet2.0

## Процесс установки и запуска проекта на сервере
Для начала нужно убедиться в актуальности содержимого файлов конфигурации
```
/nginx/default.conf
nano .env
```
После чего переходим непосредственно к запуску:
```
git pull

docker-compose up -d --build
chmod -R 777 ./
docker-compose restart elasticsearch
docker-compose logs -f elasticsearch
bash reset.sh
```