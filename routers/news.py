
from fastapi import APIRouter
#建议路由
router=APIRouter(prefix='/api/news',tags=['news'])

@router.get('/categories')
async def get_news_categories():
    return{"messages:返回新闻类别成功!"}
