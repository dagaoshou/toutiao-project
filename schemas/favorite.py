#创建是否收藏相应模块
from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsInfoBase


class IsFavoriteResponse(BaseModel):
    isFavorite: bool
class FavoriteIdRequest(BaseModel):
    news_id:int=Field(...,alias="newsId",description="新闻ID")

class FavoriteResponse(BaseModel):
    f_list:list[NewsInfoBase]=Field(alias="list",description="新闻列表")
    total:int
    has_more:bool=Field(alias="hasMore")
    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从ORM属性取值
    )