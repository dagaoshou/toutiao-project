import json

import redis.asyncio as redis
REDIS_HOST = "192.168.227.128"
REDIS_PORT = 6379
REDIS_DB = 0

#创建Redis的连接对象
redis_client=redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    password="root"
)
#获取字符串类型数据
async def get_str_cache(key:str):
    try:
       return  await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

#获取：列表,字典:
async def get_json_cache(key:str):
    try:
        data=await redis_client.get(key)
        if data:
            return  json.loads(data)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None
#设置字符串类型缓存
async def set_str_cache(key:str,value:str,expire=None):
    try:
        await redis_client.set(key,value,expire)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
#设置json类型缓存
async def set_cache(key:str,value,expire:int=None):
    try:
        if isinstance(value,dict) or isinstance(value,list):
            value=json.dumps(value,ensure_ascii=False)#中文正常保存
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
