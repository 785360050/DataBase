from sqladmin import ModelView
# from Table import Account

# 完整的模板已丢失

# 定义表视图
class View_Account(ModelView, model=Account):
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
    name = "Account"  # 记录名称，默认为类名
    # name_plural = "Users"  # 记录的复数名，默认为[name]+s
    # icon = "fa-solid fa-user"  # 模型的图标，仅支持FontAwesome 详见https://fontawesome.com/
    category = "Login"  # 左侧的分组

    # ============================================================================================================
    # 		表界面(表记录总览界面)
    # ============================================================================================================
    column_list = "__all__"  # 展示的列, "__all__"为所有的列
    # column_searchable_list = [Account.uid] # 支持搜索的列(只支持一列)
    # column_sortable_list   = [User.id, User.name]  # 排序的列(点击列排序)
    # # column_default_sort    = [(User.id, True), (User.name, False)]  # 默认排序的依据列(column, is_descending)的格式
    # column_formatters      = {User.name: lambda m, a: m.name[:10]}  # 列表页面中列格式化程序的字典?

    # ============================================================================================================
    # 		记录界面
    # ============================================================================================================
    column_details_list = [Account.name,Account.phone]  # 显示的列
    column_details_list # 要在详细信息页面中显示的列或列名称的列表。
    # column_details_exclude_list # 详细信息页面中要排除的列或列名称的列表。
    # column_formatters_detail # 详细信息页面中的列格式化程序字典。

    # ============================================================================================================
    # 		分页
    # ============================================================================================================
    page_size = 50  # 分页时的默认页面大小。默认为10
    page_size_options = [25, 50, 100, 200]  # 分页选择器选项。默认为[10, 25, 50, 100]