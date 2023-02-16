ALTER USER JEVON DEFAULT TABLESPACE PRODUCTION_MANAGEMENT;

SELECT TABLESPACE_NAME FROM TABS WHERE TABLE_NAME='CUSTOMER';


CREATE USER JEVON IDENTIFIED BY JEVON;
Grant ALL PRIVILEGES
to JEVON;

/*==============================================================*/
/* DBMS name:      ORACLE Version 11g                           */
/* Created on:     2022-10-24 17:21:25                          */
/*==============================================================*/


alter table Delivery
   drop constraint FK_DELIVERY_REFERENCE_PRODUCT;

alter table Delivery
   drop constraint FK_DELIVERY_REFERENCE_ORD;

alter table EMP
   drop constraint FK_EMP_REFERENCE_DEPART;

alter table Invoice
   drop constraint FK_INVOICE_REFERENCE_PRODUCT;

alter table Invoice
   drop constraint FK_INVOICE_REFERENCE_ORD;

alter table Ord
   drop constraint FK_ORD_REFERENCE_PRODUCT;

alter table Ord
   drop constraint FK_ORD_REFERENCE_CUSTOMER;

alter table ProBuy
   drop constraint FK_PROBUY_REFERENCE_STOCK;

alter table ProBuy
   drop constraint FK_PROBUY_REFERENCE_PRODUCT;

alter table Stock
   drop constraint FK_STOCK_REFERENCE_PRODUCT;

alter table WIP
   drop constraint FK_WIP_REFERENCE_PRODUCT;

drop table Customer cascade constraints;

drop table Delivery cascade constraints;

drop table Depart cascade constraints;

drop table EMP cascade constraints;

drop table Invoice cascade constraints;

drop table Ord cascade constraints;

drop table ProBuy cascade constraints;

drop table Product cascade constraints;

drop table Stock cascade constraints;

drop table WIP cascade constraints;

/*==============================================================*/
/* Table: Customer                                              */
/*==============================================================*/
create table Customer 
(
   CustID               VARCHAR2(10)         not null,
   CustName             VARCHAR2(22),
   CustAdd              VARCHAR2(20),
   CustPhone            VARCHAR2(12),
   CustFax              VARCHAR2(12),
   constraint PK_CUSTOMER primary key (CustID)
);

/*==============================================================*/
/* Table: Delivery                                              */
/*==============================================================*/
create table Delivery 
(
   ProID                VARCHAR2(20),
   OrdID                VARCHAR2(10),
   CarNO                VARCHAR2(10)
);

/*==============================================================*/
/* Table: Depart                                                */
/*==============================================================*/
create table Depart 
(
   DeptNo               NUMBER(2)            not null,
   DeptName             VARCHAR2(20),
   -- Pro                  VARCHAR2(20),
   -- Sal                  NUMBER(20),
   -- Educa                VARCHAR2(20),
   -- Exper                VARCHAR2(20),
   LOC                  VARCHAR2(20),
   constraint PK_DEPART primary key (DeptNo)
);

/*==============================================================*/
/* Table: EMP                                                   */
/*==============================================================*/
create table EMP 
(
   EmpId                VARCHAR2(10)         not null,
   EmpName              VARCHAR2(10),
   EmpAdd               VARCHAR2(20),
   EmpPhone             VARCHAR2(12),
   Email                VARCHAR2(20),
   MGR                  VARCHAR2(6),
   HireDate             DATE,
   COMM                 NUMBER(7,2),
   DeptNo               NUMBER(2),
   Pro                  VARCHAR2(10),
   Sal                  NUMBER(10),
   Educa                VARCHAR2(10),
   Exper                VARCHAR2(10),
   constraint PK_EMP primary key (EmpId)
);

/*==============================================================*/
/* Table: Invoice                                               */
/*==============================================================*/
create table Invoice 
(
   OrdID                VARCHAR2(10),
   ProID                VARCHAR2(10),
   InvID                VARCHAR2(10),
   Money                NUMBER(10)
);

/*==============================================================*/
/* Table: Ord                                                   */
/*==============================================================*/
create table Ord 
(
   OrdID                VARCHAR2(10)         not null,
   CustID               VARCHAR2(10),
   ProID                VARCHAR2(20),
   Qty                  VARCHAR2(20),
   OrdDate              DATE,
   D_Date               DATE,
   constraint PK_ORD primary key (OrdID)
);

/*==============================================================*/
/* Table: ProBuy                                                */
/*==============================================================*/
create table ProBuy 
(
   ProID                VARCHAR2(10),
   StiQty               VARCHAR2(10),
   InsQty               NUMBER(10)
);

/*==============================================================*/
/* Table: Product                                               */
/*==============================================================*/
create table Product 
(
   ProID                VARCHAR2(10)         not null,
   ProName              VARCHAR2(20),
   constraint PK_PRODUCT primary key (ProID)
);

/*==============================================================*/
/* Table: Stock                                                 */
/*==============================================================*/
create table Stock 
(
   ProID                VARCHAR2(10),
   StiQty               VARCHAR2(10)         not null,
   constraint PK_STOCK primary key (StiQty)
);
 
/*==============================================================*/
/* Table: WIP  工令表记录当前正在进行生产的计划信息                  */
/*==============================================================*/
create table WIP 
(
   ProID                VARCHAR2(20),
   WIPID                VARCHAR2(10),
   Qty                  VARCHAR2(10)
);

alter table Delivery
   add constraint FK_DELIVERY_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);

alter table Delivery
   add constraint FK_DELIVERY_REFERENCE_ORD foreign key (OrdID)
      references Ord (OrdID);

alter table EMP
   add constraint FK_EMP_REFERENCE_DEPART foreign key (DeptNo)
      references Depart (DeptNo);

alter table Invoice
   add constraint FK_INVOICE_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);

alter table Invoice
   add constraint FK_INVOICE_REFERENCE_ORD foreign key (OrdID)
      references Ord (OrdID);

alter table Ord
   add constraint FK_ORD_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);

alter table Ord
   add constraint FK_ORD_REFERENCE_CUSTOMER foreign key (CustID)
      references Customer (CustID);

alter table ProBuy
   add constraint FK_PROBUY_REFERENCE_STOCK foreign key (StiQty)
      references Stock (StiQty);

alter table ProBuy
   add constraint FK_PROBUY_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);

alter table Stock
   add constraint FK_STOCK_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);

alter table WIP
   add constraint FK_WIP_REFERENCE_PRODUCT foreign key (ProID)
      references Product (ProID);




/*==============================================================*/
/* 用户创建                                               */
/*==============================================================*/

CREATE USER Abel IDENTIFIED BY Abel;
GRANT CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
TO Abel;

create user Alan identifIed by Alan;
Grant create session , create view, CREATE SEQUENCE,CREATE PROCEDURE 
to Alan;

create user Bard identified by Bard;
Grant create session , create view, CREATE SEQUENCE,CREATE PROCEDURE 
to Bard;

create user Bart identified by Bart;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Bart;

create user Beau identified by Beau;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Beau;

create user Carl identified by Carl;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Carl;

create user Ed identified by Ed;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Ed;

create user Dan identified by Dan;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Dan;

create user Des identified by Des;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Des;

create user Ford identified by Ford;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Ford;

create user CASH identified by CASH;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to CASH;

create user Ian identified by Ian;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Ian;

Create user Ira identified by Ira;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Ira;

create user Jack identified by Jack;
Grant CREATE SESSION , CREATE VIEW, CREATE SEQUENCE,CREATE PROCEDURE 
to Jack;


DROP USER JEVON;
--read
DROP USER Abel;
DROP USER Alan;
DROP USER Bard;
DROP USER Cash;
DROP USER Ian;
DROP USER Ira;
DROP USER Jack;
--write
DROP USER Bart;
DROP USER Beau;
DROP USER Carl;
DROP USER Dan;
DROP USER Des;
DROP USER Ford;

--origion
DROP USER Ivan;--
DROP USER Henry;--
DROP USER Harry;--
DROP USER Eden;--
DROP USER Ed;--
DROP USER Cliff;--
DROP USER Frank;--
DROP USER Hermes;--
DROP USER Gale;--
DROP USER Beck;--
DROP USER Gary;--
DROP USER Danny;--
DROP USER Eddy ;--
DROP USER Barton; --
DROP USER Hank;--
DROP USER Abner;--
DROP USER Ade;--


--EMP
GRANT SELECT,INDEX,REFERENCES ON EMP
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON EMP
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON EMP
TO Bard WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON EMP
TO Bart WITH GRANT OPTION;

--DEPART
GRANT SELECT,INDEX,REFERENCES ON DEPART
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DEPART
TO Bard WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON DEPART
TO Bart WITH GRANT OPTION;

--PRODUCT
GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Carl WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON PRODUCT
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PRODUCT
TO Jack WITH GRANT OPTION;

--CUSTOMER

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Bart WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Beau WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Carl WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON CUSTOMER
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Ford WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON CUSTOMER
TO Jack WITH GRANT OPTION;

--ORD

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Carl WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON ORD
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON ORD
TO Jack WITH GRANT OPTION;

--WIP
GRANT SELECT,INDEX,REFERENCES ON WIP
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Carl WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Dan WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON WIP
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Ford WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON WIP
TO Jack WITH GRANT OPTION;

--STOCK

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Beau WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Carl WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Dan WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON STOCK
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Ford WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON STOCK
TO Jack WITH GRANT OPTION;

--PROBUY
GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Beau WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Carl WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON PROBUY
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON PROBUY
TO Jack WITH GRANT OPTION;

--INVOICE
GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Beau WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON INVOICE
TO Carl WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON INVOICE
TO Ian WITH GRANT OPTION;

--DELIVERY
GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Abel WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Alan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Bard WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Beau WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Carl WITH GRANT OPTION;

GRANT SELECT,INSERT,UPDATE,ALTER,DELETE,INDEX,REFERENCES ON DELIVERY
TO Dan WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Des WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Ford WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Cash WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Ian WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Ira WITH GRANT OPTION;

GRANT SELECT,INDEX,REFERENCES ON DELIVERY
TO Jack WITH GRANT OPTION;




insert into Depart(DeptNo,DeptName,LOC) values ('11','总经理室','北京');
insert into Depart(DeptNo,DeptName,LOC) values ('12','监督室','北京');
insert into Depart(DeptNo,DeptName,LOC) values ('21','管理部','郑州');
insert into Depart(DeptNo,DeptName,LOC) values ('31','会计科','北京');
insert into Depart(DeptNo,DeptName,LOC) values ('22','业务部','北京');
insert into Depart(DeptNo,DeptName,LOC) values ('32','生管科','郑州');
insert into Depart(DeptNo,DeptName,LOC) values ('33','品保科','郑州');
insert into Depart(DeptNo,DeptName,LOC) values ('23','制造部','郑州');
insert into Depart(DeptNo,DeptName,LOC) values ('34','压合科','郑州');
insert into Depart(DeptNo,DeptName,LOC) values ('35','内务科','郑州');
SELECT * FROM DEPART;

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper) 
values ('00101','Abel','北京市海淀区','(010)-111111','xxx@yahoo.com',null,to_date('06/05/90','dd/mm/yy'),null,'11','总经理','180000','研究所','五年');
                                
Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00102','Ivan','上海市四川路','(021)-111111','xxx@yahoo.com','Abel',to_date('13/01/92','dd/mm/yy'),'200','11','特助','120000','研究所','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00201','Alan','郑州市人民路','(037)-111111','xxx@yahoo.com','Abel',to_date('23/06/91','dd/mm/yy'),null,'12','经理','120000','研究所','三年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00202','Henry','郑州市中山路','(037)-111112','xxx@yahoo.com','Alan',to_date('05/02/92','dd/mm/yy'),'600','12','监督员','40000','大学','三年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00301','Bard','上海市南京路','(021)-11112','xxx@yahoo.com','Abel',to_date('26/03/91','dd/mm/yy'),null,'21','经理','70000','大学','三年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00302','Harry','南京市六合区','(021)-111112','xxx@yahoo.com','Bard',to_date('15/06/91','dd/mm/yy'),null,'21','科长','50000','大学','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00303','Bart','广州市人民路','(020)-111111','xxx@yahoo.com','Harry',to_date('15/12/91','dd/mm/yy'),'400','21','人事','30000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00304','Eden','广州市中山路','(020)-111112','xxx@yahoo.com','Harry',to_date('08/01/92','dd/mm/yy'),'500','21','总务','30000','大学','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00305','Beau','北京市海淀区','(010)-111111','xxx@yahoo.com','Harry',to_date('16/01/92','dd/mm/yy'),'300','21','采购','30000','大学','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00401','Carl','郑州市中山路','(037)-111112','xxx@yahoo.com','Bard',to_date('18/04/91','dd/mm/yy'),null,'31','经理','70000','大学','四年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00402','Ed','石家庄市人民路','(031)-11111','xxx@yahoo.com','Carl',to_date('28/09/91','dd/mm/yy'),'500','31','成会','40000','大学','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00403','Cliff','上海市南京路','(021)-11112','xxx@yahoo.com','Carl',to_date('17/10/91','dd/mm/yy'),'300','31','普会','35000','大学','一年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00501','Dan','广州市人民路','(020)-111111','xxx@yahoo.com','Abel',to_date('24/07/91','dd/mm/yy'),null,'22','经理','80000','大学','三年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00502','Frank','广州市中山路','(020)-111112','xxx@yahoo.com','Dan',to_date('21/03/92','dd/mm/yy'),'1000','22','业助','33000','专科','一年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00601','Hermes','上海市四川路','(021)-111111','xxx@yahoo.com','Abel',to_date('29/04/92','dd/mm/yy'),null,'32','科长','40000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00602','Des','北京市中山区','(010)-111112','xxx@yahoo.com','Hermes',to_date('19/06/92','dd/mm/yy'),'600','32','生管','31000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00603','Gale','郑州市中山路','(037)-111112','xxx@yahoo.com','Hermes',to_date('02/12/93','dd/mm/yy'),'700','32','生管','40000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00604','Beck','石家庄市人民路','(031)-11111','xxx@yahoo.com','Hermes',to_date('25/03/93','dd/mm/yy'),'500','32','助理','25000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00605','Gary','上海市四川路','(021)-111111','xxx@yahoo.com','Hermes',to_date('03/09/94','dd/mm/yy'),'800','32','仓管','25000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00606','Danny','北京市海淀区','(010)-111111','xxx@yahoo.com','Hermes',to_date('18/05/93','dd/mm/yy'),'400','32','外务','30000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00607','Ford','上海市四川路','(021)-111111','xxx@yahoo.com','Hermes',to_date('23/02/94','dd/mm/yy'),'600','32','外务','25000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00701','CASH','石家庄市人民路','(031)-11111','xxx@yahoo.com','Abel',to_date('15/11/93','dd/mm/yy'),null,'33','科长','40000','专科','四年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00702','Eddy','上海市南京路','(021)-11112','xxx@yahoo.com','CASH',to_date('09/07/94','dd/mm/yy'),'300','33','QA','25000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00703','Barton','南京市六合区','(021)-111112','xxx@yahoo.com','CASH',to_date('02/06/95','dd/mm/yy'),'700','33','QC','23000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00801','Ian','北京市海淀区','(010)-111111','xxx@yahoo.com','Abel',to_date('10/12/92','dd/mm/yy'),null,'23','副理','60000','专科','五年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00802','Hank','上海市南京路','(021)-11112','xxx@yahoo.com','Ian',to_date('06/03/95','dd/mm/yy'),'1000','23','工务','32000','专科','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00803','Ira','上海市四川路','(021)-111111','xxx@yahoo.com','Ian',to_date('26/08/94','dd/mm/yy'),null,'34','科长','38000','高中','八年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00804','Abner','郑州市人民路','(037)-111111','xxx@yahoo.com','Ira',to_date('10/09/95','dd/mm/yy'),'900','34','领班','33000','高中','二年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00805','Jack','郑州市中山路','(037)-111112','xxx@yahoo.com','Ian',to_date('16/10/93','dd/mm/yy'),null,'35','科长','39000','专科','六年');

Insert INTO EMP (EmpID,EmpName,EmpAdd,EmpPhone,EMail,MGR,HireDate,COMM,DeptNo,Pro,Sal,Educa,Exper)
values ('00806','Ade','石家庄市人民路','(031)-11111','xxx@yahoo.com','Jack',to_date('19/02/95','dd/mm/yy'),'800','35','领班','32000','高中','二年');
SELECT * FROM EMP;

insert into product values ('P001','主板');
insert into product values ('P002','处理器');
insert into product values ('P003','内存');
insert into product values ('P004','硬盘');
insert into product values ('P005','显卡');
SELECT * FROM PRODUCT;


insert into customer values('C001','南亚电子股份有限公司','北京市海淀区','(010)-111111','(010)-111112');
insert into customer values('C002','华通电子股份有限公司','上海市四川路','(021)-111111','(021)-111112');
insert into customer values('C003','欣兴电子股份有限公司','北京市中山区','(010)-111112','(010)-111113');
insert into customer values('C004','群策电子股份有限公司','郑州市人民路','(037)-111111','(037)-111112');
insert into customer values('C005','联致电子股份有限公司','郑州市中山路','(037)-111112','(037)-111113');
insert into customer values('C006','旭德电子股份有限公司','石家庄市人民路','(031)-111111','(031)-111112');
insert into customer values('C007','联能电子股份有限公司','上海市南京路','(021)-111112','(021)-111113');
insert into customer values('C008','铭望电子股份有限公司','南京市六合区','(022)-111112','(022)-111113');
insert into customer values('C009','柏拉图电子股份有限公司','广州市人民路','(020)-111111','(020)-111112');
insert into customer values('C010','定颖电子股份有限公司','广州市中山路','(020)-111112','(020)-111113');
insert into customer values('C011','南华电子股份有限公司','北京市海淀区','(010)-111111','(010)-111112');
insert into customer values('C012','华欣电子股份有限公司','上海市四川路','(021)-111112','(021)-111112');
Insert INTO Customer values ('C013','欣群电子股份有限公司','北京市中山区','(010)-111112','(010)-111113');
Insert INTO Customer values ('C014','群联电子股份有限公司','郑州市人民路','(037)-111111','(037)-111112');
Insert INTO Customer values ('C015','联旭电子股份有限公司','郑州市中山路','(037)-111112','(037)-111113');
Insert INTO Customer values ('C016','旭联电子股份有限公司','石家庄市人民路','(031)-11111','(021)-11112');
Insert INTO Customer values ('C017','联铭电子股份有限公司','上海市南京路','(021)-11112','(021)-11113');
Insert INTO Customer values ('C018','铭图电子股份有限公司','南京市六合区','(021)-111112','(021)-111113');
Insert INTO Customer values ('C019','柏图电子股份有限公司','广州市人民路','(020)-111111','(020)-111112');
Insert INTO Customer values ('C020','南颖电子股份有限公司','广州市中山路','(020)-111112','(020)-111113');
Insert INTO Customer values ('C021','旭联电子股份有限公司','石家庄市人民路','(031)-11111','(021)-11112');
Insert INTO Customer values ('C022','联铭电子股份有限公司','上海市南京路','(021)-11112','(021)-11113');
Insert INTO Customer values ('C023','铭图电子股份有限公司','南京市六合区','(021)-111112','(021)-111113');
Insert INTO Customer values ('C024','柏图电子股份有限公司','广州市人民路','(020)-111111','(020)-111112');
Insert INTO Customer values ('C025','南颖电子股份有限公司','广州市中山路','(020)-111112','(020)-111113');
SELECT * FROM CUSTOMER;

insert into STOCK (ProID,StiQty) values('P001','0');
insert into STOCK (ProID,StiQty) values('P002','10');
insert into STOCK (ProID,StiQty) values('P003','20');
insert into STOCK (ProID,StiQty) values('P004','30');
insert into STOCK (ProID,StiQty) values('P005','40');
select * from stock;

Insert into ProBuy(ProID,StiQty,InsQty) values('P001','0','20');
Insert into ProBuy(ProID,StiQty,InsQty) values('P002','10','0');
Insert into ProBuy(ProID,StiQty,InsQty) values('P003','20','0');
Insert into ProBuy(ProID,StiQty,InsQty) values('P004','30','0');
Insert into ProBuy(ProID,StiQty,InsQty) values('P005','40','0');
SELECT * FROM PROBUY;


insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR01','P001','C001','30',to_date('10/02/92','dd/mm/yy'),to_date('20/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR02','P001','C002','60',to_date('15/02/92','dd/mm/yy'),to_date('25/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR03','P001','C003','50',to_date('02/03/92','dd/mm/yy'),to_date('16/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR04','P001','C004','80',to_date('15/03/92','dd/mm/yy'),to_date('23/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR05','P001','C005','100',to_date('03/04/92','dd/mm/yy'),to_date('18/04/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR06','P002','C006','150',to_date('08/04/92','dd/mm/yy'),to_date('26/04/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR07','P002','C007','30',to_date('16/05/92','dd/mm/yy'),to_date('28/05/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR08','P002','C008','15',to_date('06/05/92','dd/mm/yy'),to_date('25/05/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR09','P002','C009','200',to_date('11/06/92','dd/mm/yy'),to_date('22/06/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR10','P002','C010','300',to_date('18/06/92','dd/mm/yy'),to_date('30/06/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR11','P003','C011','30',to_date('10/02/92','dd/mm/yy'),to_date('20/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR12','P003','C012','60',to_date('15/02/92','dd/mm/yy'),to_date('25/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR13','P003','C013','50',to_date('02/03/92','dd/mm/yy'),to_date('16/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR14','P003','C014','80',to_date('15/03/92','dd/mm/yy'),to_date('23/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR15','P003','C015','100',to_date('03/04/92','dd/mm/yy'),to_date('18/04/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR16','P004','C016','150',to_date('08/04/92','dd/mm/yy'),to_date('26/04/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR17','P004','C017','30',to_date('16/05/92','dd/mm/yy'),to_date('28/05/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR18','P004','C018','15',to_date('06/05/92','dd/mm/yy'),to_date('25/05/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR19','P004','C019','200',to_date('11/06/92','dd/mm/yy'),to_date('22/06/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR20','P004','C020','300',to_date('18/06/92','dd/mm/yy'),to_date('30/06/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR21','P005','C021','30',to_date('10/02/92','dd/mm/yy'),to_date('20/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR22','P005','C022','60',to_date('15/02/92','dd/mm/yy'),to_date('25/02/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR23','P005','C023','50',to_date('02/03/92','dd/mm/yy'),to_date('16/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR24','P005','C024','80',to_date('15/03/92','dd/mm/yy'),to_date('23/03/92','dd/mm/yy'));
insert into Ord (OrdID,ProID,CustID,Qty,OrdDate,D_Date) values('CR25','P005','C025','100',to_date('03/04/92','dd/mm/yy'),to_date('18/04/92','dd/mm/yy'));
SELECT * FROM ORD;


insert into Delivery values('P001','CR01','A1-1111');
insert into Delivery values('P001','CR02','A1-1111');
insert into Delivery values('P001','CR03','A1-1111');
insert into Delivery values('P001','CR04','A1-1111');
insert into Delivery values('P001','CR05','A1-1111');
insert into Delivery values('P002','CR06','A1-1111');
insert into Delivery values('P002','CR07','A1-1112');
insert into Delivery values('P002','CR08','A1-1112');
insert into Delivery values('P002','CR09','A1-1112');
insert into Delivery values('P002','CR10','A1-1112');
insert into Delivery values('P003','CR11','A1-1112');
insert into Delivery values('P003','CR12','A1-1112');
insert into Delivery values('P003','CR13','A1-1112');
insert into Delivery values('P003','CR14','A1-1112');
insert into Delivery values('P003','CR15','A1-1113');
insert into Delivery values('P004','CR16','A1-1113');
insert into Delivery values('P004','CR17','A1-1113');
insert into Delivery values('P004','CR18','A1-1113');
insert into Delivery values('P004','CR19','A1-1113');
insert into Delivery values('P004','CR20','A1-1113');
insert into Delivery values('P005','CR21','A1-1113');
insert into Delivery values('P005','CR22','A1-1113');
insert into Delivery values('P005','CR23','A1-1113');
insert into Delivery values('P005','CR24','A1-1113');
insert into Delivery values('P005','CR25','A1-1113');
SELECT * FROM DELIVERY;


insert into Invoice(OrdID,InvID,ProID,Money) values('CR01','I001','P001','35000');
insert into Invoice(OrdID,InvID,ProID,Money) values('CR02','I002','P002','50000');
insert into Invoice(OrdID,InvID,ProID,Money) values('CR03','I003','P003','65000');
insert into Invoice(OrdID,InvID,ProID,Money) values('CR04','I004','P004','15000');
insert into Invoice(OrdID,InvID,ProID,Money) values('CR05','I005','P005','40000');
SELECT * FROM INVOICE;

insert into WIP(WIPID,ProID,Qty)values('W001','P001','3');
insert into WIP(WIPID,ProID,Qty)values('W002','P001','6');
insert into WIP(WIPID,ProID,Qty)values('W003','P001','5');
insert into WIP(WIPID,ProID,Qty)values('W004','P001','8');
insert into WIP(WIPID,ProID,Qty)values('W005','P001','10');
insert into WIP(WIPID,ProID,Qty)values('W006','P002','15');
insert into WIP(WIPID,ProID,Qty)values('W007','P002','3');
insert into WIP(WIPID,ProID,Qty)values('W008','P002','1');
insert into WIP(WIPID,ProID,Qty)values('W009','P002','20');
insert into WIP(WIPID,ProID,Qty)values('W010','P002','30');
insert into WIP(WIPID,ProID,Qty)values('W011','P003','3');
insert into WIP(WIPID,ProID,Qty)values('W012','P003','6');
insert into WIP(WIPID,ProID,Qty)values('W013','P003','5');
insert into WIP(WIPID,ProID,Qty)values('W014','P003','8');
insert into WIP(WIPID,ProID,Qty)values('W015','P003','10');
insert into WIP(WIPID,ProID,Qty)values('W016','P004','15');
insert into WIP(WIPID,ProID,Qty)values('W017','P004','3');
insert into WIP(WIPID,ProID,Qty)values('W018','P004','1');
insert into WIP(WIPID,ProID,Qty)values('W019','P004','20');
insert into WIP(WIPID,ProID,Qty)values('W020','P004','30');
insert into WIP(WIPID,ProID,Qty)values('W021','P005','3');
insert into WIP(WIPID,ProID,Qty)values('W022','P005','6');
insert into WIP(WIPID,ProID,Qty)values('W023','P005','5');
insert into WIP(WIPID,ProID,Qty)values('W024','P005','8');
insert into WIP(WIPID,ProID,Qty)values('W025','P005','10');
SELECT * FROM WIP;






