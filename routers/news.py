
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_category_list,get_news_list_by_category, get_news_count, get_news_exists
from crud import news
router=APIRouter(prefix='/api/news',tags=['news'])
#新闻分类路由
@router.get('/categories')
async def get_news_categories(db:AsyncSession=Depends(get_db),skip:int=0,limit:int=100):
    categories=await get_category_list(db,skip,limit)
    return{
        "code":200,
        "message":"返回新闻类别成功!",
        "data":categories
    }
#获取新闻列表路由
@router.get("/list")
async def get_news_list(db:AsyncSession=Depends(get_db),
                       category_id:int=Query(...,alias="categoryId"),
                       page:int=Query(1,ge=1),
                       page_size:int=Query(10,le=100,alias="pageSize")):
    skip=(page-1)*page_size  # 计算跳过数量
    news_list=await get_news_list_by_category(db,category_id,skip,page_size)
    news_count=await get_news_count(db,category_id)
    has_more=await get_news_exists(db,category_id,skip,page_size)
    return{
        "code":200,
        "message":"返回新闻列表成功!",
        "data":{
            "list":news_list,
            "total":news_count,
            "hasMore":has_more
        }
    }
@router.get("/detail")
async def get_news_detail(db:AsyncSession=Depends(get_db),news_id:int=Query(...,alias="id")):
    new_detail=await news.get_news_detail(db,news_id)
    if not new_detail:
        return{
            "code":404,
            "message":"新闻详情不存在!"
        }
    else:
        return{
            "code":200,
            "message":"返回新闻详情成功!",
            "data": {
                "id": new_detail.id,
                "title": new_detail.title,
                "content": new_detail.content,
                "image": new_detail.image,
                "author": new_detail.author,
                "publishTime": new_detail.publish_time,
                "categoryId": new_detail.category_id,
                "views": new_detail.views,
                "relatedNews": []
  }
    }
