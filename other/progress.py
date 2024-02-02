import subprocess

# 첫 번째 파일 실행
subprocess.Popen(["sudo", "python3", "vibrationTest.py"])

# 두 번째 파일 실행
subprocess.Popen(["python3", "firebase.py"])