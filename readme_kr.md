# js redos finder
* 이 프로젝트는 npm 패키지 내 ReDos 취약점을 자동으로 찾기 위한 프로젝트입니다. `recheck` 및 `nodejs` 에 종속되어져 있는 프로그램입니다.
* https://github.com/makenowjust-labs/recheck 프로그램을 기반으로 작성되었습니다.


## 주요 기능
* JavaScript 및 TypeScript 파일에서 정규식 패턴 추출
* 추출한 정규표현식(found_regex)을 `recheck` 이용해 공격 가능한 정규표현식(Attack string)을 생성 
* 추출한 정규표현식과 공격 정규표현식을 이용한 `nodeJS`의 실제 동작 시간 측정
* 검사 결과를 CSV 파일로 저장


## 프로젝트 구조
```
project_root/
│
├── input/                     #  분석할 파일들이 위치하는 폴더
│   ├── example npm folder 1
│   └── example npm folder 2
│
├── src/                       # 패키지 및 소스 코드가 위치하는 폴더
│   ├── __init__.py            # 패키지 초기화 파일
│   ├── constants.py           # 상수 및 설정 파일
│   ├── log_utils.py           # 로그 관련 유틸리티 함수 파일
│   ├── file_utils.py          # 파일 처리 관련 유틸리티 함수 파일
│   ├── regex_utils.py         # 정규식 검사 관련 유틸리티 함수 파일
│   └── main.py                # 메인 실행 스크립트
│
├── scripts/                   # 외부 정규식 검사기 프로그램 위치
│   └── recheck-windows-x64.exe
│
├── logs/                      # 로그 파일이 저장되는 폴더
│   └── (로그 파일들이 생성됩니다)
│
└── output/                    # 결과 CSV 파일이 저장되는 폴더
    └── regex_search_results_output.csv
```


## 설치 및 실행 방법
### 사전 요구 사항
* Python 3.x
* Node.js (JavaScript 코드 실행을 위해 필요)
* 윈도우

### 설치
1. 이 저장소를 클론합니다.
    ```
    git clone https://github.com/your-repository-url.git
    ```

2. 정규표현식을 검사할 패키지들을 `input` 폴더에 넣기 
    ```
    mkdir input
    cp [npmProject] input
    ```

3. src/constants.py 파일에서 ROOT_DIRECTORY와 PROGRAM_PATH 값을 적절하게 수정합니다.
아래 명령어를 실행하여 도구를 실행합니다.
    ```
    python src/main.py
    ```


# 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하십시오.

# 기여 방법
기여를 환영합니다! 버그 제보, 기능 요청 또는 풀 리퀘스트를 통해 기여할 수 있습니다.