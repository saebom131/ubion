import os
from glob import glob
import pandas as pd

# encoding 기본값 없이 조건문 내에 try ~ except문 작성

def dir_load_vari(file_path, file_tail='*.*', engine='cp949'):
    file_path = file_path + '/'
    # 만약 file_tail이 '*.*'이 아니라면 file_tail 앞에 '*.' 추가
    # file_tail -> csv라면 => '*.' + file_tail -> *.csv
    if file_tail != '*.*':
        file_tail = '*.' + file_tail

    # glob()를 이용하여 파일 목록 로드
    file_list = glob(file_path + file_tail)

    # 반복문 반복 횟수 체크 위해 숫자 0을 변수에 저장
    cnt = 0

    for file in file_list:
        # file을 경로 / 파일명 으로 나눔
        path, name = os.path.split(file)    # name = os.path.split(file)[1]
        # name을 이름 / 확장자로 나눔
        head, tail = os.path.splitext(name)
        
        # tail에 따라 read_함수를 지정
        if tail == '.csv':
            # 기본값 utf-8로 먼저 인코딩
            try:
                df = pd.read_csv(file)
            # 오류 발생 시 cp949로 인코딩
            except:
                df = pd.read_csv(file, encoding=engine)
        elif tail == '.tsv':
            try:
                df = pd.read_csv(file, sep='\t')
            except:
                df = pd.read_csv(file, encoding=engine)
        elif tail == '.json':
            try:
                df = pd.read_json(file)
            except:
                df = pd.read_json(file, encoding=engine)
        elif tail == '.xml':
            try:
                df = pd.read_xml(file)
            except:
                df = pd.read_xml(file, encoding=engine)
        elif tail in ['.xlsx', '.xls']:
            try:
                df = pd.read_excel(file)
            except:
                df = pd.read_excel(file)

        try:
            # head를 이용해 전역변수 생성하고, df의 복사본 대입
            globals()[head] = df.copy()
            # 전역변수 생성 -> cnt 1 증가
            cnt += 1
            # 전역변수 생성되면 print() 이용해 출력
            print(f'{cnt}번째 전역변수 생성: {head}')
        except:
            print(f'{tail} 확장자는 지원하지 않음')
    # 함수를 종료하기 위해 전역변수가 생성된 횟수인 cnt 반환
    return cnt      # 생성된 전역변수 개수

# 특정 경로에 존재하는 데이터 파일을 로드하여 하나의 데이터프레임으로 생성해주는 함수
# 매개변수 2개 -> 파일의 경로, 파일 확장자, 인코딩엔진(기본값: utf-8)
def dir_load_df(file_path, file_tail, engine = 'utf-8'):
    # file_path의 마지막에 '/' 없으면 에러 발생 -> '/' 임의로 추가
    file_path = file_path + '/'
    # 인자로 전달받은 file_path를 기준으로 파일 목록 생성
    file_list = os.listdir(file_path)
    file_list.sort()

    result = pd.DataFrame()

    # 확장자가 file_path인 파일만 따로 리스트에 저장
    new_list = []
    for file in file_list:
        # 조건: 확장자가 file_tail과 같다면
        # 확장자 확인 방법: 문자열에서 마지막의 문자와 같은가?
        # endswith()
        if file.endswith(file_tail):
            new_list.append(file)

    for file2 in new_list:
        # file_tail에 따라 read 함수 변경
        if file_tail == 'csv':
            df = pd.read_csv(file_path + file2, encoding=engine)
        elif file_tail == 'json':
            df = pd.read_json(file_path + file2, encoding=engine)
        elif file_tail == 'xml':
            df = pd.read_xml(file_path + file2, encoding=engine)
        # elif (file_tail == 'xlsx') | (file_tail == 'xls'):
        elif file_tail in ['xlsx', 'xls']:
            df = pd.read_excel(file_path + file2)       # 엑셀은 인코딩 엔진 없음
        else:
            print('확장자명 잘못 입력(csv, json, xml, excel 사용 가능)')
            return ""
        
        # result에 누적 행 결합
        result = pd.concat([result, df])
        print(f'{file2} 데이터 행결합 완료')    # 각 파일 정상 로드 확인
    # 인덱스 초기화, 기존 인덱스 제거
    result.reset_index(drop=True, inplace=True)
    
    return result

# dir_load_vari() 함수와 dir_load_df() 함수를 호출하는 새로운 함수 생성
# 매개변수 -> dir_load_xxx() 함수에서 사용되는 매개변수의 값들 모두 생성
# 둘 중에 어떤 함수를 호출할지 지정하는 매개변수 하나 필요

def dir_load(file_path, file_tail='*.*', engine='utf-8', selected = 0):
    if selected == 0:
        result = dir_load_vari(file_path, file_tail, engine)
    else:
        if file_tail == '*.*':
            file_tail = 'csv'
        result = dir_load_df(file_path, file_tail, engine)
    return result

# 모듈 테스트용 조건문
if __name__ == "__main__":
    # 해당 py파일을 직접 실행했을때만 print문 실행
        # 1. code runner를 이용해 run code 실행할 때
        # 2. cmd에서 python 파일명으로 실행할 때
    print(dir_load(r'C:\ubion\csv\num_3'))     # 반복횟수 : 5
    print(dir_load(r'C:\ubion\csv\2021', selected=1))     # 결합된 데이터프레임