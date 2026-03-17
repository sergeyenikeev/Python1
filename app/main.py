"""
Pet Project API - Демонстрация FastAPI с интеграцией LangGraph, PostgreSQL и Kafka.

Этот модуль содержит основное приложение FastAPI с endpoints для обработки текста
с использованием рабочих процессов LangGraph, сохранения результатов в PostgreSQL
и отправки сообщений в Kafka.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.langgraph_workflow import run_workflow
from app.database import save_to_db
from app.kafka_producer import send_to_kafka

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pet Project API",
    version="1.0.0",
    description="Пет-проект, демонстрирующий FastAPI, LangGraph, PostgreSQL и Kafka."
)

class InputData(BaseModel):
    """Модель входных данных для запросов обработки текста."""
    text: str

@app.post("/process")
async def process_text(data: InputData):
    """
    Обработать входной текст с использованием рабочего процесса LangGraph,
    сохранить в базу данных и отправить в Kafka.

    Args:
        data (InputData): Входные данные, содержащие текст для обработки.

    Returns:
        dict: Словарь с обработанным результатом.

    Raises:
        HTTPException: Если во время обработки возникает ошибка.
    """
logger.info(f"Получен запрос на обработку текста: {data.text[:50]}...")
    try:
        # Запустить рабочий процесс LangGraph
        logger.info("Запуск рабочего процесса LangGraph...")
        result = run_workflow(data.text)
        logger.info(f"Результат рабочего процесса: {result[:50]}...")

        # Сохранить в PostgreSQL
        logger.info("Сохранение в PostgreSQL...")
        save_to_db(data.text, result)
        
        # Отправить в Kafka
        logger.info("Отправка в Kafka...")
        send_to_kafka("processed_topic", {"input": data.text, "output": result})
        
        logger.info("Обработка завершена успешно.")
        return {"result": result}
    except Exception as e:
        logger.error(f"Ошибка во время обработки: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Корневой endpoint для проверки работы API.

    Returns:
        dict: Приветственное сообщение.
    """
    logger.info("Доступ к корневому endpoint.")
    return {"message": "Pet Project API работает"}