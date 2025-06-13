# 패키지 설치
install.packages('dplyr')
library(dplyr)

for(i in 1:6) {
  for(j in 1:6) {
    if(i+j==10) {
      print(c(i, j))
    }
  }
}

i<-1
j<-1

while(i<7) {
  j<-1
  while(j<7) {
    if(i+j==10) {
      print(c(i, j))
    }
    j<-j+1
  }
  i<-i+1
}

func_1 <- function() {
  print('Hello R')
}
func_1()

func_2 <- function(x, y) {
  return (x+y)
}

func_2(3, 4)

func_3 <- function(x, y) {
  return (x^y)
}

func_3(5,3)

func_3(y=10, x=2)

func_4 <- function(x, y=3,z=2) {
  return ( (x+y)^z )
}

func_4(1)

func_4(1, 2)

func_5 <- function(...) {
  print(c(...))
}

func_5(1, 2,3,4, 5)
func_5(1,2,3)

func_sum <- function(...) {
  result <- 0
  for(i in c(...)) {
    result <- result+i
  }
  return (result)
}
func_sum(1,2,3,4,5)
func_sum(1:10)
func_sum(c(1:10))

         
func_sum_2 <- function(x) {
  result = 0
  for(i in x) {
    result <- result + i
  }
  return (result)
}
func_sum_2(c(1, 2, 3, 4, 5))
func_sum_2(1,2,3)

func_sum_3 <- function(start, end) {
  result = 0
  for(i in start: end) {
    result = result+i
  }
  return (result)
  
}
func_sum_3(1,10)
func_sum_3(10,1)

func_sum_4 <- function(start, end) {
  result=0
  if(start<end) {
    while(start<=end) {
      result=start+result
      start=start+1
    }
  } else {
    while(end<=start) {
      result = result+end
      end=end+1
    }
  }
  return (result)
}
func_sum_4(1, 10)
func_sum_4(10, 1)

func_sum_5 <- function(start, end) {
  result<-0
  if(start<end) {
    s<-start
    e<-end
  }else {
    s<-end
    e<-start
  } 
  while(s<=e) {
    result=result+s
    s<-s+1
  }
  return (result)
}

func_sum_5(1,10)
func_sum_5(10,1)

func_mean <- function(...) {
  sum_data<-0
  cnt=0
  for(i in c(...)) {
    sum_data=sum_data+i
    cnt=cnt+1
  }
  return (sum_data/cnt)
}
func_mean(2,4,6,8,10)

"%s%" = function(x, y) {
  return ((x+y)^y)
}

5 %s% 2
func_6 = function(x,y) {
  return ((x+y)^y)
}
func_6(5,2)

names <- c('test', 'test2', 'test3')
grade <- c(1,2,2)
student<- data.frame(names, grade)
student
typeof(student)

midterm <- c(70,80,90)
final <- c(100,90,95)
score<-cbind(midterm, final)
score
typeof(score)

gender<-c('F', 'F', 'M')
data.frame(student, score, gender) -> students
students

students$midterm
students[['names']]
students[[2]]
students[1]
typeof(students[1])
typeof(students[[2]])
students[1,]
students[1,3]
students[c(2,3), c('midterm', 'final')]
students[c(1), c(3)]

students$midterm >= 80 -> flag
flag
students[flag, c('names', 'grade', 'gender')]

new_student <- data.frame(
  names='test4',
  gender='M',
  final=70,
  midterm = 60,
  grade=3
)
new_student
rbind(students, new_student) ->students
students
students$midterm + students$final -> total
cbind(students, total) -> students
students
students$total/2 -> students$mean
students

df <- read.csv("../csv/csv_exam.csv")
df
df2 <- read.csv('C:\\ubion\\csv\\csv_exam.csv')
df2

head(df)
head(df, 3)
tail(df)
tail(df, 3)
dim(df)
str(df)
summary(df)
View(df)

df$mean <- (df$math+df$english+df$science) / 3
df$mean
df

ifelse(
  df$mean>=70,
  'pass',
  'fail'
) -> df$check
head(df, 5)

df %>% 
  mutate(sum = math+english+science) -> df
df
