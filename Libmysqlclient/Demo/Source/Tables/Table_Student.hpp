#pragma once
#include <string>

#include "Table.hpp"

using std::string;

class Table_Student : public Table
{
    const string table{"Student"};

public:
    enum Column
    {
        ID = 0,
        Name,
        Department,
        Sex,
        Age,
        Count_Class
    };

public:
    Table_Student(MySQL *mysql) : Table(mysql){};
    ~Table_Student() = default;

private:
    // 列名转字符串
    std::string Column_Get(Column column)
    {
        switch (column)
        {
        case ID:
            return "ID";
        case Name:
            return "Name";
        case Department:
            return "Department";
        case Sex:
            return "Sex";
        case Age:
            return "Age";
        case Count_Class:
            return "Count_Class";

        default:
            throw std::logic_error("Illigal Column");
        }
    }

public:
    // 更新ID=id的学生column列的数据为value
    void Updata(const string &id, Column column, const string &value)
    { // 更新ID=id的学生column列的数据为value

        using namespace Database;
        Log("Updating Student");
        std::string clm = Column_Get(column);
        // string sql{"update Student set " + clm + " = " + value + " where id = " + id + ";"};
        if (!sql->Parameter_Check(id) || !sql->Parameter_Check(value))
        {
            Log("Update Failed");
            return;
        }
        // int failed = mysql_query(mysql, sql.c_str());
        // if (failed) // 现在就代表执行失败了
        //     Log_Error("Update Failed");
        auto res = this->sql->Query_Execute(this->mysql,
                                            {"update Student set " + clm + " = " + value + " where id = " + id + ";"});
        Log("Update Succeed");
    }

public:
    // 返回结果同mysql_store_result
    MYSQL_RES *Student_Get(const std::string &id) const
    {
        return sql->Query_Execute(mysql, {"select * from Student where id = " + id});
    }
};

// SQL注入：id接收为"7 or 1=1"
// 正常执行
// update Student set clm = [value] where id = [7] ;
// 实际执行
// update Student set clm = [value] where id = [7 or 1=1] ;
// 等价于执行 update Student set clm = [value]; 把所有记录都改了
