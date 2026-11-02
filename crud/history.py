from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from sqlalchemy import select, func, delete

from models.news import News


#添加历史记录
async def add_history(db:AsyncSession, user_id, news_id):
    history_content=History(user_id=user_id, news_id=news_id)
    db.add(history_content)
    await db.commit()
    await db.refresh(history_content)
    return history_content


async def get_history_list(db:AsyncSession, user_id, offset, page_size):
    #total:
    total = await db.execute(select(func.count(History.id)).where(History.user_id == user_id))
    total=total.scalar()
    stmt=(select( News.id,
            News.title,
            News.description,
            News.image,
            News.author,
            News.publish_time,
            News.category_id,
            News.views,
            History.view_time.label("viewTime"))
          .join(History, News.id == History.news_id)
          .where(History.user_id == user_id)
          .order_by(History.view_time.desc())
          .offset(offset)
          .limit(page_size))
    result=await db.execute(stmt)
    history_list = [dict(row) for row in result.mappings().all()]
    return history_list, total


async def delete_history(db:AsyncSession, user_id, history_id):
    stmt=delete(History).where((History.id==history_id)&(History.user_id==user_id))
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount>0


async def clear_history(db:AsyncSession, user_id):
    stmt=delete(History).where(History.user_id==user_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount>0