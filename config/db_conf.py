from fastapi import HTTPException

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
#创建异步数据库引擎
url = "mysql+aiomysql://root:mysql@host:3306/news_app?charset=utf8mb4"
engine = create_async_engine(url)
create_async_engine(
    url=url,
    echo=True,
    pool_size=10,
    max_overflow=20,
)
#创建异步数据库工厂
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

#创建异步数据库会话
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await db.close()
