#!/bin/sh

git pull origin dev
#docker-compose down fastapi
#docker-compose up -d fastapi

#docker-compose restart fastapi

docker-compose stop fastapi
docker-compose rm fastapi
docker-compose up -d fastapi
#docker-compose up -d --build fastapi # если требуется установка библиотек

docker-compose logs -f fastapi