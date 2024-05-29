from cgitb import reset, text
from curses import flash
from typing import Text
from unittest import result
import uuid

# from mysqlx import Result
from Table import Account
from sqlalchemy.orm import Session
from Engine import engine
from sqlalchemy import false, insert, select, update, delete


def Verify_Account(account: str, password: str) -> bool:
    with Session(engine) as session:
        stmt = select(Account.password).where(Account.account == account)
        result_password: str = session.execute(stmt).scalar_one()
        if result_password == password:
            return True
        else:
            return False


from Json_Body import Account_Info, Request_Register


def Has_Account(account: str) -> bool:
    with Session(engine) as session:
        stmt = select(Account).where(Account.account == account)
        result = session.execute(stmt).scalar_one_or_none()
        if result == None:
            return False
        else:
            return True


def Register_Account(account: str, password: str, name: str, phone: int = None) -> bool:
    with Session(engine) as session:

        new_user = Account(account=account, password=password, name=name, phone=phone)
        session.add(new_user)
        session.commit()

        succees = Verify_Account(account, password)
        if succees:
            return True
        else:
            return False


# with Session(engine) as session:
#     user = Account("aaa", "aaa", "aaa", uuid.uuid1())
#     session.add(user)
#     session.commit()


def Update_Account(account: str, password: str, name: str, phone: str) -> bool:
    with Session(engine) as session:
        # 先定位到记录
        # user:Result = session.execute(select(Account).filter_by(account=account)).all()
        # if len(user) != 1:
        #     return False
        # user:Account=user.scalar_one()
        user = session.execute(select(Account).where(Account.account == account)).scalar_one()
        # 然后直接在记录对象上更改数据
        if password:
            user.password = password
        if name:
            user.name = name
        if phone:
            user.phone = phone
        session.commit()

        return True
        # succees = Verify_Account(account, account_info.password)
        # if succees:
        #     return True
        # else:
        #     return False


def Delete_Account(account: str) -> bool:
    with Session(engine) as session:
        stmt = select(Account).where(Account.account == account)
        user = session.execute(stmt).scalar_one()
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True


# 按uid删除用户
def Delete_Account_By(uid: int) -> bool:
    with Session(engine) as session:
        stmt = select(Account).where(Account.uid == uid)
        user = session.execute(stmt).scalar_one()
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True


from Log import log


def Get_User_Info(account: str) -> Account_Info:
    with Session(engine) as session:
        stmt = select(Account).where(Account.account == account)
        user = session.execute(stmt).scalar_one()
        json = Account_Info(uid=user.uid, password=user.password, account=user.account, name=user.name, phone=user.phone)
        return json
