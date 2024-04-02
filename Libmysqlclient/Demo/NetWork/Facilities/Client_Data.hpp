#pragma once

#include "Timer.hpp"

class Timer;

// 用户数据
struct Client_Data
{
    int socket;
    Address address;
    // char buf[BUFFER_SIZE];
    Timer *timer = nullptr;

public:
    Client_Data()
        : socket(-1), timer(nullptr){};
    Client_Data(int socket, Address address, Timer *timer)
        : socket(socket), address(address), timer(timer){};
    ~Client_Data() = default;
};