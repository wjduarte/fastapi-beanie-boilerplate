from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from beanie.operators import RegEx 
from uuid import UUID
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskOut, TaskUpdate
from app.api.api_v1.dependencies.user_deps import get_current_user
from app.models.category_model import Category

task_router = APIRouter()

# 1. LISTAR 
@task_router.get("/", response_model=List[TaskOut])
async def list_tasks(
    task_status: Optional[bool] = None,
    title: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    current_user: User = Depends(get_current_user)
):
    """
    Lista tarefas com filtros opcionais de status e título.
    """
    # Consulta base: tarefas do usuário atual
    query = Task.find(Task.owner == current_user.id)
    
    # Se o usuário enviou um status, adicionamos o filtro
    if task_status is not None:
        query = query.find(Task.status == task_status)
        
    # Se o usuário enviou um título, adicionamos o filtro com RegEx para busca parcial
    if title:
        query = query.find(RegEx(Task.title, title, options="i"))
        
    return await query.limit(limit).skip(skip).to_list()

# 2. CRIAR
@task_router.post("/create", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, current_user: User = Depends(get_current_user)):
    
    # Validação de Segurança Comercial
    if data.category:
        category_exists = await Category.find_one(
            Category.id == data.category, 
            Category.owner == current_user.id
        )
        if not category_exists:
            raise HTTPException(
                status_code=404, 
                detail="A categoria informada não foi encontrada ou não pertence a você."
            )

    new_task = Task(
        title=data.title,
        description=data.description,
        owner=current_user.id,
        category=data.category # Salvamos o UUID da categoria na tarefa
    )
    await new_task.insert()
    return new_task

# 3. BUSCAR UMA TAREFA ESPECÍFICA
@task_router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: UUID, current_user: User = Depends(get_current_user)):
    task = await Task.find_one(Task.id == task_id, Task.owner == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 4. ATUALIZAR (PUT)
@task_router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: UUID, data: TaskUpdate, current_user: User = Depends(get_current_user)):
    task = await Task.find_one(Task.id == task_id, Task.owner == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Atualiza apenas os campos enviados no JSON
    await task.update({"$set": data.model_dump(exclude_unset=True)})
    return task

# 5. DELETAR
@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, current_user: User = Depends(get_current_user)):
    task = await Task.find_one(Task.id == task_id, Task.owner == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await task.delete()
    return None