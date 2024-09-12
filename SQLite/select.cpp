#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>




// sudo apt install libsqlite3-dev
// gcc demo.c -g -o main -lsqlite3
int main(int argc, char **argv)
{
    static sqlite3 *sqlite;
    int rc = sqlite3_open("test.sqlite", &sqlite);
    if (rc)
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(sqlite));
        sqlite3_close(sqlite);
        exit(1);
    }

    char *data = "Callback function called";
    char *sql = "select * from test;";

    char *zErr;

    auto callback = [](void *data, int ncols, char **values, char **headers) -> int
    {
        int i;
        fprintf(stderr, "%s: ", (const char *)data);
        for (i = 0; i < ncols; i++)
            printf("%s\t", headers[i]);
        for (i = 0; i < ncols; i++)
            fprintf(stderr, "%s\t", values[i]);

        fprintf(stderr, "\n");
        return 0; // 返回成功，继续执行回调，否则终止后续所有sql执行
    };
    rc = sqlite3_exec(sqlite, sql, callback, data, &zErr);

    if (rc != SQLITE_OK)
    {
        if (zErr != NULL)
        {
            fprintf(stderr, "SQL error: %s\n", zErr);
            sqlite3_free(zErr);
        }
    }

    sqlite3_close(sqlite);

    return 0;
}

