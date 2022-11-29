创建mysql的sql

CREATE TABLE `api_auto_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` text,
  `assert` text,
  `uri` text,
  `method` text,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后一次修改时间',
  `describe` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

下面的是创建pg的表的sql
创建pg表
设置id自增长
CREATE SEQUENCE id_seq START 1;

创建表
CREATE TABLE "public"."api_auto_test" (
  "id" int8 NOT NULL DEFAULT nextval('id_seq'::regclass),
  "data" json,
  "assert" json,
  "uri" varchar(255) COLLATE "pg_catalog"."default",
  "method" varchar(255) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6),
  "describe" varchar(255) COLLATE "pg_catalog"."default",
  "is_delete" int2,
  "respond" text COLLATE "pg_catalog"."default",
  CONSTRAINT "api_auto_test_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."api_auto_test" 
  OWNER TO "postgres";

CREATE TRIGGER "update_time" BEFORE UPDATE ON "public"."api_auto_test"
FOR EACH ROW
EXECUTE PROCEDURE "public"."up_timestamp"();



自动更新时间

create or replace function up_timestamp() returns trigger as
$$
begin
    new.update_time= current_timestamp;
    return new;
end
$$
language plpgsql;

create trigger update_time before update on api_auto_test for each row execute procedure up_timestamp();


运行项目
1. 导出安装的包 pip install -r requirements.txt
2. 数据线连接手机
3. 直接运行run.py


注意：
1.手机要开启开发者模式 开启usb调试 允许模拟点击
2.本项目的ui自动化是用airtest写的，需要手机连接电脑



笔记

导出当前项目的所有包  pipreqs . --encoding=utf8 --force


