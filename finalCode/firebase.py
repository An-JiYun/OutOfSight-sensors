import firebase_admin
from firebase_admin import credentials, firestore
import os
import time

# Firebase 초기화
cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred)

# Firestore 인스턴스 초기화
db = firestore.client()

# 파일 경로
vibration_file = "/home/rpi/Documents/sensors/text/vibration_data.txt"
pressure_file = "/home/rpi/Documents/sensors/text/pressure_data.txt"
gps_file = "/home/rpi/Documents/sensors/text/gps_data.txt"

# 이전 GPS 데이터 저장 변수 초기화
prev_gps_data = None

def file_exists(file_path):
    #파일 존재 여부 확인 및 값 반환
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read().strip()
        os.remove(file_path)  # 데이터 읽은 후 파일 삭제
        return data
    return False


def read_gps_data():
    #GPS 파일에서 데이터 읽기 또는 이전 값 사용
    global prev_gps_data
    if os.path.exists(gps_file):
        with open(gps_file, "r") as file:
            lat, lng = file.read().strip().split()
        prev_gps_data = (float(lat), float(lng))
        os.remove(gps_file)
        return prev_gps_data, True
    return prev_gps_data, False


def send_data_to_firebase(vibration, pressure, gps_data, gps_signal):
    #파이어베이스에 데이터 전송
    gps_lat, gps_lng = gps_data if gps_data else (-1, -1)
    doc_ref = db.collection('vehicle').document('1234-ID').collection('Notifications').document()
    data = {
        'geopoint': firestore.GeoPoint(gps_lat, gps_lng),
        'signal': {
            'gps': gps_signal,
            'pressure': pressure,
            'vibration': vibration
        },
        'time': firestore.SERVER_TIMESTAMP  # 현재 시간
    }
    doc_ref.set(data)
    print("Sensor data sent to Firebase.")
    

if __name__ == "__main__":
    while True:
        # 센서 데이터 파일에서 데이터 읽기 및 존재 여부 확인
        vibration = file_exists(vibration_file) == "true"
        pressure = file_exists(pressure_file) == "true"
        gps_data, gps_signal = read_gps_data()
        
        # 모든 데이터를 파이어베이스에 전송
        send_data_to_firebase(vibration, pressure, gps_data, gps_signal)
        
        time.sleep(5)  # 데이터 확인 주기
