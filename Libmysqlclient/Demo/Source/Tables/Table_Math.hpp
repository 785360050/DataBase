#pragma once

#include <string>

#include "../Tables/Table.hpp"

#include "Table_Student.hpp"

using std::string;

class Table_Math : public Table
{
    const string table{"Math"};

public:
    enum Column
    {
        ID,
        Name,
        Sex,
        Department
    };

public:
    Table_Math(MySQL *mysql) : Table(mysql){};
    ~Table_Math() = default;

private:
    std::string Column_Get(Column column)
    {
        switch (column)
        {
        case ID:
            return "ID";
        case Name:
            return "Name";
        case Sex:
            return "Sex";
        case Department:
            return "Department";

        default:
            throw std::logic_error("Illigal Column");
        }
    }

public:
    // 将id号学生添加到班级内
    void Insert(Table_Student &student, const std::string &id)
    {
        using namespace Database;

        // 需要根据学生ID查询Name，Sex,Department的信息
        MYSQL_RES *res = student.Student_Get("7");
        auto num_row = mysql_num_rows(res);
        if (num_row == 0)
            Log_Error(mysql, "No Such Student");
        if (num_row != 1)
            Log_Error(mysql, "Multiple Result Exist");

        // auto num_field = mysql_num_fields(res);
        auto record = mysql_fetch_row(res);
        std::string Name = '\'' + std::string(record[Table_Student::Column::Name]) + '\'';
        std::string Sex = '\'' + std::string(record[Table_Student::Column::Sex]) + '\'';
        std::string Department = '\'' + std::string(record[Table_Student::Column::Department]) + '\'';

        sql->Query_Execute(mysql,
                           {"INSERT INTO Math VALUES ('" + id + "\'," + Name + ',' + Sex + ',' + Department + ");"});
    }

    // 将id号学生从班级中删除
    void Table_Math::Delete(Table_Student &student, const std::string &id)
    { // 更新ID=id的学生column列的数据为value

        sql->Query_Execute(mysql,
                           {"DELETE FROM Math WHERE ID='" + id + "';"});
    }
    //
    // void Updata(const string &id, Column column, const string &value);
};