import pandas as pd
from datetime import datetime
import numpy as np

# 밴드 생성 함수
def create_band(_df, _start = '2010-01-01', _end = datetime.now(), _col = 'Adj Close', _cnt = 20):
    # 입력받은 데이터프레임 복사본 생성
    df = _df.copy()

    # 'Date'가 컬럼에 존재하면 인덱스로 변환
    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)
    # df의 인덱스를 시계열로 변경
    df.index = pd.to_datetime(df.index)
    
    # 기준이 되는 컬럼을 제외하고 모두 제거 -> 특정 컬럼만 선택
    df = df[[_col]]

    # 결측치, 무한대 제거
    flag = df.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
    df = df.loc[-flag, ]

    # 이동평균선 컬럼 생성
    df['center'] = df[_col].rolling(_cnt).mean()
    std_data = df[_col].rolling(_cnt).std()
    # 상단 밴드 생성: 이동평균선 + (2 * 20개 데이터의 표준편차)
    df['ub'] = df['center'] + (2 * std_data)
    # 허단 밴드 생성: 이동평균선 + (2 * 20개 데이터의 표준편차)
    df['lb'] = df['center'] - (2 * std_data)

    # 시작시간, 종료시간으로 데이터 필터링
    try: 
       df = df.loc[_start : _end, ]
    except Exception as e:
        print(e)
        print('인자값이 잘못되었습니다')
        return ""
    
    return df

# 트레이드 컬럼 생성 함수
def create_trade(_df):
    # 데이터프레임의 복사본 생성
    df = _df.copy()
    
    df['trade'] = ''
    
    # 기준 컬럼의 이름을 변수에 저장
    col = df.columns[0]
    
    # 기준 컬럼의 값과 밴드 값을 비교해 거래내역 컬럼 생성 
    for idx in df.index:
    # idx에 들어오는 데이터: 시계열 데이터
    # 기준 컬럼의 값이 상단밴드보다 크거나 같은 경우
        if df.loc[idx, col] >= df.loc[idx, 'ub']:
                df.loc[idx, 'trade'] = ''
        
        # 수정종가가 하단밴드보다 작거나 같은 경우
        elif df.loc[idx, col] <= df.loc[idx, 'lb']:
                df.loc[idx, 'trade'] = 'buy'
        
        # 수정종가가 상단밴드보다 낮고 하단밴드보다 높은 경우
        else:
            # 현재 보유상태라면 보유 유지
            # 보유상태가 아니라면 -> 유지
            # 전날의 trade를 그대로 유지
            df.loc[idx, 'trade'] = df.shift().loc[idx, 'trade']

    
    return df

# 수익률 계산 함수 create_rtn()
def create_rtn(_df):
    # 데이터프레임 복사본 생성
    df = _df.copy()
    # 기준이 되는 컬럼 이름을 변수에 저장
    col = df.columns[0]
    # 수익률 컬럼 생성, 기본값 1
    df['rtn'] = 1

    # 수익률 계산
    for idx in df.index:
        # 매수가 생성
        # 전날 -> shift() 사용
        if (df.shift().loc[idx, 'trade'] == '') & \
            (df.loc[idx, 'trade'] == 'buy'):
            # 매수가를 변수에 저장
            buy = df.loc[idx, col]
            print(f'매수일: {idx}, 매수가: {buy}')
        # 매도가 생성
        elif (df.shift().loc[idx, 'trade'] == 'buy') & \
            (df.loc[idx, 'trade'] == ''):
            # 매도가를 변수에 저장
            sell = df.loc[idx, col]
            # 수익률 계산
            rtn = sell / buy
            df.loc[idx, 'rtn'] = rtn
            print(f'매도일: {idx}, 매도가: {sell}, 수익률: {rtn}')

    # 누적수익률 계산
    df['acc_rtn'] = df['rtn'].cumprod()
    # 최종누적수익률
    final_acc_rtn = df.iloc[-1, -1]
    
    return df, final_acc_rtn