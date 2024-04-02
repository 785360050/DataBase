#pragma once

#include <cstring>
#include <string>
#include <iostream>

void Log_Error(const std::string &error_info, bool shut_down = true)
{
    std::cerr << "[ " << error_info << ':' << strerror(errno) << " ]" << std::endl;
    if (shut_down)
        exit(1);
}

const void Log(const std::string &info) 
{
    std::cout << "[ " << info << " ]" << std::endl;
}