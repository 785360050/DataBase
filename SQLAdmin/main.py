from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from watchfiles import PythonFilter

Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://root:187065@127.0.0.1:9200/ORM")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))


Base.metadata.create_all(engine)  # Create tables


from fastapi import FastAPI
from sqladmin import Admin, ModelView

app = FastAPI()
admin = Admin(app, engine)

# 定义表视图
class UserAdmin(ModelView, model=User):
    # ============================================================================================================
    # 		模型的权限控制
    # ============================================================================================================
    can_create       = True  # 是否能创建新记录(提供右上角的添加记录图标)
    can_view_details = True  # 是否能查看详情(记录的眼睛图标)
    can_edit         = True  # 是否能修改记录(提供记录的修改图标)
    can_delete       = True  # 是否能删除(记录的垃圾桶图标,还有批量删除操作)

    # ============================================================================================================
    # 		元数据
    # ============================================================================================================
    name        = "User"                # 记录名称，默认为类名
    name_plural = "Users"               # 记录的复数名，默认为[name]+s
    icon        = "fa-solid fa-user"    # 模型的图标，仅支持FontAwesome 详见https://fontawesome.com/
    category    = "account"             # 左侧的分组

    # ============================================================================================================
    # 		常规选项(表界面和记录界面通用)
    # ============================================================================================================
    def date_format(value):
        return value.strftime("%d.%m.%Y")

    column_labels = {User.id: "ID"}  # 列标签的映射，用于将所有地方的列名称映射到新名称。
    column_type_formatters = dict(ModelView.column_type_formatters, date=date_format)
    save_as = True  # 是否在编辑对象时启用“另存为新”选项。

    # ============================================================================================================
    # 		表界面(表记录总览界面)
    # ============================================================================================================
    column_list            = [User.id, User.name]  # 展示的列, "__all__"为所有的列
    # column_exclude_list    = [User.id]  # 排除显示的列，与column_list只能用一个
    column_searchable_list = [User.name] # 支持搜索的列(只支持一列)
    column_sortable_list   = [User.id, User.name]  # 排序的列(点击列排序)
    # column_default_sort    = [(User.id, True), (User.name, False)]  # 默认排序的依据列(column, is_descending)的格式
    column_formatters      = {User.name: lambda m, a: m.name[:10]}  # 列表页面中列格式化程序的字典?

    # ============================================================================================================
    # 		记录界面
    # ============================================================================================================
    column_details_list         = [User.id, User.name, "user.address.zip_code"]  # 显示的列
    # column_details_exclude_list = [User.id]  # 要排除的列, 与column_details_list冲突
    column_formatters_detail    = {User.name: lambda m, a: m.name[:10]}  # 列格式化程序字典

    # ============================================================================================================
    # 		分页选项
    # ============================================================================================================
    page_size         = 50                  # 分页时的默认页面大小。默认为10.
    page_size_options = [25, 50, 100, 200]  # 分页选择器选项。默认为[10, 25, 50, 100]

    # ============================================================================================================
    # (略)
    # 表单选项
    # 导出选项
    # 模板
    # 活动(类似触发器)
    # 自定义操作
    # ============================================================================================================


# ============================================================================================================
# 		将需要展示的表添加到视图
# ============================================================================================================
admin.add_view(UserAdmin)

#  uvicorn main:app --reload
# 开启服务器
# 浏览器访问url:[ip]/admin  例：  http://127.0.0.1:8000/admin
