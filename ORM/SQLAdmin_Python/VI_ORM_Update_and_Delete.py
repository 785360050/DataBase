from I_Engine连接数据库 import engine
from IV_i_MetaData_ORM_DeclarativeBase import User, Address
from sqlalchemy.orm import Session
from sqlalchemy import select


# ============================================================================================================
# 		Update
# ============================================================================================================
with Session(engine) as session:
    # 先定位到记录
    sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
    # 然后直接在记录对象上更改数据
    sandy.fullname = "Sandy Squirrel"
    print(sandy in session.dirty) # true 表示记录被修改过，脏数据会在更新时修改数据库记录
    session.flush() # 刷新到内存Table对象
    sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
    print(sandy_fullname)
    session.rollback() # 回退检查是否成功
    sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
    print(sandy_fullname)

# ============================================================================================================
# 		Delete
# ============================================================================================================
with Session(engine) as session:
    session.autoflush=False # 暂时关闭自动刷新
    patrick = session.get(User, 3)
    session.delete(patrick)

    # 只有flush之后，内存中的Table记录才会被删除
    result = session.execute(select(User).where(User.name == "patrick")).first()
    print(result)
    session.flush() # 这里要先删除address的对应记录，不然会抛出异常
    result = session.execute(select(User).where(User.name == "patrick")).first()
    print(result)
    # print(patrick in session)
    session.rollback()


# ============================================================================================================
# 		批量操作
# 基于Core的insert(User,[{1},{2},...])实现，
# 详见https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete
# 例
# from sqlalchemy import insert
# session.execute(
#     insert(User),
#     [
#         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
#         {"name": "sandy", "fullname": "Sandy Cheeks"},
#         {"name": "patrick", "fullname": "Patrick Star"},
#         {"name": "squidward", "fullname": "Squidward Tentacles"},
#         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
#     ],
# )
# ============================================================================================================


# ============================================================================================================
#       session事务回滚
# ============================================================================================================
# 		调用 Session.rollback() 不仅会回滚事务，还会使当前与此会话相关联的所有对象过期，
# 可以查看记录对象的.__dict__查看事务的修改历史
# 例：sandy.__dict__
# ============================================================================================================

# ============================================================================================================
# 		session关闭
# ============================================================================================================
# with时会自动关闭，否则需要手动调用.close()
# 执行的内容：
# - 将所有连接资源释放到连接池，取消（例如回滚）任何正在进行的事务。
# - 从Session中删除所有对象。
# ============================================================================================================
