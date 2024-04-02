#pragma once

#include <sys/epoll.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>

#include <cstring>

#include <stdexcept>
#include <iostream>
#include <vector>
#include <array>
#include <iterator>

#include "Log.hpp"

class Epoll_Event
{
public:
    using Event = decltype(epoll_event::events);

private:
    Event event; // 如EPOLLIN等

public:
    Epoll_Event(Event event = EPOLLIN)
    {
        this->event = event;
    }
    ~Epoll_Event() = default;
};

// class Epoll
// {
// // private:
// public:
//     int file_epoll;
//     const int maxsize;

// public:
//     epoll_event *array_events;

// public:
//     Epoll(int maxsize = 10)
//         : maxsize{maxsize}
//     {
//         file_epoll = epoll_create(maxsize);
//         if (file_epoll == -1)
//             Log_Error("Epoll Create Failed");
//         array_events = new epoll_event[maxsize]{};
//         Log("Epoll Created");
//     }

//     ~Epoll()
//     {
//         if (file_epoll)
//         {
//             close(file_epoll);
//             Log("Epoll Destroyed");
//         }
//         if (array_events)
//             delete[] array_events;
//     }
// private:
//     int setnonblocking(int file)
//     {
//         int old_option = fcntl(file, F_GETFL);
//         int new_option = old_option | O_NONBLOCK;
//         fcntl(file, F_SETFL, new_option);
//         return old_option;
//     }

// public:
//     // 添加监听事件
//     void Event_Add(int socket, epoll_event &event)
//     {
//         if (epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event))
//             Log_Error("Event_Add Failed");
//         /* 将文件描述符设置成为非阻塞的 */
//         // fcntl(socket, F_SETFL, fcntl(socket, F_GETFL) | O_NONBLOCK);
//         setnonblocking(socket);
//     }
//     void Event_Add(int socket)
//     {
//         epoll_event event;
//         event.data.fd = socket;
//         event.events = EPOLLIN | EPOLLET;
//         epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event);
//         setnonblocking(socket);
//     }
//     void Event_Mod(int socket, epoll_event &event)
//     {
//         if (epoll_ctl(file_epoll, EPOLL_CTL_MOD, socket, &event))
//             Log_Error("Event_Add Failed");
//     }
//     void Event_Delete(int socket, epoll_event &event)
//     {
//         if (epoll_ctl(file_epoll, EPOLL_CTL_DEL, socket, 0))
//             Log_Error("Event_Add Failed");
//     }

//     int Wait(int time_wait_milliseconds = -1)
//     {
//         return epoll_wait(file_epoll, array_events, maxsize, time_wait_milliseconds);
//     }
// };

class Epoll
{
    // private:
public:
    int file_epoll = -1;
    const int maxsize;

public:
    epoll_event *array_events;

public:
    Epoll(int maxsize = 10)
        : maxsize{maxsize}
    {
        file_epoll = epoll_create(maxsize);
        if (file_epoll == -1)
            Log_Error("Epoll Create Failed");
        array_events = new epoll_event[maxsize];
        Log("Epoll Created");
    }

    ~Epoll()
    {
        if (file_epoll)
        {
            close(file_epoll);
            Log("Epoll Destroyed");
        }
        if (array_events)
            delete[] array_events;
    }

public:
    int setnonblocking(int file)
    {
        int old_option = fcntl(file, F_GETFL);
        int new_option = old_option | O_NONBLOCK;
        fcntl(file, F_SETFL, new_option);
        return old_option;
    }

public:
    // 添加监听事件
    void Event_Add(int socket, epoll_event &event)
    {
        if (epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event))
            Log_Error("Event_Add Failed");
        /* 将文件描述符设置成为非阻塞的 */
        // fcntl(socket, F_SETFL, fcntl(socket, F_GETFL) | O_NONBLOCK);
        this->setnonblocking(socket);
    }
    void Event_Add(int socket, bool one_shot)
    {
        epoll_event event;
        event.data.fd = socket;
        event.events = EPOLLIN | EPOLLET;
        if (one_shot)
            event.events |= EPOLLONESHOT;
        int status = epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event);
        if (status == -1)
            Log_Error(" Event_Add Failed ");
        setnonblocking(socket);
    }
    void Event_Add(int socket)
    {//线程池，触发一次
        epoll_event event;
        event.data.fd = socket;
        event.events = EPOLLIN | EPOLLET | EPOLLRDHUP;
        int status = epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event);
        if (status == -1)
            Log_Error(" Event_Add Failed ");
        setnonblocking(socket);
    }
    void Event_Add_OUT(int socket)
    {
        epoll_event event;
        event.data.fd = socket;
        event.events |= EPOLLOUT;
        int status = epoll_ctl(file_epoll, EPOLL_CTL_ADD, socket, &event);
        if (status == -1)
            Log_Error(" Event_Add Failed ");
        setnonblocking(socket);
    }

    void Event_Mod(int socket, epoll_event &event)
    {
        if (epoll_ctl(file_epoll, EPOLL_CTL_MOD, socket, &event))
            Log_Error("Event_Mod Failed");
    }
    void Event_Delete(int socket)
    {
        if (epoll_ctl(file_epoll, EPOLL_CTL_DEL, socket, 0))
            Log_Error("Event_Delete Failed");
    }

    int Wait(int time_wait_milliseconds = -1)
    {
        return epoll_wait(file_epoll, array_events, maxsize, time_wait_milliseconds);
    }
};
