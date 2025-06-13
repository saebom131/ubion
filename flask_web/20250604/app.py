# flask 프레임워크 로드 
# 프레임워크는 규모가 크기 때문에 전체 로드 대신 일부만 로드
from flask import Flask, render_template, request, redirect
# Flask: 웹서버 구동, 특정 api(주소)를 생성해 함수들과 연결
# render_template(): 작업 공간에서 templates라는 하위 폴더의 
#                    HTML 파일을 요청한 유저에게 보내주는 역할
# request(): 유저가 보낸 메시지를 되돌려주는 기능
# redirect(): 특정한 주소로 요청을 보내는 기능()

# Flask 클래스 생성
app = Flask(__name__)

user_data = {
    'id' : 'test',
    'pass' : '1234',
    'nickname' : 'bom'
}
# 첫번째 api 생성
@app.route('/')
# 127.0.0.1:5000(root 주소) + '/' 해당 주소로 요청이 들어왔을 때
# 바로 아래의 함수 호출 -> 함수 이름 조건: 중복 사용 불가
def index():
    # render_template() 함수 이용해 html 문서를 유저에게 반환(응답)
    # return '<h1>Title</h1> <br> abcdefg<b>hijk</b>lmn'
    return render_template('index.html')

@app.route('/send_get')
def send_get():
    # 유저가 보낸 데이터 확인 -> 유저가 보낸 데이터는 request
    # get 방식으로 보낸 데이터는 request 안의 args에 데이터가 존재
    print(f'유저가 보낸 데이터 : {request.args}')
    # request.args에는 유저가 보낸 데이터가 
    # 딕셔너리 {input_id : test, input_pass : 1234}의 형태로 들어옴
    # 유저가 보낸 아이디 값: request.args['input_id']
    user_id = request.args['input_id']
    # 유저가 보낸 패스워드 값: request.args['input_pass']
    user_pass = request.args['input_pass']
    print(f'유저가 입력한 아이디: {user_id}, 비밀번호: {user_pass}')
    return ""

# post 방식의 api 생성
# /send_post라는 post 형식으로 주소 생성
@app.route('/send_post', methods=['post'])
def send_post():
    # post 방식으로 보낸 데이터 로드
    # post 방식으로 보낸 데이터는 request 안의 from에 존재
    print(f'유저가 보낸 데이터: {request.form}')
    # 유저가 보낸 데이터 값
    user_id = request.form['input_id']
    user_pass = request.form['input_pass']
    print(f'유저의 id: {user_id}, pass: {user_pass}')

    # user_data와 user_id, user_pass 비교 -> 모두 참이라면 로그인 성공
    if (user_id == user_data['id']) and (user_pass == user_data['pass']):
        # 로그인 성공
        # return '로그인 성공'
        # user_data에서 nickname 추출
        nick = user_data['nickname']
        # render_template() 함수 이용해 페이지와 닉네임 전송
        return render_template('main.html', user_nick = nick)
    else:
        # return '로그인 실패'
        # 로그인이 실패했을 때는 로그인화면(root)로 되돌아감
        return redirect('/')

@app.route('/test')
def test():
    return render_template('test.html')

        
# 웹 서버 실행
app.run(debug=True)     
# debug=True -> 코드 수정시 자동 재실행 (cmd 서버 종료&재실행 불필요)
