from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
#创建异步数据库引擎
url = "mysql+aiomysql://root:mysql@host:3306/news_app?charset=utf8mb4"
engine = create_async_engine(url)
create_async_engine(
    url=url,
    echo=True,
    pool_size=10,
    max_overflow=20,
)
#创建数据库工厂
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#创建异步数据库会话
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        except Exception as e:
            print(e)
        finally:
            await db.close()
