#pragma once

#include <arpa/inet.h>
#include <stdlib.h> //atoi

class Address
{
public:
    using Address_Family = decltype(sockaddr_in::sin_family);
    using Address_Internet = decltype(decltype(sockaddr_in::sin_addr)::s_addr);
    using Port = decltype(sockaddr_in::sin_port);

public:
    // const Address_Family address_family;
    // const Address_Internet address;
    // const Port port;
    sockaddr_in address;

public:
    // Address(Address_Family address_family=AF_INET, Address_Internet address=htonl(INADDR_ANY), Port port=htons(atoi("9200"))
    //     : address_family{address_family}, address{address}, port{port} {};
    Address() = default;
    // Client Address
    Address(Address_Family AF, const char *ip, const char *port)
    {
        address.sin_family = AF;                 /// IPV4
        address.sin_addr.s_addr = inet_addr(ip); /// IP地址
        address.sin_port = htons(atoi(port));    /// 端口号
    }
    // Server Address
    Address(Address_Family AF, const char *port)
    {
        address.sin_family = AF;                     /// IPV4
        address.sin_addr.s_addr = htonl(INADDR_ANY); /// IP地址 (任意)
        address.sin_port = htons(atoi(port));        /// 端口号
    }
    ~Address() = default;

    // public:
    //     socklen_t *Length() const// { return &((socklen_t)sizeof(sockaddr_in)); }
    //     {
    //         socklen_t* len = sizeof(sockaddr_in);
    //         return &len;
    //     }
};
