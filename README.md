MYSQL

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

创建pg表

CREATE TABLE "public"."api_auto_test" (
  "id" int8 NOT NULL,
  "data" json,
  "assert" json,
  "uri" varchar(255) COLLATE "pg_catalog"."default",
  "method" varchar(255) COLLATE "pg_catalog"."default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp(6),
  "describe" varchar(255) COLLATE "pg_catalog"."default",
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
