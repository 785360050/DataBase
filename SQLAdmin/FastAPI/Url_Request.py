from typing import Union
from enum import Enum

from httpx import delete
from pydantic import BaseModel

from Server_Instance import app
from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数

router_url_request = APIRouter()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


# ============================================================================================================
# 		请求方式
# ============================================================================================================
# app.post()
# app.get()
# app.put()
# app.delete()
#
# app.options()
# app.head()
# app.patch()
# app.trace()
# ============================================================================================================


# 例：
# 指定请求方式为get,url为"/"
@app.get("/")
def read_root():
    return {"Hello": "World"}


# url中的参数写法
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/test")
def Handle_get():
    print("app.get(\"test\") accepted request and Handle_get() is called")
    # return {"msg": "Handle_get"}
    return {"app.get(\"test\") accepted request and Handle_get() is called"}  # 返回类型通常会被转为json格式


# @表示装饰器，使用下方的函数来处理装饰器接受的url请求


# 直接在路径中声明参数，然后在处理函数中获取参数
@app.get("/Account/{username}")
def Account_Login(username: str):
    return {"Result": "Ok", "username": username}


# 如果有多个处理函数可以接受同一个url请求，FastAPI会优先选择先声明的，比如会先处理/Account/{username}
@app.get("/Account/ID/{account_id}")
async def Account_Login_ID(account_id: int):  # 这里指定参数为Int类型
    return {"account_id": account_id}


# {如果访问 http://127.0.0.1:8000/Account/ID/sss 或者/4.2 会报错如下，因为account_id不是int类型
#     "detail": [{
#         "type": "int_parsing",
#         "loc": ["path", "account_id"],
#         "msg": "Input should be a valid integer, unable to parse string as an integer",
#         "input": "4.2",
#         "url": "https://errors.pydantic.dev/2.5/v/int_parsing"}]}

from typing import Annotated
from fastapi import Path, Query


# URL参数验证 (与FastAPI/Url_Parameters.py中的 字符串检查 类似)
@app.get("/Account/ID/{account_id}")  # URL参数是必须的，声明为允许None无效
async def Account_Login_ID_Check(account_id: Annotated[int, Path(title="The ID of the item to get", ge=1,le=1000)],
                                 # Path用于从url中提取对应的参数
                                 # ge=1表示account_id必须>=1,le=1000表示account_id必须<=1000
                                 q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"account_id": account_id}
    if q:
        results.update({"q": q})
    return results



# ============================================================================================================
# 		使用预定义值
# ============================================================================================================
# 先定义class，指定枚举的类型
# 这部分的枚举类型会在docs中生成对应的枚举值，作为选项参数供选择
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):  # 指定参为ModelName的枚举类型
    if model_name is ModelName.alexnet:  # 使用枚举类型判断
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":  # 使用值判断
        return {"model_name": model_name, "message": "LeCNN all the images"}

    # resnet使用defaut判断
    return {"model_name": model_name, "message": "Have some residuals"}


# ============================================================================================================
# 		文件路径作为url的参数
# ============================================================================================================


@app.get("/files/{file_path:path}")  # 一定要指定为path类型，否则OpenAPI是不支持的
async def read_file(file_path: str):
    return {"file_path": file_path}


# http://127.0.0.1:8000/files//files/home/johndoe/myfile.txt
# {"file_path": "/files/home/johndoe/myfile.txt"}
