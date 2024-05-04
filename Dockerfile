FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["sh", "-c", "alembic upgrade head && python main.py"]
