#pragma once


#include <mysql/mysql.h>
#include <string>
#include <iostream>

///显示操作日志
namespace Database
{
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