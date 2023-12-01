# ============================================================================================================
# 		Core风格使用Table
# 		Table定义了表的结构，并且是后续所有Core和ORM的操作对象
# 主要包含了Column和Constraint两部
# ============================================================================================================
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String  # 对应数据库的数据类型

# ============================================================================================================
# 		Table必须指定所属的MetaData对象
# ============================================================================================================
from IV_MetaData import metadata_obj

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(30)),
)

print(f"输出表的所有列: {user_table.c.keys()}")
# ['id', 'name', 'fullname']
print(f"输出表的主键: {user_table.primary_key}")
# PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
print(f"获取id列:{user_table.c.id}")  # 访问Table中Colume的方式，c.[列名]  (无IDE提示)
# user_account.id


from sqlalchemy import ForeignKey

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),  # ForeignKey指定外键匹配的列
    Column("email_address", String(30), nullable=False),  # nullable指定非空约束
)


