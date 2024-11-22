FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /api/

COPY ./api/ /api/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]