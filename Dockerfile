FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /app/