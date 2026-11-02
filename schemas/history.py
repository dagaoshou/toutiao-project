from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HistoryAddRequest(BaseModel):
    news_id:int=Field(...,alias="newsId",description="新闻ID")
    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从ORM属性取值
    )
class HistoryInfo(BaseModel):
    id: int
    title: str
    description: str
    image: str
    author: str
    publish_time:datetime = Field(alias="publishTime")
    category_id: int = Field(alias="categoryId")
    views: int
    view_time: datetime = Field(alias="viewTime")
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从ORM属性取值
    )
class HistoryInfoResponse(BaseModel):
    h_list: list[HistoryInfo] = Field(alias="list", description="历史列表")
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从ORM属性取值
    )