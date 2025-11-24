#!/bin/sh

#чистим docker
docker-compose down
docker system prune -a

#чистим файлы и базы данных
rm -rf ./code/files_db/
mkdir ./code/files_db
mkdir ./code/files_db/user_photo

rm -rf ./code/vcard_db/
mkdir ./code/vcard_db



sudo rm -rf ./mongodb/data/*

sudo rm -rf ./pSQL/data/*

sudo rm -rf ./elasticsearch/data*


#качаем с гита и запускаемся
git pull origin main

docker-compose up -d --build

chmod -R 777 ./

docker-compose restart elasticsearch

docker-compose restart fastapi

docker-compose logs -f fastapi