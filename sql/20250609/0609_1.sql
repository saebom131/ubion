insert into `ubion`.`user_info` values('test2', '0000', 'park', 20);

use `ubion`;	-- 데이터베이스 변경

select * from `user_info`;

insert into `user_info` values('test3', '9999', 'lee', '50');	-- age 필드 에러 발생X(int로 자동 변경)
insert into `user_info` values('test3', '9999', 'lee', 'a');	-- age 필드에서 에러 발생(int 형식x)
