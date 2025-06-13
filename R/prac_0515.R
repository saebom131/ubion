msg <- "hello"
msg

x <- 100            # 변수
typeof(x)           # 데이터타입 확인

v <- c(1,2,3,4,5)   # 벡터
print(v)

score=85      
if(score>=90) {     # if 조건문
  print("A")
} else if(score>=80) {
  print("B")
}

result=0
for(i in 1:10) {
  result <- result+i
}
print(result)

names <- c("alice", "bob", "charlie")   
which(names=="bob")     # 해당값이 있는 위치(인덱스) 출력

for(i in 1:20) {        # for 반복문
  if(i>=5) {
    break;
  }
  print(i)
}

i=1
sum=0
while(i<=10) {        # while 조건문
  sum <- sum + i
  i <- i + 1
}
print(sum)


if(x%%7==0) {
  print('7의 배수입니다')
} else {
  print('7의 배수가 아닙니다')
}

for(i in 1:100) {     # for, if 문
  if(i%%3==0) {
    print(i)
  }
}

