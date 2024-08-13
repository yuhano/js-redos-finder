from pathlib import Path
import csv
import os
from constants import *

def save_results_to_csv(results, output_csv):
    """Save the results to a CSV file.
    결과를 CSV 파일로 저장합니다."""
    
    output_dir = os.path.dirname(output_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fieldnames = ['file_path', 'line_number', 'found_regex', 'Status', 'Complexity', 'Attack string', 'Checker', 'JS REGEX CHECKER', 'JS Test Time']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def should_exclude(path, excluded_names, excluded_keywords):
    """Check if a path should be excluded based on excluded folder names or keywords.
    제외된 폴더 이름 또는 키워드를 기반으로 경로를 제외할지 확인합니다."""
    if any(part in excluded_names for part in path.parts):  # Check if any part of the path matches excluded folder names (경로의 일부가 제외된 폴더 이름과 일치하는지 확인)
        return True
    if any(keyword in path.name for keyword in excluded_keywords):  # Check if any keyword is in the file/folder name (파일/폴더 이름에 키워드가 포함되어 있는지 확인)
        return True
    return False
