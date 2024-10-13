CREATE TABLE `z_gis` (
  `id` varchar(45) NOT NULL,
  `name` varchar(10) NOT NULL COMMENT '姓名',
  `gis` geometry NOT NULL COMMENT '经纬度位置信息', -- geometry 类型是空间数据类型，用于存储地理空间数据
  `geohash` varchar(20) GENERATED ALWAYS AS (st_geohash(`gis`,8)) VIRTUAL, -- 根据gis字段自动计算生成的虚拟列
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  SPATIAL KEY `idx_gis` (`gis`), -- 空间索引
  KEY `idx_geohash` (`geohash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='空间位置信息'


insert into z_gis(id,name,gis) 
values
    (replace(uuid(),'-',''),'张三',ST_GeomFromText('point(108.9498710632 34.2588125935)')),
    (replace(uuid(),'-',''),'李四',ST_GeomFromText('point(108.9465236664 34.2598766768)')),
    (replace(uuid(),'-',''),'王五',ST_GeomFromText('point(108.9477252960 34.2590342786)')),
    (replace(uuid(),'-',''),'赵六',ST_GeomFromText('point(108.9437770844 34.2553719653)')),
    (replace(uuid(),'-',''),'小七',ST_GeomFromText('point(108.9443349838 34.2595663206)')),
    (replace(uuid(),'-',''),'孙八',ST_GeomFromText('point(108.9473497868 34.2643456798)')),
    (replace(uuid(),'-',''),'十九',ST_GeomFromText('point(108.9530360699 34.2599476152)'));

-- 操作空间数据需要用相关函数实现字符串和geometry类型的互相转换
-- ST_GeomFromText，ST_AsText
select name, ST_AsText(gis) as gis from z_gis where name = '张三';

update z_gis 
set gis = ST_GeomFromText('point(108.9465236664 34.2598766768)') 
where name = '张三';


select gis from z_gis where name= '王五';
select gis from z_gis where name= '李四';
-- 查询王五和李四之间的距离
select floor(st_distance_sphere((select gis from z_gis where name= '王五'),gis)) as distance 
from z_gis where name= '李四';


-- 查询距离张三500米内的所有人
-- ST_Distance_Sphere(point1, point2) 计算两个点之间的距离
SELECT name,
    FLOOR(ST_DISTANCE_SPHERE((SELECT gis FROM z_gis WHERE name = '张三'),gis)) as distance,ST_AsText(gis) as point
FROM
    z_gis
WHERE
    ST_DISTANCE_SPHERE((SELECT gis FROM z_gis WHERE name = '张三'),gis) < 500
    AND name != '张三';
       
       
       
       

