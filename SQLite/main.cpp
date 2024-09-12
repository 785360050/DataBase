
#include <iostream>
#include <sstream>

#include "Sqlite.hpp"


Sqlite sqlite("foods.sqlite");

void Demo_Execute()
{
    char data[] = "[Callback]";

    // 每条记录都会执行一次回调
    auto row_callback = [](void *data, int ncols, char **values, char **headers) -> int
    {
        std::stringstream ss;
        ss << std::string((char *)data) << " ";
        for (int i = 0; i < ncols; i++)
            ss << headers[i] << ":" << values[i] <<" ";
        std::cout << ss.str() << std::endl;

        return 0; // 返回成功，继续执行回调，否则终止后续所有sql执行
    };

    sqlite.Execute("select * from food_types;", row_callback, data);

}

void Demo_Prepared_Stmt()
{
    Statement stmt("select * from episodes limit 5;", sqlite.instance);

    // 首次执行时会执行sql语句并返回状态结果
    int rc = stmt.Execute();

    // 获取列数
    int ncols = stmt.Column_Count();
    // 获取行数
    int row_count = stmt.Row_Count();

    while (stmt.Next_Row() == SQLITE_ROW) // 无记录时step会返回 SQLITE_DONE
    {
        // 输出当前行的每列元素
        for (int i = 0; i < ncols; i++)
            std::cout << std::any_cast<std::string>(stmt.Column_Value<Storage_Type::Text>(i)) << " ";
            // std::cout << sqlite3_column_text(stmt.stmt, i)<<" ";
        std::cout << std::endl;
    }
    stmt.Reset();//重置后可复用
}

// sudo apt install libsqlite3-dev
// gcc main.cpp -g -o main -lsqlite3
int main(int argc, char const *argv[])
{
    // Demo_Execute();
    Demo_Prepared_Stmt();
}
