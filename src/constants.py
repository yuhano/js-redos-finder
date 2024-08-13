import re
import os

# Constants and Configuration
# 상수 및 설정
SOURCE_EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.mjs']
REGEX_PATTERN = re.compile(r'\/.*?\/[gimsuy]*')  # Regular expression pattern for JavaScript regex (JavaScript 정규식 패턴)

# Set paths using absolute paths for Windows compatibility
# Windows 호환성을 위한 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로를 기준으로 베이스 디렉토리 설정
OUTPUT_CSV = os.path.join(BASE_DIR, '..', 'output', 'regex_search_results_output.csv')
LOG_FILE = os.path.join(BASE_DIR, '..', 'logs', 'result.log')
PROGRAM_PATH = os.path.join(BASE_DIR, '..', 'scripts', 'recheck-windows-x64.exe')

SHOW_ZERO_SECOND_LOGS = False  # Set to False to hide logs with 0 seconds (0초 로그를 숨기려면 False로 설정)
INCLUDE_FALSE_RESULTS = False  # Set to False to exclude rows with JS REGEX CHECKER as false (JS 정규식 검사기가 false인 행을 제외하려면 False로 설정)
NUM_WORKERS = 4  # Number of parallel workers (threads) (병렬 작업자 수 (스레드))
EXCLUDED_FOLDER_NAMES = ['node_modules', 'dist', 'build', 'packages']  # Folders to exclude (제외할 폴더 이름 목록)
EXCLUDED_FILES = []  # Files to exclude (제외할 파일 목록)
EXCLUDED_KEYWORDS = ['test', 'mock', 'example']  # Keywords to exclude (제외할 키워드 목록)
LOG_EXCLUSIONS = True  # Set to True to log excluded files/folders (제외된 파일/폴더를 로그로 기록하려면 True로 설정)

# Root directory to search for files (파일을 검색할 루트 디렉토리)
ROOT_DIRECTORY = os.path.join(BASE_DIR, '..', 'colord')  
