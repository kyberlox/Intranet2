#!/bin/sh

git stash
git pull origin main
docker-compose down fastapi
docker-compose up -d fastapi
docker-compose logs fastapi -f