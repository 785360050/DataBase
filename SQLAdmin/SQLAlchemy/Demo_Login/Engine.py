from sqlalchemy import create_engine
# 引擎负责连接数据库
engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM")
