install.packages('dpylr')
library(dplyr)

install.packages('foreign')
library('foreign')

read.spss("../csv/Koweps.sav", to.data.frame = T) -> welfare
View(welfare)

welfare %>% rename(
  gender = h10_g3,
  birth = h10_g4,
  code_job = h10_eco9,
  income = p1002_8aq1,
  loc = h10_reg7
) %>% select(gender, birth, code_job, income, loc) -> df

str(df)
df
summary(df)

table(
  is.na(df)
)

table(is.na(df$gender))
table(is.na(df$birth))
table(is.na(df$code_job))
table(is.na(df$income))
table(is.na(df$loc))

ifelse(df$gender == 1, 'male','female') -> df$gender
df
table(df$gender)

df %>% 
  select(gender, income) %>% 
  filter(!is.na(income) & income != 0 & income != 9999) %>% 
  group_by(gender) %>% 
  summarise(mean_income = mean(income)) -> gender_income

ggplot(
  gender_income,
  aes(
    x=gender,
    y=mean_income
  )
) + geom_col()

df
df %>% 
  mutate(age=2015-birth+1) %>% 
  select(age, income) %>% 
  filter(!is.na(income)&!income %in% c(0,9999)) %>% 
  group_by(age) %>% 
  summarise(mean_income = mean(income)) -> age_income
df
ggplot(
  age_income,
  aes(
    x=age,
    y=mean_income
  )
) + geom_col()

ggplot(
  age_income,
  aes(
    x=age,
    y=mean_income
  )
) +geom_line()

age_income %>% 
  arrange(-mean_income) %>% 
  head(5)

df %>% 
  mutate(age=2015-birth+1) %>% 
  mutate(ageg = ifelse(
    20<=age & 40>age,
    'young',
    ifelse(
      age<60,
      'middle',
      'old'
    )
  )
) %>% 
  filter(!is.na(income) & !income %in% c(0,9999)) %>% 
  group_by(ageg) %>% 
  summarise(mean_income=mean(income)) -> ageg_income

ageg_income

ggplot(ageg_income,
       aes(
         x=ageg,
         y=mean_income)
      ) +geom_col()+scale_x_discrete(
         limits=c('young', 'middle','old')
       )

df_1 <- data.frame(
  id = 1:3,
  score = c(70,80,90)
)
df_1

df_2 <- data.frame(
  id = 2:5,
  weight = c(40,50,60,70)
)
df_2

inner_join(df_1, df_2, by='id')
left_join(df_1, df_2, by='id')
right_join(df_1, df_2, by='id')
full_join(df_1, df_2, by='id')

df_3 = data.frame(
  id=c(2,2,5,5,5),
  loc=c('a','b','c','d','e')
)
left_join(df_3, df_2, by='id')

install.packages('readxl')
library(readxl)
read_excel('../csv/Koweps_Codebook.xlsx', sheet=2) -> code_book
code_book

df %>% 
  filter(!is.na(code_job)) %>% 
  filter(income==0)

inner_join(df, code_book, by='code_job') -> total_df

View(total_df)
total_df %>% 
  filter(!is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_income = mean(income)) %>% 
  arrange(-mean_income) %>% 
  head(10)

total_df %>% 
  filter(gender == 'female' & !is.na(income)) %>% 
  group_by(job) %>% 
  summarise(mean_income = mean(income)) %>% 
  arrange(-mean_income) %>% 
  head(5)
