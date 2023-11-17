
from ORM_Define import Base, User, Address
# ============================================================================================================
# 		创建数据库表
# ============================================================================================================

from sqlalchemy import create_engine
# 引擎负责连接数据库
engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM")

# 根据上方声明的模型创建数据库表，此处所有继承Base的对象都会被创建
Base.metadata.create_all(engine)
