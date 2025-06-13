# 함수, 패키지, 데이터분석기초 
# 반복문 문제 - 복습
# 2개의 주사위가 존재한다.
# 주사위를 굴려서 주사위의 합이 10인 모든 경우의 수를 출력하시오.
# 2개의 주사위의 경우의 수 : 36개
# 1번째 -> 6, 4
# 2번째 -> 5, 5
# 3번재 -> 6, 4

# for문
# 첫번째 주사위의 경우의수 반복문
for(i in 1:6) {
  # 두번째 주사위의 경우의수 반복문
  for(j in 1:6) {
    if(i+j==10) {
      res <- c(i,j)
      print(res)
    }
    j <- j+1
  }
  i <- i+1
}
# 첫번째 반복 : i=1, j=1
# 두번째 반복 : i=1, j=2
# 세번째 반복 : i=1, j=3
# ...
# 7번째 반복 : i=2, j=1

# while문
i <- 1
j <- 1
# 첫번째 주사위의 경우의 수
while(i<=6) {
  # 두번째 주사위의 경우의 수
  while(j<=6) {
    # 두 주사위의 합이 10이라면
    if(i+j==10) {
      print(c(i,j))
    }
    # j를 1씩 증가
    j<-j+1
  }
  j <- 1
  # i를 1씩 증가
  i<-i+1
}


# 함수
# 특정한 행동을 하는 코드
# 입력값을 받아서 연산을 한 뒤 되돌려줌

# 매개변수와 인자가 존재하지 않는 경우
func_1 <- function() {
  print('Hello R')
}

# 함수 호출
func_1()

# 매개변수가 존재하지 않는 함수에 인자 입력
func_1('a')
# => 에러 발생: 사용되지 않은 인자(입력값을 저장한 공간이 존재X)

# 매개변수 존재하는 함수 생성
func_2 <- function(x, y) {
  # 매개변수는 2개
  return (x+y)
}

# func_2() 함수 호출 -> 매개변수 2개 -> 인자 2개
func_2(2,3)

func_3 <- function(x, y) {
  return(x^y)
}

func_3(10,2)
func_3(2,10)
# func_3에 x=2, y=10 대입
func_3(y=10, x=2)

# 매개변수에 기본값이 존재하는 함수
func_4 <- function(x, y = 3, z = 2) {
  return ( (x+y)^z )
}

func_4(1)
func_4(1,2)
func_4(2,3,3)
func_4(2, z=3)

# 인자의 개수가 가변인 경우
func_5 <- function(...) {
  print(c(...))
}

func_5(1,2,3,4,5)
func_5(1,6,3)
func_5(1,2,3,4,5,6,7,8,9,10)






# 합계를 구하는 함수 생성
# 인자가 가변인 경우
func_sum <- function(...) {
  # 누적합을 할 수 있는 데이터 생성
  result <- 0
  # ... 데이터를 반복 실행하여 result에 누적합
  for(i in c(...)) {
    result <- result + i
  }
  # 누적합이 된 결과값 반환
  return (result)
}
func_sum(1,2,3,4,5)
func_sum(1,2,3,4,5,6,7,8,9,10)
func_sum(10,3)
# 인자를 벡터데이터로 입력하는 경우
func_sum_2 <- function(x) {
  # x에는 벡터데이터가 입력 가정
  result <- 0
  for(i in x) {
    result <- result + i
  }
  return (result)
}
func_sum_2( c(1,2,3,4,5) )
# 에러 발생 -> 벡터데이터로 입력 필요
func_sum_2(1,2,3)

# 함수 생성
# 매개변수 2개 사용
# 시작값, 종료값
func_sum_3 <- function(start, end) {
  result <- 0
  for(i in start:end) {
    result <- result + i
  }
  return (result)
}
func_sum_3(1, 10)
func_sum_3(10, 1)

func_sum_4 <- function(start, end) {
  result <- 0
  if(start < end) {
    while(start <= end) {
      result <- start + result
      start <- start + 1
    }
  }else {
    while(end <= start) {
      result <- result + end
      end <- end + 1
    }
  }
  return (result)
}
func_sum_4(1, 10)
func_sum_4(10, 1)

func_sum_5 <- function(start, end) {
  result <- 0
  if(start < end) {
    s <- start
    e <- end
  }else {
    s <- end
    e <- start
  }
  while(s <= e) {
    result <- result + s
    s <- s + 1
  }
  return (result)
}
func_sum_5(1, 10)
func_sum_5(10, 1)

# 함수를 생성
# 인자의 개수가 가변
# 해당하는 인자들의 평균값을 출력하는 함수
func_mean <- function(...) {
  # 합계를 구하기 위한 초기값 0
  sum_data <- 0
  # 개수를 확인하기 위한 변수 생성 0
  cnt <- 0
  # 반복문 생성
  for(i in c(...)) {
    # 누적합
    sum_data <- sum_data + i
    # 반복 실행할때마다 개수 1씩 증가
    cnt <- cnt + 1
  }
  # 누적합과 개수를 나눠준 값 반환
  return (sum_data / cnt)
}
func_mean(2,4,6,8,10)

# 커스텀 연산자 %s%
"%s%" <- function(x, y) {
  return ( (x+y) ^ y )
}
5 %s% 2
func_6 <- function(x,y) {
  return ( (x+y) ^ y)
}
func_6(5, 2)

# 데이터프레임
# 데이터의 분석에서 가장 많이 사용되는
# 2차원 데이터의 형태
names <- c('test', 'test2', 'test3')
grade <- c(1, 2, 2)
# 벡터데이터를 이용해서 데이터프레임 생성
# 같은 길이의 벡터데이터 이용
student <- data.frame(names, grade)
student
typeof(student)

midterm <- c(70, 80, 90)
final <- c(100, 90, 95)
score <- cbind(midterm, final)
score
typeof(score)

# 벡터데이터 생성
gender <- c('F', 'F', 'R')
# 데이터프레임, 행렬, 벡터 데이터를 결합
data.frame( student, score, gender ) -> students

# 특정 컬럼의 데이터를 확인
# 결과가 벡터데이터로 나오는 경우
# 데이터프레임명$컬럼명
students$midterm
# 데이터프레임명[[컬럼명]]
students[['names']]
# 데이터프레임명[[컬럼의 위치]]
students[[2]]
# 컬럼을 이용하여 필터는 되지만 결과 데이터프레임
students[1]

# 특정 인덱스의 데이터를 확인
students[1, ]
students[1, 3]
# 2, 3번 학생의 중간과 기말 성적 추출
students[ c(2,3), c('midterm', 'final') ]
students[ c(1), c(3) ]

# 조건식을 이용해서 데이터프레임 필터링
# 중간 성적이 80점 이상인 학생 정보 확인
students$midterm >= 80 -> flag
# flag는 인덱스의 조건식
# 컬럼의 조건식 -> names, grade, gender
students[ flag, c('names', 'grade', 'gender') ]

# 데이터 추가 (행추가)
# 데이터의 형태가 같은 행을 추가
new_student <- data.frame(
  names = 'test4',
  gender = 'M',
  final = 70,
  midterm = 60,
  grade = 3
)
new_student
# students와 new_student 결합
rbind(students, new_student) -> students

# 파생변수 생성 -> 열 결합
# 중간 성적과 기말 성적을 더한 총 점수 생성
students$midterm + students$final -> total
# 열 결합 -> cbind()
cbind(students, total) -> students
# 평균 점수 컬럼을 생성
students$total / 2 -> students$mean
students

# 외부의 데이터 파일을 로드
# 경로(주소)
# 절대경로
  # 절대적인 주소
  # 누가 보더라도 같은 위치
  # 환경이 변하더라도(컴퓨터) 같은 위치를 지정
  # ex) window : c\users\admin\a.txt
  # ex) mac : ~/user/a.txt
  # ex) https://www.google.com
# 상대경로
  # 상대적인 주소
  # 환경이 변할때 위치로 같이 변경
  # ./ : 현재 작업중인 디렉토리(위치)
  # ../ : 부모(상위) 디렉토리로 이동
  # /디렉토리명/ : 자식(하위) 디렉토리로 이동
  # 현재 디렉토리(./) -> 상위로 이동(../) -> 
  # csv 하위 이동(csv/) -> csv_exam.csv
  #  ../csv/csv_exam.csv

# 외부의 csv 파일을 로드 -> 함수를 이용
# csv 파일을 로드하여 데이터프레임으로 생성
# 상대 경로로 파일 로드
df <- read.csv('../csv/csv_exam.csv')
df
# 절대 경로로 파일 로드
df2 <- read.csv('C:\\ubion\\csv\\csv_exam.csv')
df2

# 데이터프레임 확인
# 상위의 데이터 확인 (6개)
head(df)
# 하위의 데이터 확인 (6개)
tail(df)
tail(df, 3)   # 데이터 개수 지정

# 데이터프레임 크기 확인 => dim()
dim(df)
# 데이터프레임 정보 확인 => str()
str(df)
# 통계 정보 확인 => summary()
summary(df)
# 뷰어창에서 데이터 확인 => View()
View(df)

# 파생변수 생성
# 평균 성적 -> (수학+영어+과학) / 3
df$mean <- (df$math + df$english + df$science) / 3
df

# ifelse(조건식, 참인경우 결과, 거짓인경우 결과)
ifelse(
  df$mean >= 70,
  'pass',
  'fail'
) -> df$check
head(df, 5)
