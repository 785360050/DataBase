#pragma once

#include <unistd.h>

#include <iostream>
#include <string>
#include <iterator>

#include "Log.hpp"

template <int maxsize = 32>
class Message
{
private:
public:
    // static const int maxsize;
    char message_send[maxsize];
    char message_receive[maxsize];

public:
    Message()
    {
        memset((void *)message_send, '\0', sizeof(char) * maxsize);
        memset((void *)message_receive, '\0', sizeof(char) * maxsize);
    }
    ~Message() = default;

private:
    void Reset(char *message)
    {
        memset((void *)message, '\0', sizeof(char) * maxsize);
    }

public:
    // void Send(int &to_socket, const std::string &message)
    // {
    //     if (write(to_socket, message.c_str(), message.size()) == -1)
    //         Log_Error("Send Failed");
    //     Log("Message Sent:\t" + std::to_string(message.size()) + "B " + message);
    // }

    // int Receive(int &from_socket, const std::string &message)
    // {
    //     int count = read(from_socket, (void *)message.c_str(), message.capacity());
    //     if (count == -1)
    //         Log_Error("Receive Failed");
    //     Log("Message Received:\t" + std::to_string(message.size()) + "B " + message);
    //     return count;
    // }
    void Send(int &to_socket)
    {
        if (write(to_socket, message_send, strlen(message_send) + 1) == -1)
            Log_Error("Send Failed");
        std::cout << "[ Message Sent: " << message_send << " ]" << std::endl;
        Reset(message_send);
    }

    int Receive(int &from_socket)
    {
        Reset(message_receive);
        int count = read(from_socket, (void *)message_receive, maxsize);
        if (count == -1)
            Log_Error("Receive Failed");
        std::cout << "[ Message Received: " << message_receive << " ]" << std::endl;
        return count;
    }
    void Set(const char *message)
    {
        if (strlen(message) > maxsize)
            Log_Error("message Full");
        memcpy(this->message_send, message, strlen(message));
    }
    void Set(std::string &message)
    {
        if (message.size() > maxsize)
            Log_Error("message Full");
        std::string s(begin(message), end(message));
        strcpy(message_send, s.c_str());
    }
};
