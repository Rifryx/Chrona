# Используем официальный легковесный образ Python
FROM python:3.13-slim

# Устанавливаем uv внутрь контейнера
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости проекта (пропуская создание виртуального окружения для контейнера)
RUN uv sync --frozen --no-cache

# Копируем оставшийся код проекта
COPY . .

# Команда для запуска приложения (замените main:app на ваш путь к FastAPI, если он отличается)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
