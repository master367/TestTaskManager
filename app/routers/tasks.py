from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Task, TaskStatus, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, PaginatedTaskResponse
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        user_id=current_user.id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/", response_model=PaginatedTaskResponse)
async def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    order_by: Literal["asc", "desc"] = Query(default="desc", alias="sort"),
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be between 1 and 100")
    if offset < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset must be 0 or greater")

    base_query = select(Task).where(Task.user_id == current_user.id)

    if status_filter is not None:
        base_query = base_query.where(Task.status == status_filter)

    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = base_query

    if order_by == "asc":
        query = query.order_by(asc(Task.created_at))
    else:
        query = query.order_by(desc(Task.created_at))

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await db.delete(task)
    await db.commit()
