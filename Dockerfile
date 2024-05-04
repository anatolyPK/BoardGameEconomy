FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["sh", "-c", "python main.py && alembic upgrade head"]
