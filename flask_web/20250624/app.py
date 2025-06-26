from flask import Flask, request, render_template
import random

app = Flask(__name__)

# api 생성
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/password', methods=['post'])
def password():
    # 유저가 보낸 데이터가 post 방식
    user_pass = request.form['user_pass']
    print(user_pass)
    return ''

@app.route('/game')
def game():
    # 유저가 보낸 데이터를 변수에 저장
    _user = request.args['user_select']
    # 컴퓨터가 가위, 바위, 보 중 랜덤 선택
    com_list = ['가위', '바위', '보']
    com_select = random.choice(com_list)

    print(f'유저가 보낸 데이터 : {_user}')
    print(f'서버가 선택한 데이터 : {com_select}')

    if _user == com_select:
        result = '무승부'
    else:
        if _user == '가위':
            if com_select == '보':
                result = '승리'
            else:
                result = '패배'
        elif _user == '바위':
            if com_select == '가위':
                result = '승리'
            else:
                result = '패배'
        else:
            if com_select == '바위':
                result = '승리'
            else:
                result = '패배'
    
    print(f'결과 : {result}')
    return result

@app.route('/game_result')
def game2():
    # 유저가 비동기 방식으로 보낸 데이터 변수에 저장
    _user = request.args['user_select']
    # 컴퓨터가 가위, 바위, 보 중 랜덤 선택
    com_list = ['가위', '바위', '보']
    com_select = random.choice(com_list)

    print(f'유저가 보낸 데이터 : {_user}')
    print(f'서버가 선택한 데이터 : {com_select}')

    if _user == com_select:
        result = '무승부'
    else:
        if _user == '가위':
            if com_select == '보':
                result = '승리'
            else:
                result = '패배'
        elif _user == '바위':
            if com_select == '가위':
                result = '승리'
            else:
                result = '패배'
        else:
            if com_select == '바위':
                result = '승리'
            else:
                result = '패배'
        
        # return 데이터가 ajax에서 type이 json으로 설정
        # json과 같은 형태 -> dict
        res_data = {
            'user' : _user,
            'server' : com_select,
            'result' : result
        }
        return res_data
app.run(debug=True)