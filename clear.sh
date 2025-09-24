#!/bin/sh

#чистим docker
docker-compose down
docker system prune -a

#чистим файлы и базы данных
rm -rf ./code/files_db/
mkdir ./code/files_db
mkdir ./code/files_db/user_photo

rm -rf ./mongodb/data/*

rm -rf ./pSQL/data/*

rm -rf ./elasticsearch/data*

docker-compose up -d

chmod -R 777 ./