import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def six_month(
        _df,
        _start = '2010-01-01',
        _end = datetime.now(),
        _col = 'Adj Close',
        _month = 11
):
	# 복사본 생성
	df = _df.copy()
	# Date 컬럼이 존재한다면 인덱스로 변경
	if 'Date' in df.columns:
		df.set_index('Date', inplace=True)
    # index를 시계열 데이터로 변경
	df.index = pd.to_datetime(df.index)
	# 시작 시간을 시계열로 변경
	start = pd.to_datetime(_start)
	# 종료 시간은 타입이 문자라면 시계열로 변경
	if type(_end) == str:
		end = pd.to_datetime(_end)
	else:
		end = _end

	# 빈 데이터프레임 생성
	result = pd.DataFrame()

	for year in range(start.year, end.year):
		# 매수 시간
		buy = datetime(year = year, month = _month, day = 1)
		# 매도 시간 (매수 5개월 뒤)
		sell = buy + relativedelta(months=5)
		
		buy_mon = buy.strftime('%Y-%m')
		sell_mon = sell.strftime('%Y-%m')

		try:
			start_df = df.loc[buy_mon, [_col]].head(1)
			end_df = df.loc[sell_mon, [_col]].tail(1)
			result = pd.concat(
				[result, start_df, end_df], axis=0
			)
		except:
			break
		
	# result를 이용해 수익률 계산
	result['rtn'] = 1
	for idx in range(1, len(result), 2):
		rtn = result.iloc[idx, ][_col] / result.iloc[idx-1, ][_col]
		result.iloc[idx, -1] = rtn
	# 누적수익률 계산
	result['acc_rtn'] = result['rtn'].cumprod()
	acc_rtn = result.iloc[-1, -1]

	return result, acc_rtn