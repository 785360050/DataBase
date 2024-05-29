from fastapi import FastAPI
from sqladmin import Admin

from Engine import engine

app = FastAPI()
admin = Admin(app, engine)

from Login import router_login

app.include_router(router_login)






# ============================================================================================================
# 		将需要展示的表添加到视图
# ============================================================================================================
from View import View_Account

admin.add_view(View_Account)

#  uvicorn main:app --reload
# 开启服务器
# 浏览器访问url:[ip]/admin  例：  http://127.0.0.1:8000/admin
