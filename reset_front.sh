#!/bin/sh

# docker-compose down
# git pull origin main
# docker images
# docker rmi intranet_frontend
# docker-compose up --build -d



git pull origin main
docker-compose stop vue_async
docker rmi intranet_frontend
docker-compose up -d --build vue_async



# docker-compose rm fastapi
# docker-compose up -d fastapi

# docker-compose logs -f fastapi