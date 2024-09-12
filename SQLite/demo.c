#include <stdio.h>
#include <stdlib.h>
// #include "../common/util.h"
#include <sqlite3.h>

int callback(void *data, int ncols, char **values, char **headers)
{
    int i;
    fprintf(stderr, "%s: ", (const char *)data);
    for (i = 0; i < ncols; i++)
        printf("%s\t", headers[i]);
    for (i = 0; i < ncols; i++)
        fprintf(stderr, "%s\t", values[i]);

    fprintf(stderr, "\n");
    return 0;//返回成功，继续执行回调，否则终止后续所有sql执行
}
// sudo apt install libsqlite3-dev
// gcc demo.c -g -o main -lsqlite3
int main(int argc, char **argv)
{
    sqlite3 *db;
    int rc = sqlite3_open("test.db", &db);

    if (rc)
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    char *data = "Callback function called";
    char *sql = "select * from test;";

    char *zErr;
    rc = sqlite3_exec(db, sql, callback, data, &zErr);

    if (rc != SQLITE_OK)
    {
        if (zErr != NULL)
        {
            fprintf(stderr, "SQL error: %s\n", zErr);
            sqlite3_free(zErr);
        }
    }

    sqlite3_close(db);

    return 0;
}

