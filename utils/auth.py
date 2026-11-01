#验证用户权限
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import get_user_by_token


async def get_current_user(
    authorization: str = Header(...,alias="Authorization"),
    db:AsyncSession=Depends(get_db)

):
   user=await get_user_by_token(authorization,db)
   if not user:
       raise HTTPException(status_code=404,detail="用户令牌不存在或已过期!")
   return user