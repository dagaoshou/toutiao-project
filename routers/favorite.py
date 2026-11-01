

from fastapi import APIRouter, Path, Query, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.favorite import IsFavoriteResponse, FavoriteIdRequest, FavoriteResponse
from schemas.news import NewsInfoBase
from utils.auth import get_current_user
from crud import favorite
from utils.response import success_response

router=APIRouter(prefix='/api/favorite',tags=['favorite'])

#检查新闻收藏模块
@router.get('/check')
async def check_favorite(
        user=Depends(get_current_user),
        news_id: int=Query(...,description='新闻ID',alias="newsId"),
        db:AsyncSession=Depends(get_db)
):
    user_id = user.id
    favorite_result = await favorite.get_favorite_by_user_id_and_news_id(db, user_id, news_id)
    if favorite_result:
        return success_response(data=IsFavoriteResponse(isFavorite=True))
    else:
        return success_response(data=IsFavoriteResponse(isFavorite=False))
#添加收藏
@router.post("/add")
async def add_favorite(
        news_request: FavoriteIdRequest,
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id = user.id
    favorite_result=await favorite.add_favorite(db, user_id, news_request.news_id)
    if not favorite_result:
        raise HTTPException(status_code=400, detail="添加收藏失败")
    return success_response(messages="收藏成功", data=favorite_result)
#取消收藏
@router.delete("/remove")
async def remove_favorite(
        news_id:int=Query(...,description='新闻ID',alias="newsId"),
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id = user.id
    favorite_result=await favorite.remove_favorite(db, user_id,news_id)
    if not favorite_result:
        raise HTTPException(status_code=400, detail="取消收藏失败")
    return success_response(messages="取消收藏成功")

#获取收藏列表
@router.get("/list")
async def get_favorite_list(
        page:int=Query(1,description='页码，默认为1',alias="page"),
        page_size:int=Query(10,le=100,description='每页条数，默认为10，最大值为100',alias="pageSize"),
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
   offset=(page-1)*page_size
   limit=page_size
   rows,total=await favorite.get_favorite_list(db, user.id, offset, limit)
   has_more=False
   if limit+offset<total:
       has_more = True
   favorite_list=[NewsInfoBase(**new.__dict__,
     favorite_time=favorite_time)
     for new,favorite_time in rows]
   response_data=FavoriteResponse(f_list=favorite_list,total=total, has_more=has_more)
   return success_response(data=response_data)

#清空所有收藏
@router.delete("/clear")
async def clear_all_favorite(
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.clear_all(user.id,db)
    if not result:
        raise HTTPException(status_code=500,detail="清除失败!")
    return success_response(messages="成功清除!")

