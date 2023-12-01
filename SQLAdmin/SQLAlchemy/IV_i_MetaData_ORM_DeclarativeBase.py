# ============================================================================================================
# 		使用 ORM [声明式]定义表元数据
# (Quick_Start中也有这部分的案例，见ORM/SQLAdmin_Python/Quick_Start/ORM_Define.py)
# ============================================================================================================
# 好处
# - 设置列定义的更简洁和 Python 风格，其中 Python 类型可用于表示要在数据库中使用的 SQL 类型
# - 生成的映射类可用于形成在许多情况下维护的 SQL 表达式PEP 484由静态分析工具（例如 Mypy 和 IDE 类型检查器）获取的键入信息
# - 允许同时声明表元数据和持久化/对象加载操作中使用的 ORM 映射类。
# ============================================================================================================

from tokenize import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):  # 继承声明式的基类(DeclarativeBase包含了MetaData)
    pass


# ============================================================================================================
# 		此后所有继承Base的表映射类都会加入对应MetaData的集合中
# 实际上也包含了对应的Table类
# ============================================================================================================

print(Base().metadata)
print(Base().registry)
# DeclarativeBase().registry是映射器配置的核心，可以设置映射模式等，见https://docs.sqlalchemy.org/en/20/orm/mapper_config.html

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


# ============================================================================================================
#       声明映射类
# ============================================================================================================
# __tablename__ 指定表名
# mapped_column 声明成员列对应的数据库类型(不指定好像会报错)
# : Mapped[[python数据类型/其他映射类等]]    可略，使用Python的类型注释，将Python类型转为数据库的数据类型
#       适用于简单的数据类型，也可以不指定，或直接使用数据库对应的数据类型
# ============================================================================================================
class User(Base):
    __tablename__ = "user_account"

    # 可选：指定构造函数，初始化成员变量
    def __init__(self, name: str, fullname: Optional[str] = None):
        self.name = name
        self.fullname = fullname

    id       : Mapped[int]             = mapped_column(primary_key=True)
    name                               = mapped_column(String(30)) # Mapped可略
    fullname : Mapped[Optional[str]]   = mapped_column(String(30))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    # relationship表示关联关系，见ORM/SQLAdmin_Python/VII_ORM相关的对象关系.py
    # 一个User记录对应多个Address记录

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(30))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    # 一个Address记录对应一个User记录

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


from I_Engine连接数据库 import engine

Base.metadata.create_all(engine)
