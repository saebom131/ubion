import pandas as pd
import numpy as np
from datetime import datetime

def create_YM(_df, _col = 'Adj Close'):
	# 데이터프레임 복사본 생성
	df = _df.copy()

	# 'Date'가 컬럼에 존재한다면 index로 변경
	if 'Date' in df.columns:
		df.set_index('Date', inplace=True)

	# 인덱스를 시계열로 변경
	df.index = pd.to_datetime(df.index)
    
	# 결측치, 무한대 값 제거
	flag = df.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
	df = df.loc[-flag, ]

	# 기준 컬럼을 제외하고 나머지 제거
	df = df[[_col]]
    
	# df에 STD-YM 컬럼 생성하여 인덱스에서 년도-월 데이터 추출하여 대입
	df['STD-YM'] = df.index.strftime('%Y-%m')

	return df		
def create_last_month(
		_df, 
		_start = '2010-01-01', 
		_end = datetime.now(), 
		_momentum = 12):
		
	# 기준이 되는 컬럼 이름을 변수에 저장
	col = _df.columns[0]

	# 월말의 데이터만 모아 생성할 새로운 데이터프레임
	# 월말의 기준 : STD-YM의 현재와 다음행 데이터가 다른 경우
	flag = _df['STD-YM'] != _df.shift(-1)['STD-YM']
	df = _df.loc[flag, ]

	# 전월의 데이터 생성
	df['BF1'] = df.shift(1)[col].fillna(0)
	# _momentum 개월 전의 데이터 생성
	df['BF2'] = df.shift(_momentum)[col].fillna(0)
	
	df = df.loc[_start : _end, ]
	
	return df
def create_rtn(
		_df1, _df2, 
		_start = '2010-01-01',
		_end = datetime.now(),
		_score = 1):
	# 데이터프레임 복사본 생성
	df = _df1.copy()
	df = df.loc[_start : _end, ]

	# trade, rtn 컬럼 생성
	df['trade'] = ''
	df['rtn'] = 1
	
	# 거래내역 추가
	# _df2(create_last_month())를 이용해 momentum_index를 구함
	for idx in _df2.index:
		signal= ''

		# 절대 모멘텀 인덱스 계산
		momentum_index = \
			(_df2.loc[idx, 'BF1'] / _df2.loc[idx, 'BF2']) - _score

		# 모멘텀 인덱스가 0보다 크고 무한대가 아닌 경우
		flag = (momentum_index > 0) & (momentum_index != np.inf)
		
		# 조건(flag)이 참이라면
		if flag:
			signal = 'buy'
		# print(f'날짜: {idx}, 모멘텀인덱스: {momentum_index}, signal: {signal}')
		# df에 구매내역 추가
		df.loc[idx: , 'trade'] = signal
	
	# 기준이 되는 컬럼 이름을 변수에 저장
	col = df.columns[0]

	# 수익률 계산
	for idx in df.index:
		# 매수의 조건식: 전날의 trade가 ''이고, 오늘의 trade가 'buy'라면
		if (df.shift().loc[idx, 'trade'] == '') & (df.loc[idx, 'trade'] == 'buy'):
			buy = df.loc[idx, col]		# 구매가는 해당 날짜의 수정종가(Adj Close)
			print(f'매수일: {idx}, 매수가: {buy}')
		# 매도의 조건식: 전날의 trade가 'buy'이고, 오늘의 trade가 ''라면
		elif (df.shift().loc[idx, 'trade'] == 'buy') & (df.loc[idx, 'trade'] == ''):
			sell = df.loc[idx, col]		# 매도가는 해당 날짜의 수정종가(Adj Close)
			rtn = sell / buy
			df.loc[idx, 'rtn'] = rtn
			print(f'매도일: {idx}, 매도가: {sell}, 수익률: {rtn}')
	# 누적곱(누적수익률)
	df['acc_rtn'] = df['rtn'].cumprod()
	acc_rtn = df.iloc[-1, -1]	

	return df, acc_rtn
