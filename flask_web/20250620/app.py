# 프레임워크 로드
from flask import Flask, render_template, request
import pandas as pd

# Flask class 생성
# 생성자 함수 필요한 인자: 파일의 이름
app = Flask(__name__)

# 네비게이터 -> 특정한 주소로 요청이 들어왔을때 함수와 연결
# route() 함수에 인자의 의미
# root url + 주소
@app.route('/')
def index():
    # csv 파일 로드
    df = pd.read_csv('csv/AAPL.csv').tail(20)
    # 컬럼의 이름들을 리스트로 변경해 변수에 저장
    cols = list(df.columns)
    # values를 리스트 안에 딕셔너리 형태로 변환
    value = df.to_dict('records')

    return render_template('index.html',
                           columns = cols,
                           values = value)


# 웹서버 실행
app.run(debug=True)
