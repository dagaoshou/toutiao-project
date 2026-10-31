from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from utils import security
from models.users import User, UserToken
from sqlalchemy import select

from schemas.users import UserRequest
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
    user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
    db.add(user_token)
    await db.commit()
    await db.refresh(user_token)
    return token
