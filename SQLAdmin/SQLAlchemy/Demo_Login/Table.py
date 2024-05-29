import uuid
from tokenize import String
from pydantic import UUID1
from sqlalchemy import Integer, LargeBinary
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# import sqlalchemy


class Base_Login(DeclarativeBase):  # 继承声明式的基类(DeclarativeBase包含了MetaData)
    pass



# ============================================================================================================
#       声明映射类
# ============================================================================================================
# __tablename__ 指定表名
# mapped_column 声明成员列对应的数据库类型(不指定好像会报错)
# : Mapped[[python数据类型/其他映射类等]]    可略，使用Python的类型注释，将Python类型转为数据库的数据类型
#       适用于简单的数据类型，也可以不指定，或直接使用数据库对应的数据类型
# ============================================================================================================
class Account(Base_Login):
    __tablename__ = "account"  # drogon的model不支持数据表名大写

    # 如果有构造函数会导致sqladmin的ui操作失败
    # def __init__(self, account: str, password: str, name: str, uid:int, phone: str=None):
    #     self.uid      = uid
    #     self.account  = account
    #     self.password = password
    #     self.name     = name
    #     self.phone    = phone

    uid      : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account  : Mapped[str] = mapped_column(String(16),unique=True)
    password : Mapped[str] = mapped_column(String(16))
    name     : Mapped[str] = mapped_column(String(32),comment="用户昵称")
    phone    : Mapped[int] = mapped_column(Integer, comment="手机号", nullable=True)

    def __repr__(self) -> str:
        return f"User(uid={self.uid!r}, account={self.account!r}, password={self.password!r})"


