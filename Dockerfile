FROM python:alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /bot

# Копируем файлы проекта в контейнер
COPY . /bot

# Устанавливаем зависимости
RUN pip install -r requirements.txt

CMD ["python3", "./main.py"]