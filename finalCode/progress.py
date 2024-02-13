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
    print("프로그램 종료 중...")
    for p in processes:
        try:
            p.terminate()  # 각 자식 프로세스를 종료 시도
            p.wait(timeout=2)  # 프로세스 종료를 최대 2초간 기다림
        except Exception as e:
            print(f"프로세스 종료 대기 중 오류 발생: {e}")
            p.kill()  # 종료 실패 시 강제 종료
            p.wait()  # 강제 종료 후 종료 완료 대기
    print("모든 프로세스가 종료되었습니다.")
    exit(0)

if __name__ == "__main__":
    # Ctrl+C 시그널에 대한 핸들러 설정
    signal.signal(signal.SIGINT, signal_handler)

    # 실행할 스크립트 리스트 및 sudo 사용 여부
    scripts = [
        #("vibration.py", True),  # sudo 권한이 필요함
        #("pressure.py", False),
        ("firebase.py", False),
        ("gps.py", False)
    ]
    
    try:
        for script, use_sudo in scripts:
            run_script(script, use_sudo)
            time.sleep(0.5)  # 스크립트 실행 사이에 간단한 대기 시간

    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        signal_handler(None, None)  # 예외 발생 시 모든 프로세스를 종료
        for p in processes:
          p.terminate()
          p.wait()
        
    