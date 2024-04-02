#pragma once

#include <string>
#include <vector>
#include <set>
#include <map>

#include <mysql/mysql.h>

// #include "MySQL.hpp"
#include "SQL.hpp"
#include "Log.hpp"

#include <functional>

namespace Mysql
{
    struct Host
    {
        const char *ip_address{"localhost"};
        const char *username{"root"};
        const char *password{"187065"};
        const char *database{"Test"};
        const uint16_t port{3306}; // uint16_t是c++中typedef定义的

    public:
        Host() = default;
        Host(const char *ip_address, const char *username, const char *password, int port){};
        ~Host() = default;
    };

    void Log_Error(const MYSQL *const mysql, const std::string &error_info, bool shut_down = true)
    {
        std::cerr << "[ " << error_info << ':' << mysql_error(const_cast<MYSQL *const>(mysql)) << " ]" << std::endl;
        if (shut_down)
            exit(1);
    }

    void Log(const std::string &info)
    {
        std::cout << "[ " << info << " ]" << std::endl;
    }

    void CR()
    {
        std::cout << std::endl;
    }
}

/// @brief 负责建立数据库的连接
/// @note 每个实例建立一个新连接，单例由用户负责处理
class Database
{
protected:
    std::string name{"Unnamed_Database"};
    std::set<std::string> tables; // 存储所有数据库名

    /// @brief mysql数据库的连接实例，每次调用mysql_real_connect时会建立新连接，所以考虑是否使用单例共享连接
    /// @note mysql_close后会修改为nullptr
    MYSQL *mysql = nullptr;
    SQL &sql{SQL::Instance()}; //
    // std::function<bool(const std::string &, const std::string &&)> String_Filter;//防止sql注入的函数

public:
    Database(std::string name, const Mysql::Host &host)
        : name{name}
    {
        mysql = mysql_init(nullptr);
        if (!mysql)
            Mysql::Log_Error(mysql, "Init Failed"); // 返回并打印错误信息函数

        // 连接设置
        mysql_options(mysql, MYSQL_SET_CHARSET_NAME, "utf8");
        bool reconnect{true}; // 开启自动重连
        mysql_options(mysql, MYSQL_OPT_RECONNECT, &reconnect);

        // TODO 是否需要单例模式实现
        mysql_real_connect(mysql, host.ip_address, host.username, host.password, database, host.port, NULL, 0); // 返回值和参数值的区别？
        // 中间分别是主机，用户名，密码，数据库名，端口号（可以写默认0或者3306等），可以先写成参数再传进去
        if (!mysql)
            Mysql::Log_Error(mysql, "Connect Failed");
        Mysql::Log("Database Connected"); // 连接成功反馈

        //加载数据库到内存
        Get_Tables();
    }
    ~Database()
    {
        mysql_close(mysql); // 成功后mysql重置为nullptr
        Mysql::Log("Database Disconnected");
    }
private:
    /// @brief 获取所有数据库的表，存入tables数组
    void Get_Tables()
    {
        auto res = sql.Execute(mysql,
                               "SELECT table_name "
                               "FROM information_schema.tables "
                               "WHERE table_schema = 'Log';");

        MYSQL_ROW row;
        while ((row = mysql_fetch_row(res)))
            tables.push_back(row[0]);
        mysql_free_result(res);
    }

public:

    /// @brief 检查参数合法后，执行sql语句
    // MYSQL_RES *Execute(const std::string &sql, decltype(String_Filter) filter=nullptr)
    // {
    //     if (!filter(sql, {"'"}))
    //     {
    //         Mysql::Log("Sql Execute Rejected: Invaild strings exists");
    //         return nullptr;
    //     }
    //     return this->sql.Execute(mysql, sql);
    // }
    MYSQL_RES *Execute(const std::string &sql)
    {
        return this->sql.Execute(mysql, sql);
    }
};

class Table : public Database
{
private:
    const std::string name{"Unamed_Table"};
    std::map<std::string,int> columns; // <Column_Name,field_index>存储所有数据库名
public:
    Table(const std::string& database,const Mysql::Host& host,std::string name) 
    : Database(database,host),name{name}
    {
        if (tables.find(name)==tables.end())//Cache实现表匹配
        {
            Mysql::Log("No Matching Table Name");
            exit(1);
        }
        Get_Columns();
    }
    ~Table();

private:
    /// @brief 获取指定数据库中特定表的所有列名
    void Get_Columns()
    {
        auto res = sql.Execute(mysql,
                                                 "SELECT column_name "
                                                 "FROM information_schema.columns "
                                                 "WHERE table_schema = 'Log' AND table_name = 'Log_STD';");

        MYSQL_ROW row;
        int i = 0;
        while ((row = mysql_fetch_row(res)))
            columns[row[0]] =i++;
        mysql_free_result(res);
    }

public: //常用操作的封装
    void Insert();
    void Delete();
    void Update();
    void Select();
};

namespace Mysql_Table
{
    class Log_STD : public Table
    {
    public:
        /// @brief 手动维护
        enum class Column
        { // 每个表的
            Date,
            Time,
            Level,
            Message,
            Platform,
            Process,
            User,
            Path,
            PID,
            Count // 列数
        };

    private:
    public:
        Log_STD();
        ~Log_STD();

    public:
        /// @brief 表初始化时的列自检，防止列对不上导致
        void Check_Column()
        {
        }
    };

}
