#include <stdio.h>
#include <stdlib.h>

#include <sqlite3.h>
#include <string.h>

int main(int argc, char **argv)
{
    int rc, i, ncols, id, season;
    char *sql;
    sqlite3 *db;
    sqlite3_stmt *stmt;

    sql = "select id,season,name from episodes limit 5";
    sqlite3_open("foods.sqlite", &db);

    sqlite3_prepare(db, sql, strlen(sql), &stmt, NULL);

    ncols = sqlite3_column_count(stmt);
    rc = sqlite3_step(stmt);

    /* Print column information */
    for (i = 0; i < ncols; i++)
    {
        fprintf(stdout, "Column: name=%s, storage class=%i, declared=%s\n",
                sqlite3_column_name(stmt, i),
                sqlite3_column_type(stmt, i),
                sqlite3_column_decltype(stmt, i));
    }

    fprintf(stdout, "\n");

    while (rc == SQLITE_ROW)
    {
        id = sqlite3_column_int(stmt, 0);
        season = sqlite3_column_int(stmt, 1);
        const char* name = sqlite3_column_text(stmt, 2);
        if (name != NULL)
            fprintf(stderr, "Row:  id=%i, season=%i, name='%s'\n", id, season, name);
        else
            fprintf(stderr, "Row:  id=%i, season=%i, name=NULL\n", id, season); /* Field is NULL */

        rc = sqlite3_step(stmt);
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}
