#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#include <cstring>

#include <iostream>
#include <string>

#include "Facilities/Message.hpp"
#include "Facilities/Log.hpp"
#include "Facilities/Socket.hpp"

int main(int argc, char **argv)
{
    using namespace std;
    if (argc != 3)
        Log_Error("Usage: [IP] [Port]");

    int socket_server = socket(PF_INET, SOCK_STREAM, 0);

    Address address_server(AF_INET, argv[1], argv[2]);

    if (connect(socket_server, (sockaddr *)&address_server, sizeof(address_server)))
        Log_Error("Connect Error");

    
    while (1)
    {
        Log("Input message(Q to quit): ");
        std::string message;
        std::cin >> message;

        if(message=="q"||message=="Q")
            break;
        Log("input:"+message);
        
        Message msg;
        msg.Set(message);
        msg.Send(socket_server);
        // int str_len = message.size();
        // int recv_len = 0;

        // while (recv_len < str_len)
        // { /// 保证接受数据的完整性，且不受可能的分包影响
        //     int recv_cnt = msg.Receive(socket_server);
        //     recv_len += recv_cnt;
        // }
        msg.Receive(socket_server);
    }

    close(socket_server);
}
