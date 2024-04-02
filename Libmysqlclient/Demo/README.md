

# Mysql++(Mysqlpp)

开源的mysql C_API封装好的框架

> https://blog.csdn.net/liangwenhao1108/article/details/112300204


SQL注入案例

string query = "SELECT * FROM items " +
                "WHERE owner = '"+ userName + 
                "' AND itemname = '" + ItemName+ "'";
sql.Query_Execute(query);

userName和ItemName运行时生成

若
userName接收到"wiley"
ItemName接收到"name' OR'a'='a"

则执行为：
SELECT * FROM items
WHERE owner = 'wiley'
AND itemname = 'name' OR 'a'='a';

等价于
select * from items;



SVN教程
https://zhuanlan.zhihu.com/p/144220746



