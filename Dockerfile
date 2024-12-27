FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для логов
RUN mkdir -p /app/logs

COPY src/ .

CMD ["python", "main.py"] 