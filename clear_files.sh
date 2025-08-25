#!/bin/sh

#чистим docker
docker-compose down

#чистим файлы и базы данных
rm -r ./code/files_db/
mkdir ./code/files_db
mkdir ./code/files_db/user_photo

docker-compose up -d