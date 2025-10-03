#!/bin/sh

git pull origin main
docker-compose down fastapi
docker-compose up -d fastapi
#docker-compose restart fastapi
docker-compose logs -f fastapi