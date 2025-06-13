-- tran_1, tran_2, tran_d_1, tran_d_2 테이블
-- sales records 테이블 -> line 21
# 유니언 결합
# 단순한 행 결합
(SELECT * FROM `tran_1`
UNION
SELECT * FROM `tran_2`;)

SELECT * FROM `tran_d_1`
UNION
SELECT * FROM `tran_d_2`;

# 유니언 결합을 한 2개의 테이블 조인 결합
# 총 4개의 테이블 결합
SELECT * FROM
(SELECT * FROM `tran_1` UNION SELECT * FROM `tran_2`) as `tran`
LEFT JOIN
(SELECT * FROM `tran_d_1` UNION SELECT * FROM `tran_d_2`) as `tran_d`
ON `tran`.`transaction_id` = `tran_d`.`transaction_id`;

-- salesrecords 테이블
# 백틱 ` ` 사용 이유: 테이블 이름이나 컬럼 이름 중간에 공백 존재할 때 사용
SELECT * FROM emp;
SELECT * FROM `sales records`;

# 그룹화
SELECT `Region`, 
SUM(`Total Profit`) as `sum_profit` 
FROM `sales records`
GROUP BY `Region`;

# sales records에서 
# country별 그룹화 & total profit의 그룹화 합산
# 합산 데이터가 28000000 이상인 데이터 확인
SELECT `Country`,
SUM(`Total Profit`) as `sum_profit`
FROM `sales records`
GROUP BY `Country`
HAVING `sum_profit` >= 28000000;

# Region이 Asia인 데이터에서
# country를 기준으로 그룹화
# total profit을 그룹 합산
# 그룹 합산된 데이터를 이용해 내림차순 정렬 : ORDER BY 컬럼명 desc;
SELECT `Country` as `국가`,
SUM(`Total Profit`) as `총 이윤`
FROM `sales records`
WHERE `Region` = 'Asia'
GROUP BY `Country`
ORDER BY `총 이윤` desc
LIMIT 5;	# 상위 k개만 출력 -> LIMIT k

SELECT `Region` FROM `sales records`
GROUP BY `Region`
ORDER BY `Region`
LIMIT 5;