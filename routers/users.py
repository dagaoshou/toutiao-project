

from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from crud import users
from utils.response import success_response
from utils import security
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
        response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(new_user))
        return success_response(messages="注册成功!",data=response_data)
    raise HTTPException(status_code=500,detail="注册失败!")

#用户登录
@router.post("/login")
async def user_login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    user=await users.get_user_by_username(user_data.username,db)
    if not user:
        raise HTTPException(status_code=400,detail="用户不存在!")
    if not security.verify_password(user_data.password,user.password):
        raise HTTPException(status_code=400,detail="密码错误!")
    token=await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(messages="登录成功!",data=response_data)

