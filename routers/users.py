

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.token_cache import delete_cache_token
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, PasswordUpdateRequest
from crud import users
from utils.auth import get_current_user
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
    token=await users.create_token(new_user.id)
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
    token=await users.create_token(user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(messages="登录成功!",data=response_data)

#获取用户详细信息
@router.get("/info")
async def get_user_info(
        user=Depends(get_current_user),
):
    response_data=UserInfoResponse.model_validate(user)
    return success_response(messages="查询用户详细信息成功!",data=response_data)


#更新用户信息
@router.put("/update")
async def update_user_info(
        user_data:UserUpdateRequest,
        user:users.User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db),
):
    updated_user=await users.update_user(user_data,user.username,db)
    if not updated_user:
        raise HTTPException(status_code=500,detail="更新用户信息失败!")
    response_data=UserInfoResponse.model_validate(updated_user)
    return success_response(messages="更新用户信息成功!",data=response_data)
#修改密码
@router.put("/password")
async def update_user_password(
        update_request:PasswordUpdateRequest,
        user:users.User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db),
):
    #判断旧密码密码是否正确
    if not security.verify_password(update_request.old_password,user.password):
        raise HTTPException(status_code=400,detail="原密码错误!")
    #设置新密码
    new_hashed_password=security.get_password_hash(update_request.new_password)
    result=await users.update_password(new_hashed_password,user.username,db)
    if not result:
        raise HTTPException(status_code=500,detail="修改密码失败!")
    return success_response(messages="密码修改成功")
# ... existing code ...
#用户登出（删除Redis中的token，实现立即失效）
@router.post("/logout")
async def user_logout(authorization: str = Header(..., alias="Authorization")):
    token = authorization
    await delete_cache_token(token)
    return success_response(messages="登出成功!")
# ... existing code ...