FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]