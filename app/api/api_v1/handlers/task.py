from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from beanie.operators import RegEx 
from uuid import UUID
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskOut, TaskUpdate
from app.api.api_v1.dependencies.user_deps import get_current_user

task_router = APIRouter()

# 1. LISTAR 
@task_router.get("/", response_model=List[TaskOut])
async def list_tasks(
    status: Optional[bool] = None,
    title: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    current_user: User = Depends(get_current_user)
):
    """
    Lista tarefas com filtros opcionais de status e título.
    """
    # Iniciamos a query básica: apenas tarefas do dono
    query = Task.find(Task.owner == current_user.id)
    
    # Se o usuário enviou um status (True/False), adicionamos o filtro
    if status is not None:
        query = query.find(Task.status == status)
        
    # Se o usuário enviou um título, fazemos uma busca "case-insensitive"
    if title:
        query = query.find(RegEx(Task.title, title, options="i"))
        
    return await query.limit(limit).skip(skip).to_list()

# 2. CRIAR
@task_router.post(
    "/create", 
    response_model=TaskOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The task was successfully created in the database."
)
async def create_task(data: TaskCreate, current_user: User = Depends(get_current_user)):
    """
    Cria uma tarefa vinculada ao usuário logado.
    
    - **title**: Nome da tarefa (mínimo 3 caracteres)
    - **description**: Detalhes do que fazer
    - **status**: Por padrão, toda tarefa nasce como 'false' (pendente)
    """
    new_task = Task(title=data.title, description=data.description, owner=current_user.id)
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