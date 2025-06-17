FROM python:3.13-alpine3.22

WORKDIR /data/app
COPY ./requirements.txt /data/app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#COPY ./ /data/app

CMD ["fastapi", "run", "main.py", "--port", "8000", "--timeout-keep-alive", "20"]