from uuid import uuid1
from Engine import engine
from Table import Account
from sqlalchemy.orm import Session
from pydantic import UUID1
import uuid

# 插入的每条记录都是一个实例

# 添加到会话以插入记录
with Session(engine) as session:
    uid=uuid.uuid1()
    account_jevon = Account(account="sh187065", password=187065,name="jevon",phone="154554564")
    session.add(account_jevon)  # 添加记录
    # session.flush()
    session.commit()
