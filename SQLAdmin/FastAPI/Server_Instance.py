import imp
from fastapi import FastAPI



# 创建实例，作为所有api的交互点
# ============================================================================================================
# 启动服务器
# ============================================================================================================
# 		 uvicorn main:app --reload
# uvicorn [文件名]:[FastAPI实例名] --reload 开启文件的热重载
#
# jevon@Kubuntu:/mnt/WorkSpace/GitHub/DataBase_Experiment/ORM/FastAPI$ uvicorn main:app --reload
# INFO:     Will watch for changes in these directories: ['/mnt/WorkSpace/GitHub/DataBase_Experiment/ORM/FastAPI']
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [25531] using WatchFiles
# INFO:     Started server process [25533]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# ============================================================================================================
app = FastAPI()

from Url_Request import router_url_request
from Url_Parameters import router_url_parameters
from Request_Body import router_request_body
from Response import router_response

app.include_router(router_url_request)
app.include_router(router_url_parameters)
app.include_router(router_request_body)
app.include_router(router_response)




# ============================================================================================================
# 		Admin部分
# ============================================================================================================
from fastapi import FastAPI
from sqladmin import Admin, ModelView

admin = Admin(app, engine)

from View import View_Account

admin.add_view(View_Account)
