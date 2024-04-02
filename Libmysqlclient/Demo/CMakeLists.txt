
cmake_minimum_required (VERSION 3.0)


project(Database)
set(CMAKE_CXX_STANDARD 20)

# 查找目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
# aux_source_directory(./ root)


include_directories(/usr/include/mysql)

# 指定生成目标
add_executable(${PROJECT_NAME} main.cpp)

# 静态库链接
target_link_libraries(${PROJECT_NAME} mysqlclient)


set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_CXX_FLAGS_DEBUG "-std=c++20 -Wall -g -ggdb") 	#-Wall 用于显示警告





