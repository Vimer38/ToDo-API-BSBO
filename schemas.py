from pydantic import BaseModel, Field, computed_field
from typing import Optional
from datetime import datetime

from utils import calculate_days_left, is_urgent as check_urgent


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название задачи")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Описание задачи")
    is_important: bool = Field(
        ...,
        description="Важность задачи")
    deadline_at: datetime = Field(
        ...,
        description="Плановый срок выполнения (дедлайн)",
        examples=["2026-11-30T18:00:00Z"])


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Новое название задачи")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Новое описание")
    is_important: Optional[bool] = Field(
        None,
        description="Новая важность")
    deadline_at: Optional[datetime] = Field(
        None,
        description="Новый дедлайн")
    completed: Optional[bool] = Field(
        None,
        description="Статус выполнения")


class TaskResponse(TaskBase):
    id: int = Field(..., description="Уникальный идентификатор задачи", examples=[1])
    quadrant: str = Field(
        ...,
        description="Квадрант матрицы Эйзенхауэра (Q1, Q2, Q3, Q4)",
        examples=["Q1"])
    completed: bool = Field(default=False, description="Статус выполнения задачи")
    created_at: datetime = Field(..., description="Дата и время создания задачи")

    @computed_field(description="Дней от сегодняшней даты до дедлайна")
    @property
    def days_left(self) -> int:
        return calculate_days_left(self.deadline_at)

    @computed_field(description="Срочность (рассчитывается по дедлайну)")
    @property
    def is_urgent(self) -> bool:
        return check_urgent(self.deadline_at)

    class Config:
        from_attributes = True


class TaskDeadlineInfo(BaseModel):
    title: str
    description: Optional[str]
    created_at: datetime
    deadline_at: datetime
    days_left: int