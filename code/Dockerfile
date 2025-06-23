FROM python:3.13-alpine3.22

WORKDIR /data/app
COPY ./requirements.txt /data/app/requirements.txt

# Устанавливаем зависимости для pyvips
RUN apk add --no-cache \
    vips-dev \
    vips \
    vips-cpp \
    vips-tools \
    vips-libs \
    build-base \
    && pip install --no-cache-dir pyvips

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#COPY ./ /data/app

CMD ["fastapi", "run", "main.py", "--port", "8000"]