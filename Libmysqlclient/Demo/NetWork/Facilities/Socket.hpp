#pragma once

#include <sys/socket.h>

#include "Address.hpp"
#include "Message.hpp"

#include "Timer.hpp"


class Socket
{
public:
    int file = -1;   // 文件描述符
    Address address; // 绑定的socket地址

public:
    Socket() = default;
    Socket(int socket) : file(socket){};
    Socket(Address address) : address{address} {};
    Socket(int socket, const sockaddr_in &addr, bool TIME_WAIT = false)
    {
        this->file = socket;
        this->address.address = addr;
        if (TIME_WAIT)
        { // 如下两行是为了避免TIME_WAIT状态, 仅用于调试，实际使用时应该去掉
            int reuse = 1;
            setsockopt(socket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
        }
    }
    ~Socket() = default;
};

// 客户端socket
class Socket_Client : public Socket
{
public:
    Message<32> message; // 收发信息的缓存

public:
    Socket_Client() = default;
    Socket_Client(int socket) : Socket(socket){};
    Socket_Client(int socket, const sockaddr_in &addr, bool TIME_WAIT = false)
        : Socket(socket, addr, TIME_WAIT){};
    ~Socket_Client() = default; // 客户端需要手动处理关闭的逻辑,不能自动析构关闭

public:
    // 关闭连接
    void Close(bool real_close = true)
    {
        if (real_close && (file != -1))
            file = -1;
        close(file);
    }
};

class Timer;

// 客户端socket
class Socket_Client_Timer : public Socket_Client
{
public:
    Timer *timer = nullptr;

public:
    Socket_Client_Timer() = default;
    Socket_Client_Timer(const Socket_Client& client, Timer *timer = nullptr)
        : Socket_Client(client.file,client.address.address,false), timer{timer} {};
    ~Socket_Client_Timer() = default; // 客户端需要手动处理关闭的逻辑,不能自动析构关闭

public:

};

// 服务端socket
class Socket_Server : public Socket
{
private:
public:
    Socket_Server() = default;
    Socket_Server(Address address, bool TIME_WAIT = true) : Socket(address)
    {
        int socket_ = socket(PF_INET, SOCK_STREAM, 0);
        if (socket_ == -1)
            Log_Error("Socket Create Failed");
        file = socket_;
        if (!TIME_WAIT)
        { // 如下两行是为了避免TIME_WAIT状态, 仅用于调试，实际使用时应该去掉
            int reuse = 1;
            setsockopt(socket_, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
        }
    }
    Socket_Server(int socket, const sockaddr_in &addr, bool TIME_WAIT = true)
    {
        this->file = socket;
        this->address.address = addr;
        if (!TIME_WAIT)
        { // 如下两行是为了避免TIME_WAIT状态, 仅用于调试，实际使用时应该去掉
            int reuse = 1;
            setsockopt(socket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
        }
    }
    ~Socket_Server()
    { // 自动关闭server，client不能自动关闭，所以不放在基类
        if (file != -1)
            close(file);
    }

public:
    // bind
    void Bind()
    {
        if (bind(file, (sockaddr *)&address.address, sizeof(sockaddr_in)))
            Log_Error("Bind Failed");
        Log("Binded");
    }
    // listen
    void Listen(int buffer_size = 5)
    {
        if (listen(file, 5))
            Log_Error("Listen Failed");
        Log("Listening");
    }
    // accept
    Socket_Client Accept()
    {
        struct sockaddr_in client_address;
        socklen_t len = sizeof(sockaddr_in);
        int socket_client = accept(file, (struct sockaddr *)&client_address, &len);
        if (socket_client < 0)
            Log_Error("Accept Failed", false);
        Socket_Client client(socket_client, client_address);
        return client;
    }
    // 发送消息给client并关闭连接
    void show_error(int connfd, const char *info)
    {
        printf("%s", info);
        send(connfd, info, strlen(info), 0);
        close(connfd);
    }
};
