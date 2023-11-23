from I_Engine连接数据库 import engine
from IV_i_MetaData_ORM_DeclarativeBase import User,Address
from sqlalchemy.orm import Session

# 插入的每条记录都是一个实例
squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

# 添加到会话以插入记录
with Session(engine) as session:
    session.add(squidward) # 添加记录
    session.add(krabs)

    print(session.new) # 查看新增且未提交的记录(挂起的记录)
    # IdentitySet([
    #     User(id=None, name='squidward', fullname='Squidward Tentacles'),
    #     User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])

    # ============================================================================================================
    # 		更新内存中的Table类对象存储的记录
    # 不同于commit，flush不会修改数据库
    # ============================================================================================================
    session.flush()

    # 此时squidward和krabs处于persist状态，可以支持更多的操作
    print(squidward.id)
    print(krabs.id)

    target=session.get(User,4)    # get通过主键获取记录
    print(target)
    print(target is squidward) # 获取的对象等价于之前创建并插入的记录对象

    session.commit()


    