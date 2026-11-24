from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models import Task
from routers.tasks import router
from schemas import TaskDeadlineInfo
from utils import calculate_days_left


@router.get("/deadlines", response_model=List[TaskDeadlineInfo])
async def get_pending_deadlines(
        db: AsyncSession = Depends(get_async_session)
) -> List[TaskDeadlineInfo]:
    """Статистика по срокам невыполненных (pending) задач."""
    result = await db.execute(
        select(Task).where(Task.completed == False)  # noqa: E712
    )
    tasks = result.scalars().all()

    items = [
        TaskDeadlineInfo(
            title=t.title,
            description=t.description,
            created_at=t.created_at,
            deadline_at=t.deadline_at,
            days_left=calculate_days_left(t.deadline_at)
        )
        for t in tasks
    ]
    # Самые горящие задачи сверху
    return sorted(items, key=lambda x: x.days_left)