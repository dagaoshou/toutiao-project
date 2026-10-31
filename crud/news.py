from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.news import Category
#查询新闻分类列表
async def get_category_list(db:AsyncSession,skip:int=0,limit:int=100):
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()