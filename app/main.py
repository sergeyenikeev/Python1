from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.langgraph_workflow import run_workflow
from app.database import save_to_db
from app.kafka_producer import send_to_kafka

app = FastAPI(title="Pet Project API", version="1.0.0")

class InputData(BaseModel):
    text: str

@app.post("/process")
async def process_text(data: InputData):
    try:
        # Run LangGraph workflow
        result = run_workflow(data.text)
        
        # Save to PostgreSQL
        save_to_db(data.text, result)
        
        # Send to Kafka
        send_to_kafka("processed_topic", {"input": data.text, "output": result})
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Pet Project API is running"}