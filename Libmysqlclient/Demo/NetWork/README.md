

#编译
## Server:
g++ Server.cpp -g -o Server


## Client
g++ Client.cpp -g -o Client

# 执行
./Server 9200
./Client 127.0.0.1 9200

