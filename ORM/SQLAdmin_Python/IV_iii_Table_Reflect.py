from pydoc import describe
from sqlalchemy import Table
from IV_MetaData import metadata_obj
from I_Engine连接数据库 import engine

table_address = Table("address", metadata_obj, autoload_with=engine)
print(repr(table_address))
# Table('address',
#       MetaData(),
#       Column('id', Integer(), table=<address>, primary_key=True, nullable=False),
#       Column('user_id', Integer(), ForeignKey('user_account.id'), table=<address>, nullable=False),
#       Column('email_address', String(length=30), table=<address>, nullable=False),
#       schema=None)
