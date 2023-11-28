from Server_Instance import app

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数
router_request_body = APIRouter()

# 定义响应主体，客户端可以选择发送主体也可以零散请求，但是响应时需要以结构体的形式返回
class Item(BaseModel):  # 需要继承BaseModel，所有属性都用python的数据类型
    name: str
    description: str | None = None
    price: float | None = None
    tax: float | None = None


# ============================================================================================================
# 		使用结构体作为主题的好处
# ============================================================================================================
# 使用结构体可以方便数据有效性的验证，报错会更具类的定义详细
# 使用类时有更好的IDE提示
# docs文档可读性更好
# ============================================================================================================


# 请求body可以参考docs，如下
# {
#   "name": "item_1",
#   "description": "desc",
#   "price": 10,
#   "tax": 5
# }
# 响应
# {
#     "name": "item_1",
#     "description": "desc",
#     "price": 10.0,
#     "tax": 5.0,
#     "price_with_tax": 15.0
# }
@app.post("/items/Body")
# 声明为参数，可以将请求的参数作为Item对象的一构造参数
async def create_item(item: Item):
    item_dict = item.model_dump() # dict()接口已经被弃用，建议使用model_dump()接口
    if item.tax: # 如果请求有tax，则计算总额，添加额外的一个字段并返回
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
