from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#添加中间件

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许所有来源
    allow_credentials=True,#允许验证
    allow_methods=["*"],#允许所有方法
    allow_headers=["*"],#允许所有头
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)