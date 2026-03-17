# Пет-проект

Демонстрационный проект с использованием FastAPI, LangGraph, PostgreSQL, Kafka, Docker и Kubernetes.

## Технический стек
- Python
- FastAPI
- LangGraph
- Uvicorn
- Docker
- Kubernetes
- PostgreSQL
- Kafka
- UV (менеджер пакетов)
- GitLab CI

## Возможности
- REST API с FastAPI для обработки текста
- Рабочий процесс LangGraph для преобразования текста
- Интеграция с PostgreSQL для сохранения данных
- Мессенджинг Kafka для публикации событий
- Комплексное логирование в приложении
- Юнит и интеграционные тесты с pytest
- Контейнеризация Docker
- Манифесты развертывания Kubernetes
- Пайплайн GitLab CI/CD

## Установка

1. Установите UV: `pip install uv`
2. Установите зависимости: `uv pip install -r pyproject.toml`
3. Запустите с Docker Compose: `docker-compose up --build`

## API

- POST /process: Обработать текст с LangGraph, сохранить в БД, отправить в Kafka
- GET /: Проверка работоспособности API

## Тестирование

Запустите юнит и интеграционные тесты:
```
pytest
```

## Логирование

Приложение использует модуль логирования Python с уровнем INFO. Логи выводятся в консоль.

## Kubernetes

Примените манифесты: `kubectl apply -f k8s/`