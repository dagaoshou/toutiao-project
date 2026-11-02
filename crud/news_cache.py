from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.cache_conf import get_json_cache,set_cache
from models.news import Category
NEWS_CATEGORY="news:category"
NEWS_LIST="news:list"
#获取新闻分类列表
async def get_cache_category():
    return await get_json_cache(NEWS_CATEGORY)
#添加新闻分类列表
async def set_cache_category(category):
    await set_cache(NEWS_CATEGORY, jsonable_encoder(category), expire=7200)


#获取新闻列表
async def get_cache_list(category_id,page,page_size):
    key=f"{NEWS_LIST}:{category_id}:{page}:{page_size}"
    return await get_json_cache(key)
#设置新闻列表
async def set_cache_list(value,category_id,page,page_size):
    key=f"{NEWS_LIST}:{category_id}:{page}:{page_size}"
    await set_cache(key, jsonable_encoder(value), expire=7200)
