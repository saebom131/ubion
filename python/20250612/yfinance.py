import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ticker 입력하는 부분
ticker = input('ticker를 입력하시오: ')

# 웹 브라우저 오픈
driver = webdriver.Chrome()

time.sleep(1)

# 야후파이낸스 접속
driver.get('https://finance.yahoo.com')

time.sleep(2)

# # 웹 브라우저 전체화면 모드
# driver.fullscreen_window()

# 상단 검색어창 선택
element = driver.find_element(By.ID, 'ybar-sbq')
# 검색어창에 ticker 입력
element.send_keys(ticker)

# 검색어창에 키보드의 특수 이벤트 (ENTER) 입력
element.send_keys(Keys.ENTER)

time.sleep(2)

# elements : 검색한 결과 페이지의 좌측 사이드바의 메뉴를 모두 선택
elements = driver.find_elements(By.CSS_SELECTOR, '.item.yf-x2pyjv')

# 좌측 사이드바 메뉴 중 2번째 메뉴(News) 클릭
elements[1].click()

time.sleep(2)

soup = bs(driver.page_source, 'html.parser')

# 웹 브라우저 종료
driver.close()

ul_data = soup.find(
    'ul', attrs={
        'class' : 'stream-items yf-1drgw5l'
    }
)

# 기사 목록의 url 불러오기
a_list = ul_data.find_all('a')
_list = []
for i in a_list:
    href = i['href']
    if href not in _list and href.startswith('https://finance'):
        _list.append(href)

# 기사 목록의 헤드라인은 h3태그
h3_list = ul_data.find_all('h3')
headline = []
for h3_data in h3_list:
    headline.append(h3_data.get_text())

df = pd.DataFrame(
    {
        'headline': headline,
        'url': _list
    }
)

df.to_csv(f'./data/{ticker}_news.csv', index=False)