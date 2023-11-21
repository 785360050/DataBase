from IV_ii_MetaData_Core_Table import metadata_obj

# ============================================================================================================
# 		将定义的表对象写入数据库中
# ============================================================================================================
from I_Engine连接数据库 import engine

metadata_obj.create_all(engine)
# metadata_obj集合中存放了上方定义的所有表对象，所以create_all时将所有集合中的表对象写入数据库中

# ============================================================================================================
# 		执行的操作日志
# ============================================================================================================
# 2023-11-21 10:42:32,953 INFO sqlalchemy.engine.Engine SELECT DATABASE()
# 2023-11-21 10:42:32,953 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:42:32,957 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
# 2023-11-21 10:42:32,957 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:42:32,958 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
# 2023-11-21 10:42:32,959 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:42:32,961 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-21 10:42:32,962 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`user_account`
# 2023-11-21 10:42:32,962 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:42:32,965 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`address`
# 2023-11-21 10:42:32,965 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:42:32,968 INFO sqlalchemy.engine.Engine 
# CREATE TABLE user_account (
#         id INTEGER NOT NULL AUTO_INCREMENT, 
#         name VARCHAR(30), 
#         fullname VARCHAR(30), 
#         PRIMARY KEY (id)
# )


# 2023-11-21 10:42:32,969 INFO sqlalchemy.engine.Engine [no key 0.00063s] {}
# 2023-11-21 10:42:32,996 INFO sqlalchemy.engine.Engine 
# CREATE TABLE address (
#         id INTEGER NOT NULL AUTO_INCREMENT, 
#         user_id INTEGER NOT NULL, 
#         email_address VARCHAR(30) NOT NULL, 
#         PRIMARY KEY (id), 
#         FOREIGN KEY(user_id) REFERENCES user_account (id)
# )


# 2023-11-21 10:42:32,996 INFO sqlalchemy.engine.Engine [no key 0.00054s] {}
# 2023-11-21 10:42:33,029 INFO sqlalchemy.engine.Engine COMMIT
# ============================================================================================================

