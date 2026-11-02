from sqlalchemy import select, delete, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


#根据news_id查收藏
async def get_favorite_by_user_id_and_news_id(db:AsyncSession, user_id:int, news_id:int):
    stmt=select(Favorite).where((Favorite.user_id==user_id) & (Favorite.news_id==news_id))
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

#添加收藏
async def add_favorite(db:AsyncSession, user_id:int, news_id:int):
    favorite_data=Favorite(user_id=user_id,news_id=news_id)
    db.add(favorite_data)
    await db.commit()
    await db.refresh(favorite_data)
    return favorite_data

#删除收藏
async def remove_favorite(db:AsyncSession, user_id, news_id):
    stmt=delete(Favorite).where((Favorite.user_id==user_id) & (Favorite.news_id==news_id))
    result=await db.execute(stmt)
    return result.rowcount>0


async def get_favorite_list(db:AsyncSession,user_id:int, offset, limit):
   #total：
   stmt=select(func.count()).where(Favorite.user_id==user_id)
   result=await db.execute(stmt)
   total=result.scalar()
   stmt=(select(News,Favorite.created_at.label("favorite_time"))
         .join(Favorite,Favorite.news_id==News.id)
         .where(Favorite.user_id==user_id)
         .order_by(Favorite.created_at.desc())
         .offset(offset)
         .limit(limit)
         )
   result=await db.execute(stmt)
   return result.all(),total


async def clear_all(user_id, db:AsyncSession):
    stmt=delete(Favorite).where(Favorite.user_id==user_id)
    result = await db.execute(stmt)
    return result.rowcount > 0