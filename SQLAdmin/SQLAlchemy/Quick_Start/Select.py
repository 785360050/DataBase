# ============================================================================================================
# 		只能执行一次的文件，第二次要么修改，要么删表重来
# ============================================================================================================
from ORM_Define import User, Address

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM", echo=True)

engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:3306/ORM", echo=True)
# engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:3306/ORM")

session = Session(engine)

# ============================================================================================================
print("简单查询")
# ============================================================================================================
from sqlalchemy import select

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
# 用面向对象的方式操作数据库是ORM的核心目标的体现之一，会生成对应的sql语句操作数据库

for user in session.scalars(stmt):
    print(user)  # 这里使用了User的__repr__,以自定义的格式输出每一行记录

# ============================================================================================================
print("连接查询")
# ============================================================================================================
stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy@sqlalchemy.org"))
# 第二次之后执行 stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy_cheeks@sqlalchemy.org"))
sandy_address = session.scalars(stmt).one()
print(sandy_address)

# ============================================================================================================
print("Update")
# ============================================================================================================
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"  # 修改email
# 共享上方查询到的sandy_address = session.scalars(stmt).one()

# 例2：查询记录并修改
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
# 添加记录(此处会触发select查询patrick.addresses)

session.commit()
# Session对象会自动跟踪映射对象的更改，会在commit时发出 SQL 语句执行

# ============================================================================================================
print("Delete")
# ============================================================================================================
sandy = session.get(User, 2)
sandy.addresses.remove(sandy_address)
# session.flush() # 因为remove是延时操作，不用commit，只要flush就行 (不刷新好像不生效)

session.delete(patrick)  # 删除patrick表示的整个记录
session.commit()
