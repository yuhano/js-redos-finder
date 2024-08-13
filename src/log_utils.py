from datetime import datetime
import os
import time
from datetime import datetime
from constants import *


def initialize_log_file(log_file, start_time, directories):
    """Initialize the log file by clearing existing content and adding header information
    기존 내용을 모두 지우고 헤더 정보를 추가하여 로그 파일 초기화"""

    # Ensure the directory for the log file exists (로그 파일을 위한 디렉토리가 존재하는지 확인)
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"Start time: {start_time}")
        log.write("Directories to scan:\n")
        for idx, directory in enumerate(directories, start=1):
            log.write(f"  [{idx}/{len(directories)}] {directory.name}\n")
        log.write("\n")

def log_exclusion(log_file, exclusion_type, exclusion_path):
    """Log excluded folders or files with full paths.
    제외된 폴더 또는 파일의 전체 경로를 기록합니다."""
    if LOG_EXCLUSIONS:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"[Excluded] {exclusion_type}: {exclusion_path}\n")

def log_progress(log_file, dir_idx, total_dirs, file_counter, files_to_check, file_time_taken, directory_name, file_path):
    """Log progress in the log file.
    진행 상황을 로그 파일에 기록합니다."""
    if SHOW_ZERO_SECOND_LOGS or int(file_time_taken) > 0:
        log_message = f"           [{file_counter}/{files_to_check}] Time taken: {int(file_time_taken)}s | File path: {file_path}"
        with open(log_file, 'a', encoding='utf-8') as log:
            if file_counter == 1:  # If it's the first file in the directory, add the directory header (디렉토리의 첫 번째 파일이면 디렉토리 헤더 추가)
                dir_message = f"[{dir_idx}/{total_dirs}] {directory_name}"
                log.write(dir_message + '\n')
            log.write(log_message + '\n')
    elif file_counter == 1:
        with open(log_file, 'a', encoding='utf-8') as log:
            dir_message = f"[{dir_idx}/{total_dirs}] {directory_name}"
            log.write(dir_message + '\n')

def log_folder_summary(log_file, directory_name, dir_time_taken):
    """Log the summary for each folder.
    각 폴더에 대한 요약을 로그에 기록합니다."""
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"[{directory_name}] Folder processing time: {int(dir_time_taken)}s\n\n")

def log_total_summary(log_file, total_time_taken):
    """Log the total summary for all folders.
    모든 폴더에 대한 전체 요약을 로그에 기록합니다."""
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"\nTotal processing time: {int(total_time_taken)}s\n")

def log_end_time(log_file, end_time):
    """Log the end time when the process is completed.
    프로세스가 완료되었을 때 종료 시간을 로그에 기록합니다."""
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"End time: {end_time}\n")

