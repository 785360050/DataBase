#include <mysql/mysql.h>
#include <stdio.h>
#include <stdlib.h>

#include <iostream>
int main()
{
    MYSQL *conn;
    MYSQL_RES *res;
    MYSQL_ROW row;

    conn = mysql_init(NULL);

    if (!mysql_real_connect(conn, "192.168.203.132", "User", "187065", "hero_login", 0, NULL, 0))
    {
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(1);
    }

    if (mysql_query(conn, "show databases;"))
    {
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(1);
    }

    res = mysql_use_result(conn);
    std::cout<<"Row Count: "<<res->row_count<<std::endl;

    // 输出查询的结果
    printf("show databases:\n");
    int i{};
    while ((row = mysql_fetch_row(res)) != NULL)
        printf("%d: %s\n", i++,row[0]);

    // 清理
    mysql_free_result(res);
    mysql_close(conn);

    return 0;
}
