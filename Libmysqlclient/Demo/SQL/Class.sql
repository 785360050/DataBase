drop table if exists Math;
CREATE TABLE Math (
  ID char(12) NOT NULL,
  Name char(10) DEFAULT NULL,
  Sex char(2) DEFAULT 'M' check('Sex' in('M','F')),
  Department char(20) DEFAULT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `Math` VALUES ('1', 'A', 'M', 'CS');
INSERT INTO `Math` VALUES ('2', 'B', 'M', 'SP');
INSERT INTO `Math` VALUES ('3', 'C', 'F', 'CS');
INSERT INTO `Math` VALUES ('5', 'E', 'F', 'CS');

-- INSERT INTO Math VALUES ('7', 'G', 'F', 'MT');

-- DELETE FROM Math WHERE ID='7';