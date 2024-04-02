#include <sys/socket.h>
#include <arpa/inet.h> ///struct sockaddr
#include <unistd.h>    ///R/W
#include <sys/epoll.h>
#include <sys/errno.h>
#include <signal.h>

// C
#include <cstring> // strerror(errno)

// C++
#include <iostream>

#include <source_location>

// User Files
#include "Facilities/Epoll.hpp"
#include "Facilities/Log.hpp"
#include "Facilities/Message.hpp"
#include "Facilities/Address.hpp"
#include "Facilities/Client_Data.hpp"
// #include "Facilities/Timer.hpp"



/// ——————————————————————————————————————————————————————————
///  @brief
/// 持续提供回响服务
/// 使用技术：Epoll轮询,注册信号
/// 使用EPOLLIN和EPOLLOUT分割读写事件，读完后注册写事件，下轮while写完后注册读事件，事件检测有点类似状态机
///
///  @param argv [Port]
///  @return Success = 0 Failed = 1
/// ——————————————————————————————————————————————————————————
int main(int argc, char **argv)
{
    if (argc != 2)
        Log_Error("Usage: [Port]");

    auto socket_server = socket(PF_INET, SOCK_STREAM, 0);
    if (socket_server == -1)
        Log_Error("Socket Error");

    Address address_server(AF_INET, argv[1]);

    if (bind(socket_server, (sockaddr *)&address_server, sizeof(address_server)))
        Log_Error("Bind Error");

    if (listen(socket_server, 5))
        Log_Error("Listen Failed");

    std::string message{"Hello Client"};

    std::string received;
    received.resize(64);

    // epoll
    // 创建epoll
    Epoll epoll;
    // 初始化服务器监听的事件，并添加到epoll监听数组中
    epoll_event event_server;
    event_server.events = EPOLLIN;
    event_server.data.fd = socket_server;
    epoll.Event_Add(socket_server, event_server);

    int socket_client;
    bool server_stop{false}, time_out{false};

    Client_Data *clients = new Client_Data[10]{}; // 存放客户端的数组，上限10人
    while (!server_stop)
    {
        int count_events = epoll.Wait(-1);
        if (count_events == -1)
            Log_Error("Epoll Wait Error", false);
        else if (count_events == 0)
            Log_Error("No Events");

        for (int i = 0; i < count_events; ++i)
        { // 遍历就绪的事件
            int socket_current = epoll.array_events[i].data.fd;
            auto event_current = epoll.array_events[i].events;
            if (socket_current == socket_server) // 服务器事件就绪
            {                                    // 处理新的客户端连接请求
                Address address_client;
                socklen_t len{sizeof(address_client)};
                socket_client = accept(socket_server, (sockaddr *)&address_client, &len);
                if (socket_client == -1)
                    Log_Error("Accept Failed");
                // 连接后创建对应客户端的监听事件
                epoll_event event_client;
                event_client.events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
                event_client.events |= EPOLLONESHOT;//触发一次
                event_client.data.fd = socket_client;
                epoll.Event_Add(socket_client, event_client);

                Log("New Client Connected");
            }
            else                                 // 客户端事件就绪
            {                                    // EPOLLIN | EPOLLOUT | EPOLLRDHUP | EPOLLERR | EPOLLET
                static Message msg;//手法对象声明为static防止while循环后重置
                if (event_current == EPOLLRDHUP) // 客户端断连 bug
                {
                    close(socket_current);
                    Log("Client Closed The Connection");
                    server_stop = true;
                }
                else if (event_current == EPOLLERR) // 客户端出错
                {
                    close(socket_current);
                    Log("Client Error");
                    server_stop = true;
                }
                else if (event_current == EPOLLET)
                {
                    Log("EPOLLET");
                }
                else if (event_current == EPOLLIN) // 读取客户端
                {
                    Log("EPOLLIN");
                    msg.Receive(socket_client);
                    msg.Set(msg.message_receive);

                    //接收消息后注册写就绪事件
                    epoll_event event_client;
                    event_client.events = EPOLLOUT | EPOLLRDHUP | EPOLLERR;
                    event_client.events |= EPOLLONESHOT; // 触发一次
                    event_client.data.fd = socket_client;
                    epoll.Event_Mod(socket_client, event_client);//不能用ADD，只能用MOD修改事件
                }
                else if (event_current == EPOLLOUT)
                {
                    Log("EPOLLOUT");
                    msg.Send(socket_client);
                    Log("Echo Succeeded");

                    //写事件完成后重新注册读就绪事件
                    epoll_event event_client;
                    event_client.events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
                    event_client.events |= EPOLLONESHOT; // 触发一次
                    event_client.data.fd = socket_client;
                    epoll.Event_Mod(socket_client, event_client);
                }
                else
                {
                    Log_Error("Something Went Wrong");
                    server_stop = true;
                }
            }
        }
        Log("Loop");
    }

    // close(file_pipe[0]);
    // close(file_pipe[1]);
    close(socket_server);
    close(socket_client);
}
