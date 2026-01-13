from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.category_model import Category
from app.models.user_model import User
from app.schemas.category_schema import CategoryCreate, CategoryOut
from app.api.api_v1.dependencies.user_deps import get_current_user

category_router = APIRouter()

@category_router.post("/create", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(data: CategoryCreate, current_user: User = Depends(get_current_user)):
    # Check for existing category with the same name for the user
    existing_category = await Category.find_one(Category.name == data.name, Category.owner == current_user.id)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    # Create and save the new category    
    new_category = Category(
        name=data.name,
        color=data.color,
        owner=current_user.id
    )
    await new_category.insert()
    return new_category

@category_router.get("/", response_model=List[CategoryOut])
async def list_categories(current_user: User = Depends(get_current_user)):
    return await Category.find(Category.owner == current_user.id).to_list()