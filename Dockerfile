FROM python:3.11
LABEL authors="masha"

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","run.py"]
