from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
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
#查询新闻详细信息
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
#增加新闻浏览量
async def update_news_view_count(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(stmt)
    if result.rowcount>0:
        return True
    return False
#获取相关信息
async def get_related_news(db:AsyncSession,news_id:int):
    new_detail=await get_news_detail(db,news_id)
    stmt=select(News).where(
        (News.category_id==new_detail.category_id)&
        (News.id!=news_id)).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(5)
    result=await db.execute(stmt)
    news_list=result.scalars().all()
    return [{
        "id": new.id,
        "title": new.title,
        "content": new.content,
        "image": new.image,
        "author": new.author,
        "publishTime": new.publish_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "categoryId": new.category_id,
        "views": new.views,
    }for new in news_list]
