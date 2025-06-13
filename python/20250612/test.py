# 유저에게 주식 종목코드를 입력 받아 종목코드에 해당하는 주식이름, 종합정보를 가져와 csv 파일로 저장하는 모듈

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

codes = []      
# 유저가 입력한 종목코드를 codes에 추가
while True:
    # 유저가 값을 입력하고 그 값을 변수에 저장
    code = input('조회할 종목코드를 입력하시오(0 입력시 코드 추가 종료, 최대 10개) :  ')
    if code == '0' or len(codes) > 10: 
        break
    codes.append(code)

for code in codes:
    base_url = 'https://finance.naver.com/item/main.naver?code='
    res = requests.get(
        base_url + code
    )
    # 응답 데이터를 문자형으로 받아 BeautifulSoup class로 파싱
    soup = bs(res.text, 'html.parser')
    # 파일 이름으로 사용할 종목명 추출
    # div 태그 중 class가 h_company인 태그 선택
    div_data = soup.find(
        'div', attrs={
            'class' : 'h_company'
        }
    )

    # 존재하지 않는 종목코드인 경우 반복문으로 되돌아감(리스트의 다음 종목코드번호로)
    try: 
        # div_data에서 h2 태그를 선택해 문자 추출
        company_name = div_data.find('h2').get_text().rstrip()
    except:
        print(f'{code}는 없는 종목코드입니다.')
        continue

    # 종합정보 데이터 추출
    # soup에서 div 중 class가 invest_trend인 태그 선택
    invest_data = soup.find(
        'div', attrs={
            'class' : 'invest_trend'
        }
    )
    dfs = pd.read_html(str(invest_data))

    # 결측치가 포함된 행 제거
    trade_info = dfs[0].dropna(axis=0).reset_index(drop=True)
    fori_org = dfs[1].dropna(axis=0).reset_index(drop=True)

    trade_info.to_csv(f'data/{company_name}_거래원정보.csv', index=False)
    fori_org.to_csv(f'data/{company_name}_외국인,기관.csv', index=False)    # encoding='cp949'로 변경시 엑셀파일 한글깨짐X