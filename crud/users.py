from datetime import datetime, timedelta
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from utils import security
from models.users import User, UserToken
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
#创建token
async def create_token(db:AsyncSession,user_id):
    #生成token
    token=str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=1)
    stmt=select(UserToken).where(UserToken.user_id == user_id)
    result=await db.execute(stmt)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
        #跟新到数据库中
        stmt=update(UserToken).where(UserToken.user_id == user_id).values(token=token,expires_at=expires_at)
        await db.execute(stmt)
        await db.commit()
        await db.refresh(user_token)
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)
    return token
#根据token查询用户信息
async def get_user_by_token(token: str,db:AsyncSession):
    stmt=select(UserToken).where(UserToken.token == token)
    result=await db.execute(stmt)
    user_token=result.scalar_one_or_none()
    if not user_token or user_token.expires_at < datetime.now():
        return None
    stmt=select(User).where(User.id == user_token.user_id)
    result=await db.execute(stmt)
    user=result.scalar_one_or_none()
    if not user:
        return None
    return user

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
