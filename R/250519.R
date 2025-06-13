# dplyr 패키지 설치 -> 파이프연산자 %>% 사용
install.packages('dplyr')
library(dplyr)

# spss 파일을 로드하기 위한 패키지 설치
# .sav 파일을 로드하는 기능이 따로 존재
install.packages('foreign')
library(foreign)

# 외부의 데이터파일 로드
# 현재 디렉토리 -> 상위 폴더 이동(../)
# -> csv라는 하위 폴더로 이동(csv/) -> Koweps.sav 파일
read.spss("../csv/Koweps.sav", to.data.frame = T) -> welfare
View(welfare)

# codebook을 참고하여 데이터의 컬럼의 이름을 변경
# 컬럼의 이름을 변경하는 함수 : rename()
# rename( 데이터프레임명, 새 컬럼명 = 기존 컬럼명 )
welfare %>% rename(
  gender = h10_g3,
  birth = h10_g4,
  code_job = h10_eco9,
  income = p1002_8aq1,
  loc = h10_reg7
) %>% select(gender, birth, code_job, income, loc) -> df

# 데이터프레임 정보 확인
str(df)
# 통계 정보 확인
summary(df)

# 결측치의 개수 확인
# is -> 존재 유무, na -> 결측치
# is.na() : 결측치 -> TRUE, 아니면 -> FALSE
# table() : 데이터의 빈도수 확인
table(
  is.na(df)
)
# 각 컬럼별 결측치의 개수 확인
table(
  is.na(df$gender) )
table(is.na(df$birth))
table(is.na(df$code_job))
table(is.na(df$income))
table(is.na(df$loc))

# 성별을 male, female로 변경 
# ifelse(조건식, 참인경우 결과, 거짓인경우 결과)
ifelse(df$gender == 1, 'male', 'female') -> df$gender
table(df$gender)

# 남녀 간의 평균 임금이 얼마나 차이가 나는지?
# 특정 컬럼을 선택 (gender, income) => select()
# 성별과 임금의 결측치를 제외(0과 9999도 제외) => filter() : 인덱스 제거
# 성별을 기준으로 데이터프레임을 그룹화 => group_by()
# 임금의 그룹화 연산(평균)을 구해 새로운 데이터프레임 생성 => summarise()

df %>% 
  select(gender, income) %>% 
  # income 데이터에서 결측치가 아니라면 : !is.na(income)
  # filter(!is.na(income)) %>% 
  # filter(income != 0) %>% 
  # filter(income != 9999) %>% 
  filter( !is.na(income) & income != 0 & income != 9999 ) %>% 
  # 그룹화 : group_by(그룹화할 컬럼 이름)
  group_by(gender) %>% 
  # summarise( 컬럼의 이름 = 연산 데이터 )
  summarise( mean_income = mean(income) ) -> gender_income
# 그래프 시각화
ggplot(
  gender_income,
  aes( 
    x = gender,
    y = mean_income
  )
) + geom_col()

# 나이 컬럼 생성
# 현재 년도(2015) - birth
# 2가지 방법
# base
# 데이터프레임명$age <- 2015 - 데이터프레임명$birth
# dplyr 패키지 이용
# 컬럼 추가 함수 mutate() 함수를 이용해 컬럼 추가
# 나이별 평균 임금이 어떻게 되는가?
# 나이라는 컬럼 생성 : mutate()
# 특정 컬럼을 선택 : select()
# 임금이 0, 9999, 결측치 => 제외 : filter()
# 나이를 기준으로 그룹화 : group_by()
# 그룹화 연산 : summarise()
df %>% 
  # mutate(데이터프레임명, 컬럼명(새로 생성) = 1차원 데이터(연산))
  mutate(age = 2015 - birth + 1) %>% 
  select(age, income) %>% 
  # income에 결측치, 0, 9999 제외
  filter( !is.na(income) & !(income %in% c(0,9999)) ) %>% 
  # 나이를 기준으로 그룹화
  group_by(age) %>% 
  summarise(mean_income = mean(income)) -> age_income

# 그래프(막대) : geom_col()
ggplot(
  age_income,
  aes( 
    x = age,
    y = mean_income
  )
) + geom_col()

# 그래프(라인) : geom_line
ggplot(
  age_income,
  aes(
    x = age,
    y = mean_income
  )
) +geom_line()

# age_income에서 평균 임금이 상위 5개 출력
# age 기준으로 내림차순 정렬
# 상위 5개 데이터 선택
age_income %>% 
  arrange(-mean_income) %>%    # - : 내림차순 정렬
  head(5)       # 상위 5개만 출력

# 연령대별 평균 임금
# 나이 컬럼(age) 생성 -> 2015 - birth + 1
# 연령대 컬럼 생성 ->
  # 20세 이상 40세 미만 : 'young'
  # 40세 이상 60세 미만 : 'middle'
  # 60세 이상 : 'old'
# ifelse() 함수 이용
# 임금 결측치, 0, 9999 제외
# 연령대 기준으로 그룹화
# 임금의 평균으로 그룹화 연산
age_income

df %>% 
  mutate(age = 2015 - birth + 1) %>% 
  mutate(age_group = 
           ifelse(
             age>=20 & age<40, 
             "young", 
             ifelse(
               age<60, 
               "middle", 
               "old"))) %>% 
  filter( !is.na(income) & !(income %in% c(0,9999)) ) %>% 
  group_by(age_group)  %>% 
  summarise(mean_income = mean(income)) -> ageg_income

# x축의 순서를 고정값 지정
ggplot(ageg_income, 
       aes(x = age_group, 
           y = mean_income)
       ) + geom_col() + scale_x_discrete(
         limits = c('young', 'middle', 'old')
       )

# 조인 결합
# 특정한 조건에 맞춰 열을 결합
df_1 <- data.frame(
  id = 1:3,
  score = c(70, 80, 90)
)
df_1

df_2 <- data.frame(
  id = 2:5,
  weight = c(40, 50, 60, 70)
)
df_2
# 조인 결합 -> left, right, inner, full
# 교집합 : 2개의 데이터프레임이 모두 가지고 있는 (inner_join)
inner_join(df_1, df_2, by='id')
left_join(df_1, df_2, by='id')
right_join(df_1, df_2, by='id')
full_join(df_1, df_2, by='id')

df_3 <- data.frame(
  id = c(2, 2, 5, 5, 5),
  loc = c('a', 'b', 'c', 'd', 'e')
)
df
df_3
left_join(df_3, df_2, by='id')

# df에 code_job 컬럼과 codebook에 있는 직업 이름을 결합
# codebook.xlsx 파일 로드
install.packages('readxl')
library(readxl)
read_excel("../csv/Koweps_Codebook.xlsx", sheet = 2) -> code_book

# 조인결합
# df를 기준으로 (=교집합) => df의 code_job 데이터는 code_book에 존재

# 직업은 없는데 임금이 있는 사람
df %>% 
  filter(is.na(code_job) & !is.na(income))
# 직업은 있는데 임금이 0인 사람
df %>% 
  filter(!is.na(code_job) & income == 0)

# code_job이 결측치인 데이터는 제외
# inner_join 사용 가능
inner_join(df, code_book, by='code_job') -> total_df
View(total_df)

# 과연 어떤 직종이 돈을 가장 많이 버는가?
# 상위의 10개 직업 확인

# 임금이 결측치인 경우 제외 : filter()
# 직업을 기준으로 그룹화 : group_by()
# 그룹화 연산 -> 임금의 평균 : summarise()
# 평균 임금 내림차순 정렬 : arrange()
# 상위 10개 필터 : head()
total_df %>% 
  filter(!is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_income = mean(income)) %>% 
  arrange(-mean_income) %>% 
  head(10)

# 성별이 남자인 데이터, 인원이 10명 이상인 데이터에서 직업별 평균 임금 상위 5개
total_df %>% 
  filter(gender=='male' & !is.na(income)) %>% 
  group_by(job) %>% 
  # cnt = n() => 해당 직종별 인원수
  summarise(mean_income = mean(income), cnt = n()) %>% 
  filter(cnt>=10) %>% 
  arrange(-mean_income) %>% 
  head(5)
  

# 성별이 여자인 데이터에서 직업별 평균 임금 상위 5개
total_df %>% 
  filter(gender=='female' & !is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_income = mean(income), cnt = n()) %>% 
  filter(cnt>=10) %>% 
  arrange(-mean_income) %>% 
  head(5)



