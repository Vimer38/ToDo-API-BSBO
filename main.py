# Главный файл приложения
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from routers import tasks



app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact = {
        "name": "Андрианов Кирилл Алексеевич"
    }
)

app.include_router(tasks.router)

@app.get("/")
async def welcome() -> dict:
    return {"message": "Привет, студент!",
            "api_title": app.title,
            "api_desription": app.description,
            "api_version": app.version,
            "api_author": app.contact["name"]
            }



