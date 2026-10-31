from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.news import Category, News


#查询新闻分类列表
async def get_category_list(db:AsyncSession,skip:int=0,limit:int=100):
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
#查询指定新闻类别列表
async def get_news_list_by_category(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
#查询指定新闻个数
async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one()  #只返回一个数据，返回多个报错
#查询指定新闻是否还有多余
async def get_news_exists(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    total=await get_news_count(db,category_id)
    return skip+limit<total