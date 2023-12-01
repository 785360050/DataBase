from Server_Instance import app

from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated  # 用于定义详细的类型注解，如参数检测，标题等注释
from typing import List, Union
from fastapi import Body
# 用于修饰的函数有如下这些
# Path()
# Query()
# Header()
# Cookie()
# Body()
# Form()
# File()

from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数

router_request_body = APIRouter()


# 定义响应主体，客户端可以选择发送主体也可以零散请求，但是响应时需要以结构体的形式返回
class Item(BaseModel):  # 需要继承BaseModel，所有属性都用python的数据类型
    name: str
    description: str | None = None
    price: float | None = None
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# 用于嵌套的子类
class Image(BaseModel):
    url: HttpUrl  # 定义为HttpUrl类型,而不是str，用于检测url的合法性
    name: str


# 字段也可以使用Field来定义属性,如合法值检测，注释等
class Item_Mod(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    # tags: list = [] # list类型的字段
    tags: set[str] | None = set()  # str类型的set字段,元素不重复
    image: Image | None = None  # 嵌套的类字段


# 给docs文档中添加示例结构数据
class Item_Example(BaseModel):
    name: str
    # 方式一 直接在对应字段中设置实例数据
    description: str | None = Field(default=None, examples=["A very nice Item"])  # 这里只给了一个，支持列出多个示例，{ex1,ex2}
    price: float
    tax: float | None = None

    # # 方式二 model_config可以设置docs中的默认示例格式
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [{
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 35.4,
    #             "tax": 3.2, }]}}

    # 方式三 在openai的接口中给示例，见Show_Examples


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
    item_dict = item.model_dump()  # dict()接口已经被弃用，建议使用model_dump()接口
    if item.tax:  # 如果请求有tax，则计算总额，添加额外的一个字段并返回
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 单个主体时可以用embed显示指定单主体请求必须带有主体名
@app.get("/items/Body/{item_id}")
async def single_body(item_id: int, item: Annotated[Item, Body(embed=False)]):
    results = {"item_id": item_id, "item": item}
    return results


# 此时必须有主体名
# 原先可以支持
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }
# embed后的请求格式
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }


# ============================================================================================================
# 		多个参数
# ============================================================================================================
# 不同的结构体参数
@app.get("/items/Body/multi/{item_id}")
async def Get_Multi(item_id: int, item: Item, user: User, importance: Annotated[int, Body(gt=0)]):
    # importance用Body指定为一个主体，没有的话会被默认解析为一个url参数
    # Body指定从主体中提取字段，检查是否值>0
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# 例
# http://127.0.0.1:8000/items/Body/multi/111
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }
# 响应
# {
#     "item_id": 111,
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }


# 多个相同的结构体参数
@app.get("/images/multiple/")
async def create_multiple_images(images: list[Image]):  # list实现了同类型的多个参数
    return images


# 请求
# [
#   {
#     "url": "https://example.com/1",
#     "name": "string"
#   },
#   {
#     "url": "https://example.com/2",
#     "name": "string"
#   }
# ]
# 响应
# [
#     {
#         "url": "https://example.com/1",
#         "name": "string"
#     },
#     {
#         "url": "https://example.com/2",
#         "name": "string"
#     }
# ]


# ============================================================================================================
# 		嵌套类
# ============================================================================================================
@app.get("/items/Body/Embed/{item_id}")
async def Get_Embed_Item(item_id: int, item_mod: Item_Mod):
    # results = {"item_id": item_id, "item": item}
    results = {"tag": item_mod.tags, "image": item_mod.image}
    return results


# 请求
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["rock", "metal", "bar"],
#     "image": {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#     }
# }
# 响应
# {
#     "tag": [
#         "metal",
#         "bar",
#         "rock"
#     ],
#     "image": {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#     }
# }


@app.get("/items/Example/{item_id}")
async def update_item(item_id: int, item_example: Item_Example):
    results = {"item_id": item_id, "item_example": item_example}
    return results


@app.get("/items/Example/Openapi{item_id}")
async def Show_Examples(
    *, item_id: int,
    item: Annotated[Item,
                    Body(openapi_examples={ # 以下三中案例可以在docs中的examples中切换查看(下拉菜单中选择查看)
                        "normal": {
                            "summary": "A normal example",
                            "description": "A **normal** item works correctly.",
                            "value": {
                                "name": "Foo",
                                "description": "A very nice Item",
                                "price": 35.4,
                                "tax": 3.2, }, },
                        "converted": {
                            "summary": "An example with converted data",
                            "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                            "value": {
                                "name": "Bar",
                                "price": "35.4", }, },
                        "invalid": {
                            "summary": "Invalid data is rejected with an error",
                            "value": {
                                "name": "Baz",
                                "price": "thirty five point four", }, }, }, ), ]):
    results = {"item_id": item_id, "item": item}
    return results
