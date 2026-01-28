FROM python:3.13

WORKDIR /data/app
RUN mkdir files_db vcard_db
RUN mkdir /data/app/files_db/tours
RUN mkdir /data/app/files_db/user_photo

COPY ./requirements.txt /data/app/requirements.txt

# Устанавливаем системные зависимости
# RUN apk update && apk add --no-cache \
#     vips-dev \
#     vips \
#     vips-cpp \
#     glib-dev \
#     expat-dev \
#     tiff-dev \
#     jpeg-dev \
#     libpng-dev \
#     libwebp-dev \
#     gcc \
#     g++ \
#     make \
#     && pip install --no-cache-dir pyvips

RUN pip install --upgrade pip

RUN apt-get install libreoffice

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#COPY ./ /data/app

#CMD ["fastapi", "run", "main.py", "--port", "8000"]
CMD ["python3", "run.py"]