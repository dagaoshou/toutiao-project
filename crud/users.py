
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from crud.token_cache import set_cache_token, get_cache_token
from utils import security
from models.users import User
from sqlalchemy import select, update

from schemas.users import UserRequest, UserUpdateRequest
import uuid

#根据username查询用户
async def get_user_by_username(username: str,db:AsyncSession):
    stmt=select(User).where(User.username == username)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
#注册用户
async def create_user(user_data:UserRequest,db:AsyncSession):
    #对密码加密
    user_data.password = security.get_password_hash(user_data.password)
    #创建用户对象
    user=User(username=user_data.username,password=user_data.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
#创建token 存入Redis，TTL由Redis自动管理，不再写数据库user_token表
async def create_token(user_id):
    #生成token
    token = str(uuid.uuid4())
    await set_cache_token(token, user_id)
    return token

#根据token查询用户信息（Redis校验令牌有效性，用户信息回源数据库保证实时）
async def get_user_by_token(token: str, db: AsyncSession):
    data = await get_cache_token(token)
    if not data:
        return None
    stmt = select(User).where(User.id == data["user_id"])
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#跟新用户信息,
async def update_user(user_data:UserUpdateRequest, username, db:AsyncSession):
    stmt=update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result=await db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户更新失败!")
    await db.commit()
    #查询跟新用户
    stmt=select(User).where(User.username==username)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_password(new_password: str, username: str, db: AsyncSession):
    stmt=update(User).where(User.username==username).values(password=new_password)
    result=await db.execute(stmt)
    await db.commit()
    if result.rowcount==0:
        return False
    return True
