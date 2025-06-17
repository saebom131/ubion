import pandas as pd
from datetime import datetime
import numpy as np

def bnh(_df, _start='2010-01-01', _end=datetime.now(), _col='Adj Close'):
    df = _df.copy()
    # try:
    #     _start = datetime.strptime(_start, '%Y-%m-%d')
    #     # 만약 _end 타입이 문자라면
    #     if type(_end) == 'str':
    #         _end = datetime.strptime(_start, '%y-%m-%d')
    # except:
    #     print('시간 포맷이 맞지 않습니다, (YYYY-mm-dd)')
    #     return
    
    # Date가 컬럼에 존재한다면 Date를 인덱스로 변경
    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)

    # 인덱스 -> 시계열데이터로 변경
    df.index = pd.to_datetime(df.index)
    
    # 결측치, 양의 무한대, 음의 무한대 제거
    flag = df.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
    df = df.loc[~flag, ]
    
    try: 
       df = df.loc[_start : _end, [_col]]
    except Exception as e:
        print(e)
        print('인자값이 잘못되었습니다')
        return ""
    
    # 일별 수익률 컬럼 생성
    df['rtn'] = (df[_col].pct_change() + 1).fillna(1)
    # 누적 수익률 컬럼 생성
    df['acc_rtn'] = df['rtn'].cumprod()
    # 최종 누적 수익률
    final_acc_rtn = df.iloc[-1, -1]

    # 결과 데이터프레임과 최종 누적수익률 반환
    return df, final_acc_rtn