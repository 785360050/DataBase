/*
Navicat MySQL Data Transfer

Source Server         : 测试1
Source Server Version : 50616
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50616
File Encoding         : 65001

Date: 2014-05-11 00:37:03
*/

SET FOREIGN_KEY_CHECKS=0;
set names utf8;

-- ----------------------------
-- Table structure for `student`
-- ----------------------------
DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
  ID char(12) NOT NULL DEFAULT '',
  Name char(20) DEFAULT NULL,
  Department char(20) DEFAULT NULL,
  Sex char(2) DEFAULT NULL,
  Age smallint(6) DEFAULT NULL,
  Count_Class smallint(6) DEFAULT 0,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of stu
-- ----------------------------

INSERT INTO `Student` VALUES ('1', 'A','CS', 'M', '22', '4');
INSERT INTO `Student` VALUES ('2', 'B','SP', 'M', '20', '2');
INSERT INTO `Student` VALUES ('3', 'C','CS', 'F', '21', '4');
INSERT INTO `Student` VALUES ('4', 'D','SP', 'M', '21', '0');
INSERT INTO `Student` VALUES ('5', 'E','CS', 'F', '22', '1');
INSERT INTO `Student` VALUES ('6', 'F','MT', 'M', '19', '3');
INSERT INTO `Student` VALUES ('7', 'G','MT', 'F', '25', '4');
