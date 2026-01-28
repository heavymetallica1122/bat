FROM python:3.12-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Копирование проекта
COPY . .

# Сбор статических файлов
RUN python manage.py collectstatic --noinput || true

# Порт
EXPOSE 8080

# Запуск через gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 battery_project.wsgi:application
