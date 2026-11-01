from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username:str
    password:str
class PasswordUpdateRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword")
    new_password: str=Field(...,alias="newPassword")
class UserInfoBase(BaseModel):
 """
 ⽤户信息基础数据模型
 """
 nickname: Optional[str] = Field(None, max_length=50, description="昵称")
 avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
 gender: Optional[str] = Field(None, max_length=10, description="性别")
 bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")

class UserInfoResponse(UserInfoBase):
    """
    用户信息响应数据模型
    """
    id:int
    username:str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从ORM属性取值
    )

class UserAuthResponse(BaseModel):
    """
    用户认证信息数据模型
    """
    token: str
    user_info: UserInfoResponse=Field(...,alias="userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias/字段名兼容
        from_attributes=True # 允许从ORM属性取值
    )
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")
    phone: Optional[str] = Field(None, max_length=20, description="电话号码")