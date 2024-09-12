#pragma once

#include <sqlite3.h>
#include <iostream>
#include <cstring>

#include <any>

enum Storage_Type : int
{
    Integer = 0,
    Float,
    Text,
    Blob,
    Null
};

struct Statement
{
    sqlite3_stmt *stmt; // 查询句柄
    const char *rest;   // 剩余未处理的sql语句
    Statement(const char *query, sqlite3 *db)
    {
        const char *tail;
        int rc = sqlite3_prepare(db, query, (int)strlen(query), &stmt, &rest);
        if (rc != SQLITE_OK)
            throw std::runtime_error(sqlite3_errmsg(db));
    }
    ~Statement() { sqlite3_finalize(stmt); }

    int Row_Count() { return sqlite3_data_count(stmt); }
    int Column_Count() { return sqlite3_column_count(stmt); }
    // 获取字段类型(枚举类型),例: SQLITE_INTEGER 宏
    Storage_Type Column_Type(int index) { return static_cast<Storage_Type>(sqlite3_column_type(stmt, index)); }
    // 获取字段类型(字符类型),例: "INTEGER"
    std::string Column_Decltype(int index) { return sqlite3_column_decltype(stmt, index); }
    // 获取字段列名
    std::string Column_Name(int index) { return sqlite3_column_name(stmt, index); }

    template <Storage_Type T>
    std::any Column_Value(int index)
    {
        switch (T)
        {
        case Storage_Type::Integer:
            return sqlite3_column_int(stmt, index);
        case Storage_Type::Float:
            return sqlite3_column_double(stmt, index);
        case Storage_Type::Text:
            // return sqlite3_column_text(stmt, index);
            return std::string{(const char *)sqlite3_column_text(stmt, index)};
        case Storage_Type::Blob:
            return sqlite3_column_blob(stmt, index);
        // case Storage_Type::Null:
        //     return sqlite3_column_value(stmt, index);
        default:
            return nullptr;
        }
    }

    void Reset() { sqlite3_reset(stmt); }

    // 检查sql语句是否完整(不一定有效)
    static bool Is_Complete(const std::string &stmt) { return sqlite3_complete(stmt.c_str()); }

    int Execute() { return sqlite3_step(stmt); }
    int Next_Row() { return sqlite3_step(stmt); }
};

class Sqlite
{
public:
    sqlite3 *instance{};

public:
    Sqlite(const char *database_file = "test.sqlite")
    {
        if (sqlite3_open(database_file, &instance))
        {
            std::cout << "Can't open database: " << sqlite3_errmsg(instance) << std::endl;
            sqlite3_close(instance);
        }
    }
    ~Sqlite()
    {
        sqlite3_close(instance);
    }

public:
    std::string Get_Error() { return sqlite3_errmsg(instance); }

    using Callback = int (*)(void *data, int ncols, char **values, char **headers);
    /// @brief
    /// @param sql
    /// @param callback
    /// @param data 回调函数的收个参数
    void Execute(const char *sql, Callback callback = nullptr, char *info = nullptr)
    {
        char *error_message; // 执行的错误消息
        int rc = sqlite3_exec(instance, sql, callback, info, &error_message);
        if (rc != SQLITE_OK)
        {
            if (error_message == NULL)
                throw std::runtime_error(sqlite3_errmsg(instance));
            else
            {
                throw std::runtime_error(error_message);
                sqlite3_free(error_message);
            }
        }
    }
};
