import subprocess
import time
import signal

# 자식 프로세스 목록을 유지하기 위한 리스트
processes = []

def run_script(script_name, use_sudo=False):
    # sudo 권한이 필요한 경우와 그렇지 않은 경우를 구분하여 스크립트 실행
    if use_sudo:
        command = ["sudo", "python3", script_name]
    else:
        command = ["python3", script_name]
    process = subprocess.Popen(command)
    processes.append(process)
    

def signal_handler(sig, frame):
    # Ctrl+C (KeyboardInterrupt)를 처리하기 위한 핸들러
    print("프로그램 종료 중...")
    for p in processes:
        try:
            p.terminate()  # 각 자식 프로세스를 종료
        except Exception as e:
            print(f"프로세스 종료 중 오류 발생: {e}")
    for p in processes:
        p.wait()  # 각 프로세스가 종료될 때까지 기다림
    print("모든 프로세스가 종료되었습니다.")
    exit(0)


if __name__ == "__main__":
    # Ctrl+C 시그널에 대한 핸들러 설정
    signal.signal(signal.SIGINT, signal_handler)

    # 실행할 스크립트 리스트 및 sudo 사용 여부
    scripts = [
        ("vibrationTest.py", True),  # sudo 권한이 필요함
        ("FSRTest4.py", False),
        ("firebase.py", False),
        ("gps.py", False)
    ]
    
    try:
        for script, use_sudo in scripts:
            run_script(script, use_sudo)
            time.sleep(0.3)  # 스크립트 실행 사이에 간단한 대기 시간

    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        signal_handler(None, None)  # 예외 발생 시 모든 프로세스를 종료
        
    