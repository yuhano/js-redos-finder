import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

from constants import *
from log_utils import *
from file_utils import *
from regex_utils import *

def print_progress(total_dirs, dir_idx, directory_name, file_counter, files_to_check, found_count, file_path, file_time_taken=None, total_time_taken=None):
    """Print progress to the console."""
    overall_progress = (dir_idx / total_dirs) * 100
    file_progress = (file_counter / files_to_check) * 100
    
    # Clear the previous lines and print new progress
    print("\033[H\033[J", end="")  # Clear the terminal
    print(f"[Overall progress] {overall_progress:.2f}%")

    if total_time_taken is not None:
        hours, remainder = divmod(int(total_time_taken), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"[Total Running Time] {hours}h {minutes}m {seconds}s")
        
    print("\n[Detailed Progress]")
    print(f"[{dir_idx}/{total_dirs}] {directory_name}")
    print(f"    [{file_counter}/{files_to_check}: {file_progress:.2f}%] Currently processing file: {file_path}")
    
    if file_time_taken is not None:
        print(f"    File Processing Time: {int(file_time_taken)} seconds")


def process_file(file_path, program_path, results, files_to_check, file_counter, log_file, total_dirs, dir_idx, directory_name, total_start_time):
    """Process a single file, searching for regex patterns and checking them.
    단일 파일을 처리하여 정규식 패턴을 검색하고 검사합니다."""
    start_time = time.time()
    found_count = 0
    try:
        with file_path.open('r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, start=1):
                matches = REGEX_PATTERN.findall(line)
                for match in matches:
                    stripped_match = match.strip()

                    if ' ' in stripped_match or len(stripped_match) < 3:
                        continue
                    
                    try:
                        output_data = run_recheck(program_path, stripped_match)
                    except Exception:
                        continue
                    
                    if output_data.get('Status') in ['unknown', 'safe', 'error']:
                        continue
                    
                    if output_data.get('Checker'):
                        found_count += 1

                        # Generate and run the JavaScript code (JavaScript 코드 생성 및 실행)
                        attack_string = output_data.get('Attack string', "''")
                        js_code = generate_js_code(stripped_match, attack_string)
                        js_output = run_js_with_timeout(js_code, 30)
                        js_test_result, js_test_time = parse_js_test_output(js_output)

                        if INCLUDE_FALSE_RESULTS or js_test_result != 'false':
                            results.append({
                                'file_path': str(file_path),
                                'line_number': line_num,
                                'found_regex': stripped_match,
                                'Status': output_data.get('Status'),
                                'Complexity': output_data.get('Complexity'),
                                'Attack string': output_data.get('Attack string'),
                                'Checker': output_data.get('Checker'),
                                'JS REGEX CHECKER': js_test_result,
                                'JS Test Time': js_test_time
                            })
    except PermissionError:
        log_exclusion(log_file, "Permission denied", str(file_path))
        return
    except Exception as e:
        log_exclusion(log_file, f"Error ({e})", str(file_path))
        return

    file_time_taken = time.time() - start_time
    total_time_taken = time.time() - total_start_time  # Total running time을 갱신
    print_progress(total_dirs, dir_idx, directory_name, file_counter, files_to_check, found_count, file_path, file_time_taken, total_time_taken)
    log_progress(log_file, dir_idx, total_dirs, file_counter, files_to_check, file_time_taken, directory_name, file_path)


def find_and_check_regex_in_source_files(root_directory, program_path, output_csv, log_file):
    """Main function to find and check regex patterns in source files.
    소스 파일에서 정규식 패턴을 찾고 검사하는 메인 함수."""
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = []
    total_start_time = time.time()  # 전체 프로세스 시작 시간
    
    top_level_dirs = [d for d in Path(root_directory).iterdir() if d.is_dir()]
    total_dirs = len(top_level_dirs)

    initialize_log_file(log_file, start_time, top_level_dirs)

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for dir_idx, directory in enumerate(top_level_dirs, start=1):
            if should_exclude(directory, EXCLUDED_FOLDER_NAMES, EXCLUDED_KEYWORDS):
                log_exclusion(log_file, "Folder (폴더)", str(directory))
                continue

            dir_start_time = time.time()
            files = list(directory.rglob('*'))
            files_to_check = len([f for f in files if f.suffix in SOURCE_EXTENSIONS and not should_exclude(f, EXCLUDED_FILES, EXCLUDED_KEYWORDS)])

            file_counter = 1

            for file_path in files:
                if file_path.suffix in SOURCE_EXTENSIONS:
                    if should_exclude(file_path, EXCLUDED_FILES, EXCLUDED_KEYWORDS):
                        log_exclusion(log_file, "File (파일)", str(file_path))
                        continue

                    future = executor.submit(process_file, file_path, program_path, results, files_to_check, file_counter, log_file, total_dirs, dir_idx, directory.name, total_start_time)
                    futures.append(future)
                    file_counter += 1

            for future in as_completed(futures):
                future.result()

            dir_time_taken = time.time() - dir_start_time
            log_folder_summary(log_file, directory.name, dir_time_taken)

    total_time_taken = time.time() - total_start_time
    log_total_summary(log_file, total_time_taken)

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_end_time(log_file, end_time)

    print(f"Total processing time: {int(total_time_taken)}s (전체 처리 시간: {int(total_time_taken)}초)")
    save_results_to_csv(results, output_csv)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    find_and_check_regex_in_source_files(ROOT_DIRECTORY, PROGRAM_PATH, OUTPUT_CSV, LOG_FILE)
