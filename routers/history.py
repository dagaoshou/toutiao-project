from fastapi import APIRouter, Depends, Query, Path
from fastapi import HTTPException
from config.db_conf import get_db
from schemas.history import HistoryAddRequest, HistoryInfo, HistoryInfoResponse
from crud import history
from utils.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from utils.response import success_response

router=APIRouter(prefix="/api/history",tags=["history"])
#添加历史信息
@router.post("/add")
async def add_history(
        history_data: HistoryAddRequest,
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id=user.id
    history_response=await history.add_history(db, user_id, history_data.news_id)
    if not history_response:
        raise HTTPException(status_code=400, detail="添加历史失败")
    return success_response(messages="添加成功", data=history_response)

#获取浏览历史列表
@router.get("/list")
async def get_history_list(
        page:int=Query(1,description='页码，默认为1',alias="page"),
        page_size:int=Query(10,le=100,description='每页数量，默认为10',alias="pageSize"),
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id=user.id
    offset=(page-1)*page_size
    history_list,total=await history.get_history_list(db, user_id, offset, page_size)
    has_more=False
    if offset+page_size<total:
        has_more=True
    history_list=[HistoryInfo.model_validate(row)for row in history_list]
    return success_response(data=HistoryInfoResponse(h_list=history_list, total=total, has_more=has_more))

#删除单挑历史记录
@router.delete("/delete/{history_id}")
async def delete_history(
        history_id:int=Path(...,description="历史记录ID"),
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id=user.id
    await history.delete_history(db, user_id, history_id)
    return success_response(messages="删除成功")

#清空所有历史记录
@router.delete("/clear")
async def clear_history(
        user=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    user_id=user.id
    await history.clear_history(db, user_id)
    return success_response(messages="清空成功")

