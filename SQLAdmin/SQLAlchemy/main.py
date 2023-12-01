# ============================================================================================================
# 		检查版本
# ============================================================================================================
import sqlalchemy
print(sqlalchemy.__version__  )


# ============================================================================================================
# 		连接数据库
# ============================================================================================================
import mysql.connector
print(mysql.connector.__version__)

from sqlalchemy import create_engine
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/test",echo=True)
engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/test")




# ============================================================================================================
# 		使用connection风格的数据库操作
# ============================================================================================================
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("select * from test.t1;"))
    for row in result:
        print(row)
    conn.commit()




# ============================================================================================================
# 		使用Session的数据库操作
# ============================================================================================================
from sqlalchemy.orm import Session
with Session(engine) as session:
    result = session.execute(text("SELECT m1,n1 FROM test.t1;"))
    for row in result:
        print(row)




# 准备元数据(数据库系统数据)，后续创建新表
from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(50)),
)

print(user_table.c.name)

print(user_table.c.keys())

print(user_table.primary_key)

from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(30), nullable=False),
)

# 根据所有创建的信息(保存在metadata中)，在数据库中创建表
metadata_obj.create_all(engine)
