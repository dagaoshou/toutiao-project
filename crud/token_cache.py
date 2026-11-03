from fastapi.encoders import jsonable_encoder

from config.cache_conf import get_json_cache, set_cache, delete_cache

USER_TOKEN = "user:token"
TOKEN_TTL = 24 * 3600  # token有效期24小时，与原先数据库方案保持一致


# 登录/注册时写入缓存: token -> user_id
async def set_cache_token(token: str, user_id: int):
    key = f"{USER_TOKEN}:{token}"
    await set_cache(key, {"user_id": user_id}, expire=TOKEN_TTL)

# 根据token获取缓存中的用户ID
async def get_cache_token(token: str):
    key = f"{USER_TOKEN}:{token}"
    return await get_json_cache(key)

# 登出时删除token缓存
async def delete_cache_token(token: str):
    key = f"{USER_TOKEN}:{token}"
    await delete_cache(key)