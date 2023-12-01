# UUID:
#     标准的“通用唯一标识符”，在许多数据库和系统中作为 ID 常见。
#     在请求和响应中将表示为str.
# datetime.datetime:
#     一条蟒蛇datetime.datetime。
#     在请求和响应中将表示为strISO 8601 格式，例如：2008-09-15T15:53:00+05:00.
# datetime.date:
#     Python datetime.date。
#     在请求和响应中将表示为strISO 8601 格式，例如：2008-09-15.
# datetime.time:
#     一条蟒蛇datetime.time。
#     在请求和响应中将表示为strISO 8601 格式，例如：14:23:55.003.
# datetime.timedelta:
#     一条蟒蛇datetime.timedelta。
#     在请求和响应中将表示为float总秒数。
#     Pydantic 还允许将其表示为“ISO 8601 时间差异编码”，请参阅文档以获取更多信息。
# frozenset:
#     在请求和响应中，被视为相同set：
#     在请求中，将读取列表，消除重复项并将其转换为set.
#     在响应中，set将会转换为list.
#     生成的模式将指定值set是唯一的（使用 JSON 模式uniqueItems）。
# bytes:
#     标准Python bytes。
#     在请求和响应中将被视为str。
#     生成的模式将指定它是str带有binary“格式”的。
# Decimal:
#     标准Python Decimal。
#     在请求和响应中，处理方式与float.
#     您可以在此处检查所有有效的 pydantic 数据类型：Pydantic 数据类型


from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body

# 例
def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    repeat_at: Annotated[time | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration, }



