#!/bin/sh

git pull origin main
docker-compose restart fastapi
docker-compose logs fastapi -f