from IV_MetaData import metadata_obj
from I_Engine连接数据库 import engine

metadata_obj.drop_all(engine) # 删除所有表对象集合中所对应的表
# ============================================================================================================
# 2023-11-21 10:50:20,198 INFO sqlalchemy.engine.Engine SELECT DATABASE()
# 2023-11-21 10:50:20,198 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,200 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
# 2023-11-21 10:50:20,200 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,201 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
# 2023-11-21 10:50:20,201 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,203 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-21 10:50:20,203 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`user_account`
# 2023-11-21 10:50:20,204 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,207 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`address`
# 2023-11-21 10:50:20,207 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,209 INFO sqlalchemy.engine.Engine COMMIT
# 2023-11-21 10:50:20,211 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-11-21 10:50:20,212 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`user_account`
# 2023-11-21 10:50:20,212 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,214 INFO sqlalchemy.engine.Engine DESCRIBE `ORM`.`address`
# 2023-11-21 10:50:20,215 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2023-11-21 10:50:20,219 INFO sqlalchemy.engine.Engine
# DROP TABLE address
# 2023-11-21 10:50:20,219 INFO sqlalchemy.engine.Engine [no key 0.00071s] {}
# 2023-11-21 10:50:20,238 INFO sqlalchemy.engine.Engine
# DROP TABLE user_account
# 2023-11-21 10:50:20,238 INFO sqlalchemy.engine.Engine [no key 0.00050s] {}
# 2023-11-21 10:50:20,254 INFO sqlalchemy.engine.Engine COMMIT
# ============================================================================================================
