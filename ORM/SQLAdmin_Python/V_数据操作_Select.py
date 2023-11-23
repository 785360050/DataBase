import email
from re import sub
from sqlalchemy import insert, select
from IV_ii_MetaData_Core_Table import user_table, address_table
from I_Engine连接数据库 import engine

stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)

# Core风格的执行
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(row)

# ORM风格的执行
from sqlalchemy.orm import Session
from IV_i_MetaData_ORM_DeclarativeBase import User, Address

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

# ============================================================================================================
# 		指定select的列
# ============================================================================================================

# Core
select(user_table)  # 选择所有列
select(user_table.c.name, user_table.c.fullname)  # 选择指定列
select(user_table.c["name", "fullname"])  # 选择指定列(推荐)

# ORM
select(User)
with Session(engine) as session:
    row = session.execute(select(User)).first()  # first指定仅返回一条记录 == limit 1
    print(row[0])  # 获取仅存在的第一条记录，这里返回类型是row: Row[Tuple[User]]

    user = session.scalars(select(User)).first()
    print(user)  # user: User 所以不需要下标访问

    # 指定列可以直接访问类的成员变量
    select_stmt = select(User.name, User.fullname).where(User.name == "Sandy")
    result = session.execute(select_stmt)
    print(result.first())  # 输出仅有的一条记录

# ============================================================================================================
# 		标签 相当于as
# ============================================================================================================
from sqlalchemy import func, cast

with engine.connect() as conn:
    stmt = select(("Username: " + user_table.c.name).label("username"), ).order_by(user_table.c.name)
    # 此处是("Username: " + user_table.c.name) as username
    for row in conn.execute(stmt):
        print(f"{row.username}")
    # Username: patrick
    # Username: sandy
    # Username: spongebob

# ============================================================================================================
# 		将文本嵌入查找的元素
# ============================================================================================================
from sqlalchemy import text

with engine.connect() as conn:
    stmt = select(text("'组合的文本'"), user_table.c.name).order_by(user_table.c.name)
    print(conn.execute(stmt).all())

# ============================================================================================================
# 		没看懂和text有什么区别
# ============================================================================================================
from sqlalchemy import literal_column

with engine.connect() as conn:
    stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(user_table.c.name)
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")

# ============================================================================================================
# 		where字句
# 使用的是python的判断表达式，实际执行时会转为对应的SQL语句
# ============================================================================================================
with engine.connect() as conn:
    stmt = select(user_table).where(user_table.c.name == "squidward")
    print(conn.execute(stmt).first())  # None   找不到记录

    # where可以使用多次,默认所有where为AND
    stmt = select(user_table).where(user_table.c.id == 2).where(user_table.c.name == "sandy")
    print(conn.execute(stmt).first())  # (2, 'sandy', 'Sandy Cheeks')

    # 指定条件连接 and(xxx,xxx) 读起来很难受
    from sqlalchemy import and_, or_
    # stmt = select(user_table).where(or_(and_(user_table.c.id == 2, user_table.c.name == "sandy"), user_table.c.id == 1))
    select(Address.email_address).where(and_(
        or_(User.name == "squidward", User.name == "sandy"),
        Address.user_id == User.id,
    ))
    print(conn.execute(stmt).first())  # (2, 'sandy', 'Sandy Cheeks')

    # where(column == xxx)的一种代替filter_by(),
    stmt = select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants")
    print(conn.execute(stmt).first())  # (1, 'spongebob', 'Spongebob Squarepants')

# ============================================================================================================
# 		join 连接查询 、ON 和 From 指定表(单表不需要手动指定)
# 如果表的结构中有foreign key约束，会自动推导on的连接条件
# ============================================================================================================
with engine.connect() as conn:
    # SELECT address.email_address
    # FROM user_account JOIN address ON user_account.id = address.user_id
    # 的三种写法

    # join_from显示指定join的左右侧表: ...from user_table inner join address_table
    # ON条件被自动推断
    stmt = select(user_table.c.name, address_table.c.email_address).join_from(user_table, address_table)
    print(f"[Executing]====\n{stmt}\n===============")
    result = conn.execute(stmt)
    print(result.first())

    # join显示指定右侧，左侧推导出 ...from [推导表] inner join address_table
    # ON条件被自动推断
    stmt = select(user_table.c.name, address_table.c.email_address).join(address_table)
    print(f"[Executing]====\n{stmt}\n===============")
    result = conn.execute(stmt)
    print(result.first())

    # ============================================================================================================
    # 		不清楚select_from的意义
    # ============================================================================================================
    stmt = select(address_table.c.email_address).select_from(user_table).join(address_table)
    print(f"[Executing]====\n{stmt}\n===============")
    result = conn.execute(stmt)
    print(result.first())

    # ============================================================================================================
    # 		手动指定ON(join()和join_from)
    # ============================================================================================================
    stmt = select(address_table.c.email_address).select_from(user_table).join(address_table,
                                                                              user_table.c.id == address_table.c.user_id)

    # ============================================================================================================
    # 		外连接
    # full 指定全外连接(mysql不支持)
    # isouter 指定左/右外连接 (sqlAlchemy只用LEFT OUTER JOIN，不会用右外，右外会交换两个表的位置用左外连接实现)
    # outerjoin方法也能实现，暂不实现
    # ============================================================================================================
    stmt = select(user_table).join(address_table, isouter=True)
    print(stmt)
    result=conn.execute(stmt)
    print(result.all())

    # Mysql 不支持FULL OUTER JOIN 要么左外要么右外连接
    # stmt=select(user_table).join(address_table, full=True)
    # print(stmt)
    # # SELECT user_account.id, user_account.name, user_account.fullname
    # # FROM user_account FULL OUTER JOIN address ON user_account.id = address.user_id
    # result=conn.execute(stmt)
    # print(result.all())


# ============================================================================================================
# 		Order By
# ============================================================================================================
with engine.connect() as conn:
    # Core写法
    stmt = select(user_table).order_by(user_table.c.name)  # user_table.c.name.desc() 指定降序
    print(stmt)
    result = conn.execute(stmt)
    print(result.first())

    # ORM写法
    stmt = select(User).order_by(User.fullname.desc())  # User.fullname默认为升序
    print(stmt)
    result = conn.execute(stmt)
    print(result.first())

# ============================================================================================================
# 		Group By
# ============================================================================================================
from sqlalchemy import func

count_fn = func.count(user_table.c.id)
print(count_fn)

with engine.connect() as conn:
    count_id = func.count(Address.id)
    # # (只需要执行一次)当前每个用户只有一个email地址，为了下方select查找出有多个email地址的用户，手动插入一个新地址
    # conn.execute(insert(address_table).values(id=4, user_id=2, email_address="sandy_2@aol.com"))
    # conn.commit()
    stmt = select(User.name, count_id.label("count")).join(Address).group_by(User.name).having(count_id > 1)
    print(stmt)
    # SELECT user_account.name, count(address.id) AS count
    # FROM user_account JOIN address ON user_account.id = address.user_id GROUP BY user_account.name
    # HAVING count(address.id) > :count_1
    result = conn.execute(stmt)
    print(result.all())

# ============================================================================================================
# 		对表达式进行分类、排序
# 不同于之前的操作，都是将分类和排序作为一个整体的表达式。
# 这样可以复用先前的表达式
# ============================================================================================================
from sqlalchemy import func, desc
stmt_select=select(Address.user_id,func.count(Address.id).label("num_addresses"))
print(stmt_select)
# SELECT address.user_id, count(address.id) AS num_addresses FROM address
stmt_modified = stmt_select.group_by("user_id").order_by("user_id", desc("num_addresses"))
print(stmt_modified)
# SELECT address.user_id, count(address.id) AS num_addresses
# FROM address GROUP BY address.user_id ORDER BY address.user_id, num_addresses DESC

# ============================================================================================================
# 		from 表的别名
# ============================================================================================================
# Core风格
user_alias_1 = user_table.alias()
user_alias_2 = user_table.alias()
stmt = select(user_alias_1.c.name, user_alias_2.c.name)
stmt = stmt.join_from(user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id)
print(stmt)
# SELECT user_account_1.name, user_account_2.name AS name_1
# FROM user_account AS user_account_1 JOIN user_account AS user_account_2 ON user_account_1.id > user_account_2.id


# ORM风格
from sqlalchemy.orm import aliased

address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)
# 查找同一表中存在两个指定邮箱的用户记录
stmt = select(User).join_from(User, address_alias_1).where(address_alias_1.email_address == "patrick@aol.com").join_from(
    User, address_alias_2).where(address_alias_2.email_address == "patrick@gmail.com")
print(stmt)
# SELECT user_account.id, user_account.name, user_account.fullname
# FROM user_account
#   JOIN address AS address_1 ON user_account.id = address_1.user_id
#   JOIN address AS address_2 ON user_account.id = address_2.user_id
# WHERE address_1.email_address = :email_address_1 AND address_2.email_address = :email_address_2




# ============================================================================================================
# 		子查询 .subquery()
# 		CTE   .cte()        (相当于with ...)
# ============================================================================================================
subquery = select(func.count(address_table.c.id).label("count"),address_table.c.user_id).group_by(address_table.c.user_id).subquery()
print(f"Subquery: {subquery}")  # 子查询的sql语句如果单独执行，不会额外添加括号，等价于一个正常的查询语句
# SELECT count(address.id) AS count, address.user_id AS user_id FROM address GROUP BY address.user_id

stmt = select(user_table.c.name, user_table.c.fullname, subquery.c.count).join_from(user_table, subquery)
print(stmt)
# SELECT user_account.name, user_account.fullname, anon_1.count
# FROM user_account
#   JOIN (SELECT count(address.id) AS count, address.user_id AS user_id FROM address GROUP BY address.user_id) AS anon_1
# ON user_account.id = anon_1.user_id


subq = select(func.count(address_table.c.id).label("count"), address_table.c.user_id).group_by(address_table.c.user_id).cte()
print(f"CTE: {subq}")

stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(user_table, subq)
print(stmt)

# 例 mysql 8.0可以，5.7不支持，不清楚是否可以用python避开
with Session(engine) as session:
    stmt_cte=select(User.id,User.name).where(User.id==2).cte()
    stmt=select(Address.email_address).where(Address.user_id==stmt_cte.c.id)
    print(stmt)
    # WITH anon_1 AS
    # (
    #    SELECT user_account.id AS id, user_account.name AS name
    #    FROM user_account
    #    WHERE user_account.id = :id_1
    # )
    # SELECT address.email_address
    # FROM address, anon_1
    # WHERE address.user_id = anon_1.id
    result=session.execute(stmt)
    print(result.all())


# # ORM方式
# # ============================================================================================================
# # 		[ORM 实体子查询/CTE] 没理解
# # ============================================================================================================
# subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
# address_subq = aliased(Address, subq)
# stmt = (select(User, address_subq).join_from(User, address_subq).order_by(User.id, address_subq.id))
# print(stmt)
# # SELECT user_account.id, user_account.name, user_account.fullname, anon_1.id AS id_1, anon_1.email_address, anon_1.user_id
# # FROM user_account
# #   JOIN (SELECT address.id AS id, address.email_address AS email_address, address.user_id AS user_id
# #         FROM address
# #         WHERE address.email_address NOT LIKE :email_address_1) AS anon_1
# # ON user_account.id = anon_1.user_id ORDER BY user_account.id, anon_1.id
# with Session(engine) as session:
#     for user, address in session.execute(stmt):
#         print(f"{user} {address}")

# ============================================================================================================
# 		标量和相关子查询    返回0或一个结果的查询
# ============================================================================================================



# ============================================================================================================
# 		EXISTS 子查询
# ============================================================================================================
# 查找至少有2个email地址的用户名
with engine.connect() as conn:
    subq = select(func.count(address_table.c.id)).where(user_table.c.id == address_table.c.user_id).group_by(
        address_table.c.user_id).having(func.count(address_table.c.id) > 1)
    subq_exist = subq.exists()
    stmt = select(user_table.c.name).where(subq_exist)  # 如果要用NOT EXIST 写成.where(~subq_exist)
    print(stmt)
    # SELECT user_account.name
    # FROM user_account
    # WHERE EXISTS
    # (
    #     SELECT count(address.id) AS count_1
    #     FROM address
    #     WHERE user_account.id = address.user_id GROUP BY address.user_id
    #     HAVING count(address.id) > :count_2
    # )
    result = conn.execute(stmt)
    print(result.all())

# ============================================================================================================
# 		函数
# func命名空间下的任何字符串都会被转为对应函数，
# 例：func.Mysql_Func() 转为执行Mysql_Func()    函数名相同
#
# 常见的函数会被封装成统一的接口(称为内置函数)，对不同数据库执行不同的操作
# 例：
# count()   统计数量
# lower()   字符串转为消息
# now() 获取当前日期和时间，对不同的数据库有不同的处理方式
# ...
# ============================================================================================================
from sqladmin import func

stmt = select(func.now())
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())
    # [(datetime.datetime(2023, 11, 23, 17, 30, 54),)]

    # ============================================================================================================
    # 		内置函数的返回类型通常根据使用环境，动态调整，如max(num)->integer  max(string)->string
    # 		大部分数据库的函数返回NullType类型，需要手动指定，或者根据环境推导，如 NullType + string -> string + string
    # ============================================================================================================
    print(func.now().type)

# ============================================================================================================
# 		高级 SQL 函数技术 (略)
# ============================================================================================================


# ============================================================================================================
# 		数据转换和类型强制  SQL的CAST关键字
# cast()用于在数据库中转换
# cast_coerce()用于在python中转换类型
# ============================================================================================================
from sqlalchemy import cast,String

stmt = select(cast(user_table.c.id, String))  # 指定id列结果转为String类型
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

# cast_coerce案例，暂不执行
# import json
# from sqlalchemy import JSON
# from sqlalchemy import type_coerce
# from sqlalchemy.dialects import mysql

# s = select(type_coerce({"some_key": {"foo": "bar"}}, JSON)["some_key"])
# print(s.compile(dialect=mysql.dialect()))

# SELECT JSON_EXTRACT(%s, %s) AS anon_1