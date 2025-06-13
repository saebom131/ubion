# flask 프레임워크 로드
# 프레임워크 -> 굉장히 많은 변수, 함수, 클래스의 덩어리
# 일반적으로 프레임워크 로드 시에는 전체를 로드하지 않음
# 특정 모듈에서 일부 기능만 가지고 올 때 -> from ... import ...
# Flask -> 웹서버를 실행하고 주소를 생성하여 함수에 연결하는 기능
# render_template -> 함수에서 return에 HTML과 연결해주는 기능을 가진 함수 로드
# render_template() 함수 -> HTML 문서를 기본 경로가 현재 경로에서 templates 
from flask import Flask, render_template

# Flask class 생성
# Flask class 생성자 함수에는 필수 인자 1개 필요 (파일명)
# 파일의 이름 -> app.py -> __name__
# __name__ 사용 -> 파일 이름 변경 시에도 이름 그대로 불러옴
app = Flask(__name__)

# route(): 네이게이터 함수
# 특정한 주소로 요청이 들어왔을 때 바로 아래의 함수와 연결해주는 기능
@app.route('/')
def index():
    # return 'Hello Flask'
    # templates 폴더에 있는 index.html을 되돌려줌
    return render_template('index.html')

# route('/second') -> root(127.0.0.1:5000) + '/second'
# -> 주소로 요청이 들어왔을 때 -> 웹브라우저에서 해당 주소를 입력하고 엔터키 눌렀을 때
# 아래의 함수를 호출
    # 함수 생성 주의사항: 함수의 이름은 자유지만 중복 불가
@app.route('/second')
def second():
    return 'Second Page'


# Flask 안에 존재하는 서버 생성하는 함수 호출
app.run()