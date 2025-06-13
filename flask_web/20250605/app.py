from flask import Flask, render_template, request
import pandas as pd

# Flass class 생성
# __name__: 파일의 이름
app = Flask(__name__)

# corona.csv 파일 로드 (index는 첫번째 컬럼 사용)
corona = pd.read_csv('./data/corona.csv', index_col=0)
# stateDt의 데이터를 기준으로 오름차순 정렬

corona.sort_values(['stateDt'], inplace=True)
# 일일확진자 컬럼 생성 -> 오늘의 총 확진자수 - 어제(전 행)의 총 확진자수
corona['일일확진자'] = (corona['decideCnt'] - corona['decideCnt'].shift(1)).fillna(0)
# 일일사망자 컬럼 생성 -> 전 행 데이터의 차이값
corona['일일사망자'] = corona['deathCnt'].diff(1).fillna(0)

# api 생성
@app.route('/')
def index():
    # 127.0.0.1:5000/ 요청 들어왔을 때 자동 호출
    # corona 데이터에서 stateDt, 일일확진자, 일일사망자 컬럼 추출
    df = corona[ ['stateDt', '일일확진자', '일일사망자', 'stateTime', 'updateDt']]
    # 해당 데이터에서 가장 최근의 데이터 값들을 추출
    date = df.iloc[-1, 0]
    decide = df.iloc[-1, 1]
    death = df.iloc[-1, 2]
    print(f'최근일: {date}, 일일확진자수: {decide}, 일일사망자수: {death}')

    # 테이블에서 컬럼 이름을 리스트로 생성
    col_list = list(df.columns)
    # 전체 데이터프레임을 dict 형태로 변환 -> to_dict()
    dict_data = df.to_dict(orient='records')
    print(f'데이터프레임 컬럼의 목록: {col_list}')
    print(f'데이터프레임 딕셔너리형 변환: {dict_data[0]}')
    # 데이터의 포맷 변경
    date = str(date)
    date = date[:4]+'년' + date[4:6]+'월' + date[6:]+'일'

    return render_template('corona.html',
                           statedt = date,
                           decidecnt = decide,
                           deathcnt = death,
                           cols = col_list,
                           values = dict_data)

@app.route('/corona')
def corona2():
    df = corona[ ['stateDt', '일일확진자', '일일사망자', 'stateTime', 'updateDt'] ]
    # 만약 유저가 보낸 데이터가 존재한다면?
    if request.args:
        # print('데이터가 존재')
        # 유저가 보낸 데이터 -> 변수에 저장
        s_year = request.args['s_year']
        s_month = request.args['s_month']
        s_day = request.args['s_day']
        e_year = request.args['e_year']
        e_month = request.args['e_month']
        e_day = request.args['e_day']

        if len(s_month) == 1:
            s_month= '0' + s_month
        if len(s_day) == 1:
            s_day = '0' + s_day
        if len(e_month) == 1:
            e_month = '0' + e_month
        if len(e_day) == 1:
            e_day = '0' + e_day
        start = s_year + s_month + s_day
        end = e_year + e_month + e_day

        # df의 stateDt보다 start보다 크거나 같다
        # and
        # df의 stateDt가 end보다 작거나 같다
        flag = df['stateDt'] >= int(start)
        flag2 = df['stateDt'] <= int(end)
        df = df.loc[flag & flag2, ]
        date = f'{start} ~ {end}'
        decide = df['일일확진자'].sum()
        death = df['일일사망자'].sum()
    else:
        print('데이터가 존재하지 않음')
        # 해당 데이터에서 가장 최근의 데이터 값들을 추출
        date = df.iloc[-1, 0]
        decide = df.iloc[-1, 1]
        death = df.iloc[-1, 2]
    
    # 데이터프레임 -> html로 변환
    html_data = df.to_html(index=False)
    # 그래프에서 사용할 x, y축 데이터 생성(리스트 형태)
    x = df['stateDt'].to_list()
    y = df['일일확진자'].to_list()
    
    return render_template('corona2.html',
                           statedt = date,
                           decidecnt = decide,
                           deathcnt = death,
                           table = html_data,
                           axis_x = x,
                           axis_y = y)

app.run(debug=True)