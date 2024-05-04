FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

RUN #alembic upgrade head

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["python", "main.py"]
