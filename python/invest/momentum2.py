import pandas as pd
import os
from glob import glob
from datetime import datetime

# 기준 년월 컬럼과 월별 수익률 컬럼을 생성하는 함수
# 매개변수 5개
	# 데이터프레임
	# ticker
	# 투자의 시작시간
	# 투자의 종료시간
	# 기준이 되는 컬럼
def create_1m_rtn(_df, _ticker, _start = '2010-01-01', _end = datetime.now(), _col = 'Adj Close'):
	
	# 복사본 생성
	df = _df.copy()
	# 'Date'가 컬럼에 존재하면 인덱스로 변환
	if 'Date' in df.columns:
		df.set_index('Date', inplace=True)
	# 인덱스를 시계열로 변환
	df.index = pd.to_datetime(df.index)
	
	# 투자의 시작시간과 종료시간으로 인덱스 필터링
	# 기준이 되는 컬럼으로 컬럼 필터링
	df = df.loc[_start : _end, [_col]]
	# 기준년월 컬럼 생성해 인덱스에서 년도-월 추출
	df['STD-YM'] = df.index.strftime('%Y-%m')
	# 월별 수익률 컬럼 생성
	df['1m_rtn'] = 0
	# ticker를 컬럼에 대입
	df['CODE'] = _ticker
	# 기준년월의 유니크값 생성
	ym_list = df['STD-YM'].unique()
	
	return df, ym_list

# 데이터를 로드하고 월별 수익률 계산하여 새로운 데이터프레임에 추가하는 함수
def data_load(
		_path = './data',
		_ext = 'csv',
		_start = '2010-01-01',
		_end = datetime.now(),
		_col = 'Adj Close'
):
	files = glob(f'{_path}/*.{_ext}')
	
    # 비어있는 데이터프레임 생성
	stock_df = pd.DataFrame()
	month_last_df = pd.DataFrame()

    # files를 이용해 반복문 생성
	for file in files:
        # file: 특정 경로와 파일명
        # print(file)
        # 경로와 파일명을 나눠준다 -> os.path.split 사용
		folder, name = os.path.split(file)
        # 파일명에서 이름과 확장자로 나눠줌
		head, tail = os.path.splitext(name)
        # head는 create_1m_rtn에서 _ticker 매개변수에 넣어줄 인자값
        
        # 데이터프레임 로드
		read_df = pd.read_csv(file)
        # create_1m_rtn() 함수 호출
		price_df, ym_list = create_1m_rtn(read_df, head, _start, _end, _col)
        # price_df를 stock_df에 단순 행결합
		stock_df = pd.concat([stock_df, price_df], axis=0)
        
        # 두번째 반복문 생성
        # 월별 수익률을 계산하여 대입
		for ym in ym_list:
            # ym : 기준년월
            # 월초의 가격(매수)
			buy = price_df.loc[ym, ].iloc[0, 0]
            # 월말의 가격(매도)
			sell = price_df.loc[ym, ].iloc[-1, 0]
            # 수익률 생성
			rtn = sell / buy
            # 수익률 대입
			price_df.loc[ym, '1m_rtn'] = rtn
            # 월말의 데이터를 month_last_df에 단순 행결합
			last_df = price_df.loc[ym, ['CODE', '1m_rtn']].tail(1)
			month_last_df = pd.concat([month_last_df, last_df], axis=0)
			
	return stock_df, month_last_df


def create_position(
		_df,
		_pct = 0.4
):
	# 복사본 생성
	month_rtn_df = _df.copy()
	# _pct의 1보다 크거나 같은 숫자라면 100으로 나눠준다
	if _pct >= 1:
		_pct /= 100
	
    # 인덱스 리셋
	month_rtn_df.reset_index(inplace=True)
    # 테이블을 재구조화
	month_rtn_df = month_rtn_df.pivot_table(
        index = 'Date',
    columns = 'CODE',
    values = '1m_rtn'
    )

    # month_rtn_df의 데이터들을 랭크화(열의 값들을 이용)
	month_rtn_df = month_rtn_df.rank(
        axis=1, 
        ascending=False,
        pct=True		# 순위를 백분율로 변환 (상위 ~%)
    )
    # 상위의 40% 종목 선택
    # where() 함수 사용
        # where (조건식, 거짓일 때 대입된 데이터)
    # 0.4 보다 낮은 데이터만 남기고 나머지는 0으로 변경
	month_rtn_df = month_rtn_df.where( month_rtn_df <= _pct, 0)

    # 0이 아닌 데이터들은 1로 변환
	month_rtn_df[month_rtn_df != 0] = 1

    # stock_df의 CODE의 unique()를 변수에 저장
	stock_codes = list(month_rtn_df.columns)
	
    # 해당 일자의 구매하려는 종목들을 딕셔너리 생성
	sig_dict = dict()
	
	for idx in month_rtn_df.index:
        # idx : month_rtn_df의 인덱스들 (시계열)
		flag_col = month_rtn_df.loc[idx, ] == 1
		ticker_list = list(
			month_rtn_df.loc[idx, flag_col].index
		)
        # sig_dict에 추가
		sig_dict[idx] = ticker_list
		
	return sig_dict, stock_codes

# 구매 내역을 추가하는 함수
# 거래내역 컬럼을 추가하는 함수 생성
def create_trade_book(_df, _codes, _sig_dict):
    # 복사본 생성
    df = _df.copy()
	# stock_df를 재구조화
    df = df.reset_index().pivot_table(
        index = 'Date',
        columns = 'CODE',
        values = df.columns[0]
    )
	
    for code in _codes:
        df[f'p_{code}'] = ''	# 구매
        df[f'r_{code}'] = ''	# 수익률
    
    # sig_dict를 이용해 구매 전 준비내역 추가
    for date, codes in _sig_dict.items():
        # date : key -> 시계열 데이터(말일 데이터)
        # codes : value -> 종목 리스트
        # codes 반복문 생성
        for code in codes:
            # print(code)
            # book에서 인덱스가 date인 컬럼이 r_code인 컬럼에 준비 내역을 추가
            df.loc[date, f'p_{code}'] = f'ready_{code}'
    return df

# 보유 내역을 추가하는 함수 생성
def create_trading(_df, _codes):
    buy_phase = False
    df = _df.copy()
    std_ym = ''
    
	# _codes: 종목 리스트 -> 컬럼명
    # 종목별로 순회(컬럼)하는 반복문 생성
    for code in _codes:		# 10번 반복
        # 인덱스를 기준으로 반복문 생성
        for idx in df.index:
            # 특정 종목의 포지션을 잡는다 
			# 현재 행의 p_code 컬럼이 ''이고
			# 전행의 p_code 컬럼이 ready인 상태
            if (df.loc[idx, f'p_{code}'] == '') & (df.shift().loc[idx, f'p_{code}'] == f'ready_{code}'):
                std_ym = idx.strftime('%Y-%m')
                buy_phase = True
            # 구매 조건 : 현재 p_code가 ''이고, 
			# 			  index의 '년도-월'과 std_ym이 같고 
            # 			  buy_phase
            if (df.loc[idx, f'p_{code}'] == '') & \
                (std_ym == idx.strftime('%Y-%m')) & (buy_phase):
                df.loc[idx, f'p_{code}'] = f'buy_{code}'
            # buy_phase, std_ym 초기화
            if df.loc[idx, f'p_{code}'] == '':
                buy_phase = False
                std_ym = ''
    return df

# 수익률 계산 함수
def multi_return(_df, _codes):
    # 복사본 생성
    df = _df.copy()
    rtn = 1
    # 매수가 dict 형태로 구성
    buy_dict = dict()
    # 매도가 dict 형태로 구성
    sell_dict = dict()
    
	# index를 기준으로 반복문 생성 -> 날짜별 매수, 매도 확인
    for idx in df.index:
        # 종목별로 매수, 매도 확인
        for code in _codes:
            # 매수의 조건: 2행 전(shift(2))의 p_code가 ''이고,
            # 			   1행 전(shift())의 p_code가 'ready_code'이고,
            # 			   현재 행의 p_code가 'buy_code'인 상태
            if (df.shift(2).loc[idx, f'p_{code}'] == '') & \
				(df.shift().loc[idx, f'p_{code}'] == f'ready_{code}') & \
                (df.loc[idx, f'p_{code}'] == f'buy_{code}'):
                # 매수가 -> idx 행의 code 컬럼에 존재
                buy_dict[code] = df.loc[idx, code]
                print(f'매수일: {idx}, 매수 종목: {code}, 매수기: {df.loc[idx, code]}')
            # 매도의 조건: 1행 전의 p_code가 'buy_code'이고,
            # 			   현재 행의 p_code가 ''
            elif (df.shift().loc[idx, f'p_{code}'] == f'buy_{code}') & \
				 (df.loc[idx, f'p_{code}'] == ''):
                # 매도가 -> idx 행의 code 컬럼에 존재
                sell_dict[code] = df.loc[idx, code]
                # 수익률 계산
                rtn = sell_dict[code] / buy_dict[code]
                df.loc[idx, f'r_{code}'] = rtn
                print(f'매도일: {idx}, 매도 종목: {code}, 매도가: {sell_dict[code]}, 수익률: {rtn}')
            # buy_dict, sell_dict의 code 안에 매수가 매도가 초기화
            if df.loc[idx, f'p_{code}'] == '':
                buy_dict[code] = 0
                sell_dict[code] = 0
    return df

# 누적 수익률 계산
def multi_acc_rtn(_df, _codes):
    # 복사본 생성
    df = _df.copy()
    acc_rtn = 1
    
	# 인덱스를 기준으로 반복문 생성
    for idx in df.index:
        count = 0
        rtn = 0
        for code in _codes:
            # 수익률이 존재하는가?
            if df.loc[idx, f'r_{code}']:
                # 존재하는 경우
                count += 1
                rtn += df.loc[idx, f'r_{code}']
        if (rtn != 0) & (count != 0):
            acc_rtn *= rtn / count
            print(f'누적 - 매도일: {idx}, 매도 종목수: {count}, 수익률: {round(rtn/count, 2)}')
        df.loc[idx, 'acc_rtn'] = acc_rtn
        
    return df, acc_rtn        