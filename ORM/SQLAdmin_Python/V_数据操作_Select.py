from sqlalchemy import select
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


# # ============================================================================================================
# # 		Order By
# # ============================================================================================================
# with engine.connect() as conn:
#     # Core写法
#     stmt = select(user_table).order_by(user_table.c.name)
#     result = conn.execute(stmt)
#     print(result.first())

#     # ORM写法
#     stmt = select(User).order_by(User.fullname.desc())
#     result = conn.execute(stmt)
#     print(result.first())

# # ============================================================================================================
# # 		Group By
# # ============================================================================================================
# from sqlalchemy import func

# count_fn = func.count(user_table.c.id)
# print(count_fn)

# with engine.connect() as conn:
#     stmt = select(User.name,
#                   func.count(Address.id).label("count")).join(Address).group_by(User.name).having(func.count(Address.id) > 1)
#     result = conn.execute(stmt)
#     print(result.all())
