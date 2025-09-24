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



docker-compose up -d

sudo chmod -R 777 ./