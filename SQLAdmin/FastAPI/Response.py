from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数

router_response = APIRouter()

from Server_Instance import app


from typing import Annotated

from fastapi import  Header

# ============================================================================================================
# 		Header注意事项
# ============================================================================================================
# 默认情况下，Header会将参数名称字符从下划线 (_) 转换为连字符 (-) 以提取并记录标头。
# Header()的convert_underscores参数可以控制
#
# HTTP 标头不区分大小写，所以可以用user_agent蛇形命名，但是不能user-agent命名，基本任何语言都不支持这样命名规范

# 如果有重复的首部字段可以用 Annotated[list[str]类型的参数来接受
# ============================================================================================================

@app.get("/Header")
# 使用Header提取请求首部的user_agent字段，作为接受参数传入，参数名就是首部字段
async def Get_Header(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# 请求 (user_agent会被自动填充，一般浏览器也会自动生成)
# http://127.0.0.1:8000/Header
# 响应
# {
#   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
# }

# ============================================================================================================
# 		指定返回类型
# 会自动检查返回是是否类型有效，成员是否有效，且可以在docs中显示
# 如果检测到类型无效，会返回错误而不是返回错误的数据，这样客户端只会收到正确的类型数据，而不是有误的数据
# 方式一 使用函数的返回类型注释 -> ReturnType
# 方式二 使用app的response_model参数 例 @app.get("/Return/",response_model=Item)
# 如果两者都有，会优先使用response_model

# 数据过滤和返回类型转换
# 此外还支持类型的过滤，如相似class的，用部分字段的class来返回给客户端，详见https://fastapi.tiangolo.com/tutorial/response-model/
# ============================================================================================================
from Request_Body import Item
@app.get("/Return/")
async def Check_Return_Type(item: Item) -> Item:
    return item


# ============================================================================================================
# 		响应码 status_code指定
# ============================================================================================================
from fastapi import status


# @app.post("/items/", status_code=200) # 直接指定正常响应的代码为200
@app.post("/items/", status_code=status.HTTP_201_CREATED)   # 推荐，使用可读性更好的方式
async def create_item(name: str):
    return {"name": name}
