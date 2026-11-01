
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class NewsInfoBase(BaseModel):
    id:int
    title:str
    description:str
    image:str
    author:str
    publish_time:datetime=Field(alias="publishTime")
    category_id:int=Field(alias="categoryId")
    views:int
    favorite_time:datetime=Field(alias="favoriteTime")
    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段名兼容
        from_attributes=True  # 允许从ORM属性取值
    )