#include <iostream>

#include <mysql/mysql.h>

#include "Source/Log.hpp"
#include "Source/MySQL.hpp"
#include "Source/SQL.hpp"
// #include "Source/Tables/Table_Student.hpp"
// #include "Source/Tables/Table_Math.hpp"

#include <vector>
#include <string>

// void Database_Test()
// {
//     using namespace Database;

//     Log("初始化");
//     MySQL mysql; // 初始化连接
//     // SQL sql;     // 负责执行sql语句

//     /// 修改学生信息
//     // 初始化基表对象
//     Table_Student student(&mysql); // 使用mysql这个连接

//     CR();
//     Log("更新Student表中，ID为7的学生 Count_Class列的值为");
//     student.Updata("7", Table_Student::Column::Count_Class, "20");
//     // student.Updata("7 or 1=1", Table_Student::Column::Count_Class, "20"); // SQL注入测试
//     student.Table_Show("Student");

//     CR();
//     Log("更新Student表中，ID为7的学生 Department列的值为");
//     student.Updata("7", Table_Student::Column::Department, "\"CS\""); // 非整数要转义。防止拼接后""丢失
//     student.Table_Show("Student");

//     // 增加、删除学生的选课记录
//     Table_Math math(&mysql);

//     CR();
//     Log("插入Math表 ID为7号的学生相关的信息(查找Student表，接受结果后插入Math表)");
//     math.Insert(student, "7");
//     math.Table_Show("Math");

//     CR();
//     Log("删除Math表 ID为7号的学生记录");
//     math.Delete(student, "7");
//     math.Table_Show("Math");

//     // search专业为'SP'的学生信息
//     CR();
//     Log("执行多表查询语句");
//     auto res = SQL::Instance().Query_Execute(mysql.MYSQL_Get(),
//                                  //  {"select * from Math where id in(select id from Student where department = 'SP');"});
//                                  {"select * from Student,Math where Math.id = Student.id;"});
//     // sql.Result_Show(mysql.MYSQL_Get(), res);
//     auto record = mysql_fetch_row(res);
//     std::string Department = std::string(record[Table_Student::Column::Department]);
//     Log("Result: " + Department);
//     mysql_free_result(res);
// }

void Database_Info()
{
    MySQL mysql;

    mysql::Host localhost("127.0.0.1", "root", "187065", 3306);
    mysql.Connect(localhost, "Log");

    auto res = SQL::Instance().Query_Execute(mysql.MYSQL_Get(),
                                             "SELECT column_name "
                                             "FROM information_schema.columns "
                                             "WHERE table_schema = 'Log' AND table_name = 'Log_STD';");

    std::vector<std::string> record;
    MYSQL_ROW row;
    while ((row = mysql_fetch_row(res)))
    {
        std::cout << row[0] << ' ';
        record.push_back(row[0]);
    }
    std::cout << std::endl;
    for (const auto &rec : record)
    {
        std::cout << rec << ' ';
    }
    std::cout << std::endl;

    // auto record = mysql_fetch_row(res);
    // while(auto column = mysql_fetch_field(res))
    // {
    //     std::cout << column << ' ';
    // }

    mysql_free_result(res);
}

int main()
{
    // Database_Test();
    Database_Info();
}