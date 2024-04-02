#pragma once

#include <mysql/mysql.h>

#include "../MySQL.hpp"
#include "../SQL.hpp"
#include "../Log.hpp"

#include <iostream>
#include <string>


//基表的基类，负责组装执行对象
class Table
{
protected:
    MYSQL *mysql = nullptr; // 组合连接
    SQL *sql = nullptr;     // 组合执行语句的对象

protected:
    Table(MySQL *mysql)
    {
        this->mysql = mysql->MYSQL_Get();
        if (!mysql)
            throw std::runtime_error("Table Init Failed");
    }
    ~Table() = default;

public:
    void Table_Show(const std::string &table)
    {
        using namespace Database;
        std::string sql{"select * from " + table};
        int failed = mysql_query(mysql, sql.c_str());
        if (failed) // 现在就代表执行失败了
            Log_Error(mysql, "Error: mysql_query !", false);

        // 把查询结果装入 res_ptr
        MYSQL_RES *res_ptr = mysql_store_result(mysql);
        // 存在则输出
        if (!res_ptr)
            Log_Error(mysql, "Result Unexists");

        // 显示查询结果数量
        int affect = mysql_affected_rows(mysql);
        Log("共查询到" + std::to_string(affect) + "组结果");

        // 获取行数，列数
        auto row = mysql_num_rows(res_ptr);
        auto column = mysql_num_fields(res_ptr);

        // 显示列名
        auto fields = mysql_fetch_field(res_ptr);
        for (int i = 0; i < column; ++i)
            std::cout << fields[i].name << '\t';
        std::cout << std::endl;

        if (row <= 0)
            return;

        // 执行输出结果,从第二行开始循环（第一行是字段名）
        for (int i = 1; i < row + 1; i++)
        {
            MYSQL_ROW result_row = mysql_fetch_row(res_ptr); // 每次fetch后移动到下一行
            // 一行数据
            for (int j = 0; j < column; j++)
                std::cout << result_row[j] << '\t';
            std::cout << std::endl;
        }
    }

    // 更新ID=id的学生column列的数据为value
    // void Updata(const string &id, Table_Student::Column column, const string &value, const std::string &contion = "");
};
