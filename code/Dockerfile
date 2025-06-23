FROM python:3.13-alpine3.22

WORKDIR /data/app
COPY ./requirements.txt /data/app/requirements.txt

# Устанавливаем системные зависимости для pyvips
RUN apk update && apk add --no-cache \
    vips-dev \          # Основная библиотека VIPS
    vips \              # Runtime-зависимости
    vips-cpp \          # C++ поддержка
    glib-dev \          # Зависимость для GLib
    expat-dev \         # XML-парсинг
    build-base \        # Компиляторы (gcc, make)
    py3-pip \           # Pip для Alpine
    && pip install --no-cache-dir pyvips

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#COPY ./ /data/app

CMD ["fastapi", "run", "main.py", "--port", "8000"]