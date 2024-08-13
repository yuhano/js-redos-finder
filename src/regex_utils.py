import subprocess
import threading
import time
from constants import *

def parse_recheck_output(output):
    """Parse the output from the external regex checker into a dictionary.
    외부 정규식 검사기의 출력을 사전으로 분석합니다."""
    output_data = {}
    for line in output.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            output_data[key.strip()] = value.strip()
    return output_data

def run_recheck(program_path, regex):
    """Run the external program to check the regex.
    정규식을 검사하기 위해 외부 프로그램을 실행합니다."""
    command = f'"{program_path}" "{regex}"'
    if len(command) > 260:  # Avoid WinError 206 due to long command length (명령어 길이로 인한 WinError 206 방지)
        raise ValueError("Command too long")
    
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    if result.stderr:
        return {}  # Return an empty result if there's an error (오류가 있는 경우 빈 결과 반환)
    
    return parse_recheck_output(result.stdout)

def run_js_with_timeout(script, timeout):
    """Run a JavaScript code snippet with a timeout.
    타임아웃과 함께 JavaScript 코드 스니펫을 실행합니다."""
    process = subprocess.Popen(['node', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = threading.Timer(timeout, process.kill)
    try:
        timer.start()
        stdout, stderr = process.communicate()
        if timer.is_alive():
            if stderr:
                print("Error:", stderr.decode())
            return stdout.decode()
        else:
            print("Timeout occurred")
            return "Regex test result: true\nProcessing time: TIMEOUT"
    finally:
        timer.cancel()

def generate_js_code(argument_0, argument_1):
    """Generate JavaScript code for testing a regex.
    정규식을 테스트하기 위한 JavaScript 코드를 생성합니다."""
    js_code = f"""
    const protocolre = {argument_0};
    const startTime = Date.now();

    const maliciousInput = {argument_1};

    const result = protocolre.test(maliciousInput);

    const endTime = Date.now();

    console.log("Regex test result: ", result);
    console.log("Processing time: ", endTime - startTime, "ms");
    """
    return js_code

def parse_js_test_output(js_output):
    """Parse the JS Test Output to extract the result and time.
    JS 테스트 출력을 분석하여 결과와 시간을 추출합니다."""
    result = None
    time_taken = None
    for line in js_output.splitlines():
        if "Regex test result: " in line:
            result = line.split(": ")[1].strip()
        if "Processing time: " in line:
            time_taken = line.split(": ")[1].strip().replace("ms", "").strip()
    return result, time_taken
