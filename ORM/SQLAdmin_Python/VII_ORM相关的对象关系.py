# ============================================================================================================
# 		ORM对象与其有关联的对象交互
# ============================================================================================================


import imp
from typing import List
from IV_i_MetaData_ORM_DeclarativeBase import Base,User,Address
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


# ============================================================================================================
# 		ORM对象之间的关联要在声明时用relationship定义
# ============================================================================================================
# class User(Base):
#     __tablename__ = "user_account"
#
#     # ... mapped_column() mappings
#
#     addresses: Mapped[List["Address_2"]] = relationship(back_populates="user")
#     # 一个User记录对应多个Address记录
#
# class Address(Base):
#     __tablename__ = "address"
#
#     # ... mapped_column() mappings
#
#     user: Mapped["User_2"] = relationship(back_populates="addresses")
#     # 一个Address记录对应一个User记录
#
# ============================================================================================================
# 		持久化和加载关系
# ============================================================================================================
# 1. 手动构造所有关联的对象，然后再手动添加关系
u1 = User(name="pkrabs", fullname="Pearl Krabs")
print(u1.addresses) # 当创建一个存在关联的表记录时，会自动创建关联的记录

a1 = Address(email_address="pearl.krabs@gmail.com")
u1.addresses.append(a1) # 添加一个关联表的记录实例，此时双方的实例都存在，且关系完整
print(u1.addresses)
# [Address(id=None, email_address='pearl.krabs@gmail.com')]
print(a1.user)
# User(id=None, name='pkrabs', fullname='Pearl Krabs')

# ============================================================================================================
# 2. 另一种方式，直接在构造时指定关联关系
a2 = Address(email_address="pearl@aol.com", user=u1)
print(u1.addresses)
# [Address(id=None, email_address='pearl.krabs@gmail.com'), Address(id=None, email_address='pearl@aol.com')]
print(a2.user==u1)

# ============================================================================================================
# 		关联的对象添加到会话中(内存表对象中)
# ============================================================================================================
from sqlalchemy.orm import Session
from I_Engine连接数据库 import engine

with Session(engine) as session:
    # 上文中，u1对应a1和a2，所以添加u1时，会把所有关联的记录都添加到内存的表对象中
    session.add(u1)
    print(f"u1 in session? {u1 in session}")
    print(f"a1 in session? {a1 in session}")
    print(f"a2 in session? {a2 in session}")
    # add后这三个记录对象都处于挂起状态，可以被写入数据库
    # 而且插入到数据库时，session会自动处理关联的先后关系，如先插入用户，后插入地址

# ============================================================================================================
# 		加载关系(没搞明白)
# 可能涉及到加载器策略，因为写入数据库后，再次访问u1.id会从数据库中select，因为commit后会导致所有记录对象过期
# 详见https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-loader-strategies
# 或见后文“加载器策略”案例
# ============================================================================================================

# ============================================================================================================
# 		查询时使用关系
# ============================================================================================================
from sqlalchemy import select
# 1. 利用关系推导join时的on条件
print(select(Address.email_address).select_from(User).join(User.addresses))
# SELECT address.email_address
# FROM user_account JOIN address ON user_account.id = address.user_id
# 其中.join(User.addresses)包含了on的条件

print(select(Address.email_address).join_from(User, Address))
# SELECT address.email_address
# FROM user_account JOIN address ON user_account.id = address.user_id
# 同上，.join_from(User, Address)包含了on的条件

# ============================================================================================================
# 		加载器策略
# ============================================================================================================
from sqlalchemy.orm import selectinload

with Session(engine) as session:
    # 1. 选择加载
    stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
    result=session.execute(stmt)
    for row in result:
        print(f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})")

    print("2. 联合加载   适用于加载n对1的对象")
    from sqlalchemy.orm import joinedload
    stmt = (select(Address).options(joinedload(Address.user, innerjoin=True)).order_by(Address.id))
    for row in session.execute(stmt):
        print(f"{row.Address.email_address} {row.Address.user.name}")

    print("3. 显式连接 + 预加载")
    from sqlalchemy.orm import contains_eager
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "pkrabs")
        .options(contains_eager(Address.user))
        .order_by(Address.id)
    )
    for row in session.execute(stmt):
        print(f"{row.Address.email_address} {row.Address.user.name}")

    # # 似乎比一下方式好，因为不需要join两次
    # print("")
    # stmt = (
    #     select(Address)
    #     .join(Address.user)
    #     .where(User.name == "pkrabs")
    #     .options(joinedload(Address.user))
    #     .order_by(Address.id)
    # )
    # print(stmt)  # SELECT has a JOIN and LEFT OUTER JOIN unnecessarily

    print("")
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import Mapped
    from sqlalchemy.orm import relationship,mapped_column

    # lazy="raise_on_sql"阻止SQL的延迟加载
    class User_2(Base):
        __tablename__ = "user_account"
        id: Mapped[int] = mapped_column(primary_key=True)
        addresses: Mapped[List["Address"]] = relationship(back_populates="user", lazy="raise_on_sql")


    class Address_2(Base):
        __tablename__ = "address"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
        user: Mapped["User"] = relationship(back_populates="addresses", lazy="raise_on_sql")
