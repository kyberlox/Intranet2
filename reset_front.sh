#!/bin/sh


git pull origin main


docker-compose stop frontend
docker-compose rm frontend
docker-compose up -d --build frontend # если требуется установка библиотек


# git pull origin main
# docker-compose stop frontend
# docker rmi intranet_frontend
# docker-compose up -d frontend