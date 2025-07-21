#!/bin/sh

#чистим docker
docker-compose down
docker system prune -a

#чистим файлы и базы данных
rm -r ./code/files_db/
mkdir ./code/files_db
mkdir ./code/files_db/user_photo

rm -r ./mongodb/data/*

rm -r ./pSQL/data/*