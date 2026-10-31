
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_category_list
#建议路由
router=APIRouter(prefix='/api/news',tags=['news'])

@router.get('/categories')
async def get_news_categories(db:AsyncSession=Depends(get_db),skip:int=0,limit:int=100):
    categories=await get_category_list(db,skip,limit)
    return{
        "code":200,
        "message":"返回新闻类别成功!",
        "data":categories
    }
