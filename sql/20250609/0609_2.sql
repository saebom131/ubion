-- emp 테이블&dept 테이블

# emp 테이블에서 SAL 컬럼의 데이터가 1500 이상인 데이터 확인
SELECT * FROM emp WHERE `SAL` >= 1500;

# emp 테이블에서 JOB 컬럼의 데이터가 MANAGER이고 SAL이 1500 이상인 사원의 이름 출력
select `ENAME` from emp where `job`='MANAGER' and `SAL` >= 1500;

# SAL이 1500 이상이고 2500 이하인 사원의 전체 정보 출력
select * from `emp` where `SAL`>=1500 and `sal`<=2500;
select * from `emp` where `SAL` between 1500 and 2500;		# between 사용

# JOB이 `MANAGER'이거나 'SALESMAN'인 데이터 확인
select * from `emp` where `job`='MANAGER' or `job`='SALESMAN';
select * from `emp` where `job` in ('MANAGER', 'SALESMAN');

# 부서의 지역이 NEW YORK인 사원의 정보 확인
select `DEPTNO` from `DEPT` where `LOC` = 'NEW YORK';
select * from `emp` where `DEPTNO` in (10);

select * from `emp` where `DEPTNO` in (select `DEPTNO` from `DEPT` where `LOC` = 'NEW YORK');

# emp 테이블에는 deptno가 10, 20, 30
# dept 테이블에는 deptno가 10, 20, 30, 40
# 조인 결합이 dept 테이블 기준 -> 40 데이터 존재
# emp 테이블 기준 -> 40 데이터 존재X
# 두 테이블이 공통으로 가지고 있는 기준 -> 40 존재X 
select * from `emp` left join `dept` on `emp`.`DEPTNO` = `dept`.`DEPTNO`;	

# as: 별칭 지정 (생략 가능)
select * from `emp` as `a` left join `dept` as `b`
on `a`.`DEPTNO` = `b`.`DEPTNO`;

SELECT * FROM `emp` as `a` LEFT JOIN `dept` as `b`
ON `a`.`DEPTNO` = `b`.`DEPTNO`
WHERE `b`.`LOC` = 'NEW YORK'; 