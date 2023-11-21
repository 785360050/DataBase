from sqlalchemy import MetaData

# ============================================================================================================
# 		MetaData是Table的必备成员，
#       使用Core风格时，一个Table绑定的MetaData对象，表示该Table属于指定的MetaData集合中
#       使用ORM风格时，则可以省略MetaData，因为DeclarativeBase包含MetaData
# ============================================================================================================
metadata_obj = MetaData()
