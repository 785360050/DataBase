#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>

int main(int argc, char **argv)
{
    int rc, i, ncols;
    sqlite3 *db;
    sqlite3_stmt *stmt;
    char *sql;
    const char *tail;

    rc = sqlite3_open("foods.sqlite", &db);
    if (rc)
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    sql = "select * from episodes limit 5;";
    rc = sqlite3_prepare(db, sql, (int)strlen(sql), &stmt, &tail);
    if (rc != SQLITE_OK)
        fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));

    // 首次执行时会执行sql语句并返回状态结果
    rc = sqlite3_step(stmt);

    //获取列数
    ncols = sqlite3_column_count(stmt);
    // 获取行数
    int row_count=sqlite3_data_count(stmt);

    while (rc == SQLITE_ROW ) // 无记录时step会返回 SQLITE_DONE
    {
        // 输出当前行的每列元素
        for (i = 0; i < ncols; i++)
            fprintf(stderr, "'%s' ", sqlite3_column_text(stmt, i));
        fprintf(stderr, "\n");

        // 非首次执行时会移动游标到下一行记录
        rc = sqlite3_step(stmt);
    }

    // 释放stmt资源
    sqlite3_finalize(stmt);

    // 或 需要复用stmt时使用  sqlite3_reset
    // sqlite3_reset(stmt);

    sqlite3_close(db);

    return 0;
}
