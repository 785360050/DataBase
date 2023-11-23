from I_Engine连接数据库 import engine
from IV_ii_MetaData_Core_Table import user_table, address_table


# ============================================================================================================
# 		Update
# ============================================================================================================
from sqlalchemy import update

stmt = (update(user_table).where(user_table.c.name == "patrick").values(fullname="Patrick the Star"))
print(stmt)
print(stmt.compile().params)
# UPDATE user_account SET fullname=:fullname WHERE user_account.name = :name_1
# {'fullname': 'Patrick the Star', 'name_1': 'patrick'}

stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
print(stmt)
print(stmt.compile().params)
# UPDATE user_account SET fullname=(:name_1 || user_account.name)
# {'name_1': 'Username: '}

# ============================================================================================================
# 		bindparm用于绑定多个参数
# ============================================================================================================
from sqlalchemy import bindparam

with engine.begin() as conn:
    stmt = update(user_table).where(user_table.c.name == bindparam("oldname")).values(name=bindparam("newname"))
    conn.execute(
        stmt,
        [
            {
                "oldname": "jack",
                "newname": "ed"},
            {
                "oldname": "wendy",
                "newname": "mary"},
            {
                "oldname": "jim",
                "newname": "jake"}, ],
    )
    # 防格式化备份
    # conn.execute(
    #     stmt,
    #     [
    #         {"oldname": "jack", "newname": "ed"},
    #         {"oldname": "wendy", "newname": "mary"},
    #         {"oldname": "jim", "newname": "jake"},
    #     ],
    # )

# ============================================================================================================
# 		子查询相关更新
# ============================================================================================================
from sqlalchemy import select

# 标量子查询
scalar_subq = select(address_table.c.email_address).where(address_table.c.user_id == user_table.c.id).order_by(
    address_table.c.id).limit(1).scalar_subquery()
update_stmt = update(user_table).values(fullname=scalar_subq)
print(update_stmt)

# ============================================================================================================
# 		UPDATE...FROM语法支持
# ============================================================================================================
update_stmt = (update(user_table).where(user_table.c.id == address_table.c.user_id).where(
    address_table.c.email_address == "patrick@aol.com").values(fullname="Pat"))
print(update_stmt)
# UPDATE user_account SET fullname=:fullname FROM address WHERE user_account.id = address.user_id AND address.email_address = :email_address_1

# ============================================================================================================
# 		Mysql特有语法
# ============================================================================================================
# 更新多个表
update_stmt = \
    update(user_table).where(user_table.c.id == address_table.c.user_id).where(
    address_table.c.email_address == "patrick@aol.com").values({
        user_table.c.fullname: "Pat",
        address_table.c.email_address: "pat@aol.com", })
from sqlalchemy.dialects import mysql

print(update_stmt.compile(dialect=mysql.dialect()))
# UPDATE user_account, address
# SET address.email_address="patrick@aol.com", user_account.fullname="Pat"
# WHERE user_account.id = address.user_id AND address.email_address = "pat@aol.com"

# # 参数有序更新(仅示例)  Python 3.7 开始保证 Python 字典 按顺序插入
# update_stmt = update(some_table).ordered_values((some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10))
# print(update_stmt)
# # UPDATE some_table SET y=:y, x=(some_table.y + :y_1)


# ============================================================================================================
# 		Delete
# ============================================================================================================
from sqlalchemy import delete

stmt = delete(user_table).where(user_table.c.name == "patrick")
print(stmt)


delete_stmt = \
    delete(user_table)\
    .where(user_table.c.id == address_table.c.user_id)\
    .where(address_table.c.email_address == "patrick@aol.com")

from sqlalchemy.dialects import mysql
print(delete_stmt.compile(dialect=mysql.dialect()))
# DELETE FROM user_account WHERE user_account.name = :name_1

# ============================================================================================================
# 		多表删除
# ============================================================================================================

delete_stmt = (
    delete(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
)
from sqlalchemy.dialects import mysql
print(delete_stmt.compile(dialect=mysql.dialect()))
# DELETE FROM user_account USING user_account, address
# WHERE user_account.id = address.user_id AND address.email_address = %s

# ============================================================================================================
# 		获取影响的行数 .rowcount
# ============================================================================================================
with engine.begin() as conn:
    result = conn.execute(
        update(user_table)
        .values(fullname="Patrick McStar")
        .where(user_table.c.name == "patrick")
    )
    print(result.rowcount)

# ============================================================================================================
# 		update和delete都支持returing
# ============================================================================================================
update_stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
    .returning(user_table.c.id, user_table.c.name)
)
print(update_stmt)
delete_stmt = (
    delete(user_table)
    .where(user_table.c.name == "patrick")
    .returning(user_table.c.id, user_table.c.name)
)
print(delete_stmt)
