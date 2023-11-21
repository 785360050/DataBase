# ============================================================================================================
# 		Core方式
# ============================================================================================================
from I_Engine连接数据库 import engine

import select
from IV_ii_MetaData_Core_Table import user_table, address_table

from sqlalchemy import insert

# insert()生成一个sql insert语句的实例
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
print(stmt)  # INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
print(insert(user_table))  # 如果不指定参数，则插入所有列都为默认值的记录

compiled = stmt.compile(engine)  # 编译为对应数据库的SQL语句
print(compiled)  # INSERT INTO user_account (name, fullname) VALUES (%(name)s, %(fullname)s)
print(compiled.params)  # {'name':'spongebob', 'fullname': 'Spongebob Squarepants'}
# 所以以上两行合并起来，最终的SQL语句就是
# INSERT INTO user_account (name, fullname) VALUES ('fullname', 'Spongebob Squarepants')

# ============================================================================================================
# 		执行语句
# ============================================================================================================


with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
    print(f"插入了{result.rowcount}行数据,记录的主键集合为{result.inserted_primary_key}")

# 如果没有预先.values()指定参数,需要在execute时传入参数，格式如下，此时为传入了多个参数，每个参数用{}包裹
with engine.connect() as conn:
    result = conn.execute(  # 这里的格式化太丑了，晚点调一下
        insert(user_table),
        [
            {
                "name": "sandy",
                "fullname": "Sandy Cheeks"},
            {
                "name": "patrick",
                "fullname": "Patrick Star"}, ],
    )
    conn.commit()

with engine.connect() as conn:
    # returning指定返回的列，可以是多个 (会根据不同的数据库实现决定不同的操作方式)
    # Mysql中没有直接的Returning语法支持，用其他代替的，如SELECT LAST_INSERT_ID() AS last_id;
    # INSERT、UPDATE、DELETE 都支持returning成员函数
    insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
    print(insert_stmt)
    conn.commit()

# ============================================================================================================
# ***   from_select 用于Insert时，插入查询得到的值(偶尔用),通常用于拷贝
# 想要将数据从数据库的其他部分直接复制到一组新的行中，而不实际从客户端获取和重新发送数据时，可以使用此构造
# ============================================================================================================
from sqlalchemy import select

with engine.connect() as conn:
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com").where(user_table.c.id==2)
    result=conn.execute(select_stmt)
    insert_stmt = insert(address_table).from_select(["user_id", "email_address"], select_stmt)
    # print(insert_stmt)
    conn.execute(insert_stmt)
    conn.commit()
