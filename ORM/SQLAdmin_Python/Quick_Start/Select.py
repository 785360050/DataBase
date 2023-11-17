from ORM_Define import User, Address

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM", echo=True)

session = Session(engine)

from sqlalchemy import select
stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
# 用面向对象的方式操作数据库是ORM的核心目标的体现之一，会生成对应的sql语句操作数据库

for user in session.scalars(stmt):
    print(user)  # 这里使用了User的__repr__,以自定义的格式输出每一行记录


stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy@sqlalchemy.org"))
sandy_address = session.scalars(stmt).one()
print(sandy_address)
