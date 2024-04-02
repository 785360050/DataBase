#pragma once

#include <string>

#include "Log.hpp"

#include <unordered_set>

// // 负责执行SQL语句、显示结果(需要与MySQL组合)
// // 防止SQL注入的过滤
// class SQL
// {
// private:
// public:
//     SQL() = default;
//     ~SQL() = default;

// public:
//     // 防止SQL注入
//     virtual bool Parameter_Check(const std::string &sql)
//     {
//         std::unordered_set<std::string> key{"and", "or", "*", "=", " ", "%0a", "%", "/", "union", "|", "&", "^", "#", "/*", "*/"};
//         for (const auto &x : key)
//         {
//             if (sql.find(x) != std::string::npos)
//             {
//                 Database::Log("SQL Injection Exisit");
//                 return false;
//             }
//         }
//         return true;
//     }

//     static MYSQL_RES *Query_Execute(const MYSQL *const mysql, const std::string &sql)
//     {
//         Database::Log("Executing SQL: " + sql);
//         int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql.c_str());
//         if (failed) // 现在就代表执行失败了
//             Database::Log_Error(mysql, "Error: mysql_query !", false);

//         // 返回结果
//         return mysql_store_result(const_cast<MYSQL *const>(mysql));
//     }

//     static MYSQL_RES *Query_Execute(const MYSQL *const mysql, const char *sql)
//     {
//         Database::Log("Executing SQL: " + std::string(sql));
//         int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql);
//         if (failed) // 现在就代表执行失败了
//             Database::Log_Error(mysql, "SQL Query Failed: ", false);
//         return mysql_store_result(const_cast<MYSQL *const>(mysql));
//     }

//     void Result_Show(const MYSQL *const mysql, MYSQL_RES *res_ptr)
//     {
//         // 存在则输出
//         if (!res_ptr)
//             Database::Log_Error(mysql, "Result Unexists");

//         // 显示查询结果数量
//         int affect = mysql_affected_rows(const_cast<MYSQL *const>(mysql));
//         Database::Log("共查询到" + std::to_string(affect) + "组结果");

//         // 获取行数，列数
//         auto row = mysql_num_rows(res_ptr);
//         auto column = mysql_num_fields(res_ptr);

//         // 显示列名
//         auto fields = mysql_fetch_field(res_ptr);
//         for (int i = 0; i < column; ++i)
//             std::cout << fields[i].name << '\t';
//         std::cout << std::endl;

//         if (row <= 0)
//             return;

//         // 执行输出结果,从第二行开始循环（第一行是字段名）
//         for (int i = 1; i < row + 1; i++)
//         {
//             MYSQL_ROW result_row = mysql_fetch_row(res_ptr); // 每次fetch后移动到下一行
//             // 一行数据
//             for (int j = 0; j < column; j++)
//                 std::cout << result_row[j] << '\t';
//             std::cout << std::endl;
//         }
//     }

// };

//第二版
// class SQL
// { 
//     // 是否应该考虑多线程版本，收集map<database,sql>后生产消费
//     // 负责与数据库交互
// private:
    

// private: //仅允许内部构造
//     SQL()  = default;
//     ~SQL() = default;

// public: // 单例阻止拷贝构造和拷贝赋值
//     SQL(const SQL &) = delete;
//     SQL &operator= (const SQL &) = delete;

// public: 
//     static SQL &Instance()
//     { // 局部静态变量，线程安全
//         static SQL instance;  
//         return instance;
//     };

// public:
// public:
//     // 防止SQL注入
//     virtual bool Parameter_Check(const std::string &sql)
//     {
//         std::unordered_set<std::string> key{"and", "or", "*", "=", " ", "%0a", "%", "/", "union", "|", "&", "^", "#", "/*", "*/"};
//         for (const auto &x : key)
//         {
//             if (sql.find(x) != std::string::npos)
//             {
//                 Database::Log("SQL Injection Exisit");
//                 return false;
//             }
//         }
//         return true;
//     }

//     static MYSQL_RES *Query_Execute(const MYSQL *const mysql, const std::string &sql)
//     {
//         Database::Log("Executing SQL: " + sql);
//         int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql.c_str());
//         if (failed) // 现在就代表执行失败了
//             Database::Log_Error(mysql, "Error: mysql_query !", false);

//         // 返回结果
//         return mysql_store_result(const_cast<MYSQL *const>(mysql));
//     }

//     static MYSQL_RES *Query_Execute(const MYSQL *const mysql, const char *sql)
//     {
//         Database::Log("Executing SQL: " + std::string(sql));
//         int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql);
//         if (failed) // 现在就代表执行失败了
//             Database::Log_Error(mysql, "SQL Query Failed: ", false);
//         return mysql_store_result(const_cast<MYSQL *const>(mysql));
//     }

//     void Result_Show(const MYSQL *const mysql, MYSQL_RES *res_ptr)
//     {
//         // 存在则输出
//         if (!res_ptr)
//             Database::Log_Error(mysql, "Result Unexists");

//         // 显示查询结果数量
//         int affect = mysql_affected_rows(const_cast<MYSQL *const>(mysql));
//         Database::Log("共查询到" + std::to_string(affect) + "组结果");

//         // 获取行数，列数
//         auto row = mysql_num_rows(res_ptr);
//         auto column = mysql_num_fields(res_ptr);

//         // 显示列名
//         auto fields = mysql_fetch_field(res_ptr);
//         for (int i = 0; i < column; ++i)
//             std::cout << fields[i].name << '\t';
//         std::cout << std::endl;

//         if (row <= 0)
//             return;

//         // 执行输出结果,从第二行开始循环（第一行是字段名）
//         for (int i = 1; i < row + 1; i++)
//         {
//             MYSQL_ROW result_row = mysql_fetch_row(res_ptr); // 每次fetch后移动到下一行
//             // 一行数据
//             for (int j = 0; j < column; j++)
//                 std::cout << result_row[j] << '\t';
//             std::cout << std::endl;
//         }
//     }
// };

class SQL
{
    // 是否应该考虑多线程版本，收集map<database,sql>后生产消费
    // 负责与数据库交互
private:
private: // 仅允许内部构造
    SQL() = default;
    ~SQL() = default;

public: // 单例阻止拷贝构造和拷贝赋值
    SQL(const SQL &) = delete;
    SQL &operator=(const SQL &) = delete;
public:
    static SQL &Instance()
    { // 局部静态变量，线程安全
        static SQL instance;
        return instance;
    };

public:
public:
    // 防止SQL注入
    virtual bool Parameter_Check(const std::string &sql)
    {
        std::unordered_set<std::string> key{"and", "or", "*", "=", " ", "%0a", "%", "/", "union", "|", "&", "^", "#", "/*", "*/"};
        for (const auto &x : key)
        {
            if (sql.find(x) != std::string::npos)
            {
                Database::Log("SQL Injection Exisit");
                return false;
            }
        }
        return true;
    }

    static MYSQL_RES *Execute(const MYSQL *const mysql, const std::string &sql)
    {
        Database::Log("Executing SQL: " + sql);
        int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql.c_str());
        if (failed) // 现在就代表执行失败了
            Database::Log_Error(mysql, "Error: mysql_query !", false);

        // 返回结果
        return mysql_store_result(const_cast<MYSQL *const>(mysql));
    }

    static MYSQL_RES *Execute(const MYSQL *const mysql, const char *sql)
    {
        Database::Log("Executing SQL: " + std::string(sql));
        int failed = mysql_query(const_cast<MYSQL *const>(mysql), sql);
        if (failed) // 现在就代表执行失败了
            Database::Log_Error(mysql, "SQL Query Failed: ", false);
        return mysql_store_result(const_cast<MYSQL *const>(mysql));
    }

    void Result_Show(const MYSQL *const mysql, MYSQL_RES *res_ptr)
    {
        // 存在则输出
        if (!res_ptr)
            Database::Log_Error(mysql, "Result Unexists");

        // 显示查询结果数量
        int affect = mysql_affected_rows(const_cast<MYSQL *const>(mysql));
        Database::Log("共查询到" + std::to_string(affect) + "组结果");

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
};