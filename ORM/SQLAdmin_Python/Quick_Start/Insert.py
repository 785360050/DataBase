from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM",echo=True)

from sqlalchemy.orm import Session
from ORM_Define import User, Address

with Session(engine) as session:
    spongebob = User(name="spongebob",
                     fullname="Spongebob Squarepants",
                     addresses=[Address(email_address="spongebob@sqlalchemy.org")])
    sandy = User(name="sandy",
                 fullname="Sandy Cheeks",
                 addresses=[
                     Address(email_address="sandy@sqlalchemy.org"),
                     Address(email_address="sandy@squirrelpower.org"), ])
    patrick = User(name="patrick", fullname="Patrick Star")

    session.add_all([spongebob, sandy, patrick]) # 一次添加多个记录
    session.commit()    # 提交事务，Session全部以事务为单位执行，如果有异常，则回滚
