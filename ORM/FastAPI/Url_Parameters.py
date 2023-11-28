from ast import List
from Server_Instance import app

from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数

router_url_parameters = APIRouter()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# ============================================================================================================
# 		url中?开启查询，形如key=value，多个查询的key以&字符分隔。
# ============================================================================================================


# 获取前两条数据
# http://127.0.0.1:8000/items/?begin=0&end=2
@app.get("/items/")
async def read_item(begin: int = 0, end: int = 10):
    # 这里给查询参数设置默认值，http://127.0.0.1:8000/items 等价于 http://127.0.0.1:8000/items/?begin=0&end=10
    return fake_items_db[begin:begin + end]
# [{"item_name":"Foo"},{"item_name":"Bar"}]


# 可选参数
# http://127.0.0.1:8000/items/param/10
# {"item_id":"10"}
# http://127.0.0.1:8000/items/param/10?param=10
# {"item_id":"10","param":"10"}
@app.get("/items/param/{item_id}")
async def read_item(item_id: str, param: str | None = None):  # 此处| None说明param不是必须的，如果是必须的不能加| None
    if param:
        return {"item_id": item_id, "param": param}
    return {"item_id": item_id}
# 如果不写| None，则param必须有值，否则会报错如下
# {
#   "detail": [
#     {
#       "type": "missing",
#       "loc": [
#         "query",
#         "needy"
#       ],
#       "msg": "Field required",
#       "input": null,
#       "url": "https://errors.pydantic.dev/2.1/v/missing"
#     }
#   ]
# }


# 参数值的隐式转换，此处的short:bool 可用1,true,True,on,yes代替
# http://127.0.0.1:8000/items/convert/10?param=20&short=1
# {"item_id": "10", "param": "20", "short": "True"}
@app.get("/items/convert/{item_id}")
async def read_item(item_id: str, param: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if param:
        item.update({"param": param})
    if short:
        item.update({"short": "True"})
    return item

# 多路径查询
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item



# ============================================================================================================
# 		字符串检查
# ============================================================================================================
from typing import Annotated,List
from fastapi import Query


# http://127.0.0.1:8000/param_check?q=your_parameter_value
@app.get("/param_check")
#  Query(max_length=30) 检查参数长度最多30，超出时会给其他能处理的函数处理，如果没有则会报错，提示字符串长度超出限制
# Query还有其他的参数可以设置，如min_length, regex, alias, title, description, deprecated, gt, ge, lt, le等
# alias="qqq" 给参数起别名，此处的q为别名，在后面可以直接使用别名
# description="qqq" 给参数起描述
# title="qqq" 给参数起标题
# deprecated=True 给参数设置是否弃用
# include_in_schema=False 给参数设置是否在schema中显示
async def check_param(q: Annotated[str | None, Query(max_length=30)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"size": len(q)})
    return results

# 同时查询多个参数http://127.0.0.1:8000/param_check?q=a&q=b 每个参数都会被检查
@app.get("/param_check/multi")
async def check_param_multi(q: Annotated[List[str] | None, Query(max_length=30)] = ["foo","bar"]): # 多个参数的默认值
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    query_items = {"q": q}
    return query_items
