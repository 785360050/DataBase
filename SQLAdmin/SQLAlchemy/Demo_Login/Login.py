from pydantic import Json
from Server_Instance import app
from fastapi import APIRouter  # 用于在服务器实例中包含当前文件的处理函数

router_login = APIRouter()

from Log import log

from typing import Annotated
from fastapi import Path,Header, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from Table import Account
from Engine import engine
from Session import session

from API import Get_User_Info, Has_Account, Verify_Account


# http://127.0.0.1:8000/API/Login/sh187065
# Body: 187065
@app.get("/API/Login/{account}")
def Account_Login(account: str, password: Annotated[str, Body()]):
    log.debug(f"Login Account: account={account}")
    verified = Verify_Account(account, password)
    if verified:
        return {"Result": "OK", "Account": Get_User_Info(account)}
    else:
        return {"Result": "Failed"}


from Json_Body import Request_Register, Account_Info

from API import Register_Account


@app.post("/API/Login/{account}")
def Account_Register(account: Annotated[str, Path()], json_register: Annotated[Request_Register, Body()]):
    log.debug(f"Register Account: account={account}")
    if Has_Account(account=account):
        return "Failed: Account Existed"

    if Register_Account(account,json_register.password,json_register.name,json_register.phone):
        return {"Result": "OK", "Account": Get_User_Info(account)}
    else:
        return "Failed"


import Json_Body
from API import Update_Account
@app.put("/API/Login/{account}")
def Account_Update(account: str, account_info: Json_Body.Request_Update):
    log.debug(f"Update Account: account={account}")
    if not Has_Account(account):
        return {"Result": "Failed"}

    if Update_Account(account,account_info.password,account_info.name,account_info.phone):
        return {"Result": "OK", "Account": Get_User_Info(account)}
    else:
        return {"Result": "Failed"}
    # return {"account": account, "info": account_request}




from API import Delete_Account
@app.delete("/API/Login/{account}")
def Account_Delete(account: str):
    log.debug(f"Delete Account: account={account}")
    if not Has_Account(account):
        return {"Result": "Exception","description":"No matched account"}
    if Delete_Account(account=account):
        return {"Result": "OK"}
    else :
        return {"Result": "Failed No account"}

# from API import Delete_Account_By
# @app.delete("/API/Login/{account}/{uid}")
# def Account_Delete(uid: Annotated[int, Path(ge=0)]):
#     log.debug(f"Delete Account: uid={uid}")
#     if Delete_Account_By(uid=uid):
#         return "OK"
#     return {"uid": uid}
