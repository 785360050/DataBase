# 快速入门 https://docs.sqlalchemy.org/en/20/orm/quickstart.html

# ============================================================================================================
# 		声明模型
# ============================================================================================================

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):  # 初始化
    pass


class User(Base):  # 创建表对象
    __tablename__ = "user_account"  # 表名

    # 列名
    # Mapped[]对应的类型 如 int -> INTEGER  str -> VARCHAR等
    id: Mapped[int] = mapped_column(primary_key=True)  # 这里mapped_column指定id列为primary_key
    # 至少应该有一列有primary_key
    name: Mapped[str] = mapped_column(String(30))  # 这里mapped_column指定DB的存储类型为varchar(30)
    fullname: Mapped[Optional[str]] = mapped_column(String(30))  # Optional表示是否可以为NULL
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # relationship为表之间的关系, 一个user对应多个address，一个address对应一个user

    def __repr__(self) -> str:  # 自定义输出格式，方便后续数据每行记录 representation的缩写
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))  # 外键索引，address.user_id = user_account.id
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# print(User())
# print(Address())
# # User(id=None, name=None, fullname=None)
# # Address(id=None, email_address=None)


