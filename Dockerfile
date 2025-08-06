# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        gcc \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем pipenv
RUN pip install --upgrade pip && pip install pipenv

# Копируем только pipenv-файлы для установки зависимостей
COPY Pipfile Pipfile.lock ./

# Устанавливаем зависимости в системную среду (не создавая venv)
ENV PIPENV_VENV_IN_PROJECT=0
RUN pipenv install --deploy --system

# Копируем всё остальное
COPY . .

# Указываем команду запуска
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
