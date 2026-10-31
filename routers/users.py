

from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest
from crud import users
router=APIRouter(prefix="/api/user",tags=['user'])


#用户注册
@router.post("/register")
async def user_register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    username=user_data.username
    user=await users.get_user_by_username(username,db)
    if user:
        raise HTTPException(status_code=400,detail="用户已注册!")
    #注册用户
    new_user=await users.create_user(user_data,db)
    #生成token
    token=await users.create_token(db,new_user.id)
    if new_user:
        return {
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "userInfo": {
                    "id": new_user.id,
                    "username": new_user.username   ,
                    "nickname": new_user.nickname,
                    "avatar": new_user.avatar,
                    "bio": new_user.bio
                }
            }
        }
    raise HTTPException(status_code=500,detail="注册失败!")

