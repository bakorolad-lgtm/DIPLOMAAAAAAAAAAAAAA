# ---- Базовый образ ----
FROM python:3.12-slim AS base

# Установка системных зависимостей
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Установка uv (быстрый менеджер пакетов)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавляем uv в PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# ---- Копируем зависимости ----
COPY pyproject.toml ./

RUN uv sync

# ---- Копируем исходники ----
COPY . .

# ---- Запуск приложения ----
EXPOSE 8005
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]
