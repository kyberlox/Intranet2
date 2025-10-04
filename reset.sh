#!/bin/sh

git pull origin dev
docker-compose down fastapi
docker-compose up -d fastapi
docker-compose logs fastapi -f