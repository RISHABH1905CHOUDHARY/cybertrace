"""User management API routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_user, get_db, require_role
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.pagination import PageResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PageResponse[UserResponse], summary="List all users (Admin only)")
async def list_users(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role([UserRole.ADMIN.value])),
):
    """Retrieve paginated list of registered users. Requires Admin role."""
    count_res = await db.execute(select(func.count(User.id)))
    total = count_res.scalar_one()

    query = select(User).order_by(User.id.asc()).offset(pagination.offset).limit(pagination.page_size)
    items_res = await db.execute(query)
    users = list(items_res.scalars().all())

    return PageResponse.create(items=users, total=total, page=pagination.page, page_size=pagination.page_size)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a user (Admin only)")
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role([UserRole.ADMIN.value])),
):
    """Create a new user with designated role. Requires Admin role."""
    existing = await db.execute(select(User).where(User.email == user_in.email))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    db_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role.value,
        is_active=user_in.is_active,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse, summary="Get user details by ID")
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve user details. Permitted to Admin or the user themselves."""
    if current_user.role != UserRole.ADMIN.value and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="Update user (Admin only)")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(require_role([UserRole.ADMIN.value])),
):
    """Update user attributes (role, name, active status). Requires Admin role."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    data = user_update.model_dump(exclude_unset=True)
    for k, v in data.items():
        if hasattr(v, "value"):
            setattr(user, k, v.value)
        else:
            setattr(user, k, v)

    await db.commit()
    await db.refresh(user)
    return user
