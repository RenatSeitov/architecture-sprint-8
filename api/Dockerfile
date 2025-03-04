# Используем официальный образ Python в качестве родительского
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем пакеты, указанные в requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт 8000 для доступа извне контейнера
EXPOSE 8000

# Запускаем приложение при запуске контейнера
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
