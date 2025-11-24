# Intranet2.0

## Процесс установки и запуска проекта на сервере

Для начала нужно убедиться в актуальности содержимого файлов конфигурации:
```
/nginx/default.conf
nano .env
```
Создайте необходимые директории:
```
cd code
mkdir vcard_db
cd files_db
mkdir tours
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
