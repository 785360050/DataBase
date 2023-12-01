# ============================================================================================================
# 		获取每行各字段值的不同方式
# ============================================================================================================
# import mysql.connector
# from sqlalchemy import create_engine
# engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:3306/ORM")

# with engine.connect() as connection:
#     result = connection.execute(text("select * from ORM.user_account;"))

from I_Engine连接数据库 import engine

from sqlalchemy.orm import Session
from sqlalchemy import text
with Session(engine) as session:    # 以Session为例

    # ============================================================================================================
    print("[直接调用映射表对象定义的输出记录的格式，输出每条记录方式]") # 获取一条记录的方式
    # ============================================================================================================
    result = session.execute(text("select * from ORM.user_account;"))
    rec_id = 0
    for row in result:
        rec_id += 1
        print(f"Record {rec_id}: {row}")

    # ============================================================================================================
    print("[解包获取每条记录的各个字段]")   # 适用于记录的每个字段都需要提取的场景
    # ============================================================================================================
    result = session.execute(text("select * from ORM.user_account;"))
    rec_id=0
    for id,name,fullname in result:
        rec_id+=1
        print(f"Record {rec_id}: id = {id},name = {name},fullname = {fullname}")

    # ============================================================================================================
    print("[tuple 索引获取每条记录的各个字段]") # 不好看，用下标可读性很差
    # ============================================================================================================
    result = session.execute(text("select * from ORM.user_account;"))
    rec_id = 0
    for row in result:
        rec_id += 1
        print(f"Record {rec_id}: id = {row[0]},name = {row[1]},fullname = {row[2]}")

    # ============================================================================================================
    print("[Row对象动态访问每列的列名作为成员 ]")  # 运行时动态获取列名，无IDE提示
    # ============================================================================================================
    result = session.execute(text("select * from ORM.user_account;"))
    rec_id = 0
    for row in result:
        rec_id += 1
        print(f"Record {rec_id}: id = {row.id},name = {row.name},fullname = {row.fullname}")

    # ============================================================================================================
    print("[通过映射对象mappings()获取每条记录的各个字段，然后用map索引列名访问]")  # 列名也无IDE提示
    # ============================================================================================================
    result = session.execute(text("select * from ORM.user_account;"))
    rec_id = 0
    for row in result.mappings():
        # 这里直接print会报错，所以先提取出来
        rec_id += 1
        id=row["id"]
        name = row["name"]
        fullname = row["fullname"]
        print(f"Record {rec_id}: id = {id},name = {name},fullname = {fullname}")


# ============================================================================================================
# Text使用时如果要在sql语句的生成中传入参数，可以在原text的sql语句中声明变量 :[变量名]，然后第二个参数中赋值该变量(多个变量时用[,...]作为整体)
# (写起来不是很好看，条件查询还是用表达式语言方便，如调where()实现)
# ============================================================================================================
    print("单参数传递")
    result = session.execute(text("SELECT id,name FROM ORM.user_account WHERE id > :y"), {"y": 1})
    for row in result:
        print(f"x: {row.id}  y: {row.name}")
    print("多参数传递,找id∈[1,5] ∩ [3,7]")
    result = session.execute(text("SELECT id,name FROM ORM.user_account WHERE id > :x and id < :y"), [{"x": 0,"y": 5},{"x": 3,"y": 7}])
    for row in result:
        print(f"x: {row.id}  y: {row.name}")
