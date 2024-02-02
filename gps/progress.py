import subprocess

# 압력센서 읽고 firebase에 보내기
subprocess.Popen(["python3", "FSRTest4.py"])

# gps 위치 읽고 firebase에 보내기
subprocess.Popen(["python3", "gps.py"])


# 진동 센서 읽기
subprocess.Popen(["sudo", "python3", "vibrationTest.py"])

# 진동센서 값 보내기
subprocess.Popen(["python3", "firebase.py"])