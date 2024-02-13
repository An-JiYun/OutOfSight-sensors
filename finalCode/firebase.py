import RPi.GPIO as GPIO
import spidev
import time
import serial
import pynmea2
import os
import json
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import threading

# Firebase 초기화
cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
initialize_app(cred)
db = firestore.client()

# 센서 파일 경로
vibration_file = "/home/rpi/Documents/sensors/text/vibration_data.txt"
pressure_file = "/home/rpi/Documents/sensors/text/pressure_data.txt"
gps_file = "/home/rpi/Documents/sensors/text/gps_data.txt"

# 이전 GPS 데이터 저장 변수 초기화
prev_gps_data = (0, 0)

def read_and_send_data():
    vibration = file_exists(vibration_file)
    pressure = file_exists(pressure_file)
    gps_data, gps_signal = read_gps_data()

    # 값이 변한, 세 값 중 하나만 True인 경우에만 Firebase에 데이터 전송
    if vibration or pressure or gps_signal:
        send_data_to_firebase(vibration, pressure, gps_data, gps_signal)



def file_exists(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read().strip()
        os.remove(file_path)
        return True if data == "true" else False
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
    # gps_signal이 False일 때도 prev_gps_data 사용
    gps_lat, gps_lng = gps_data if gps_signal else prev_gps_data
    # Firestore의 GeoPoint 생성을 위해 gps_lat, gps_lng 사용
    geopoint = firestore.GeoPoint(gps_lat, gps_lng)

    data = {
        'isChecked': False,
        'geopoint': geopoint,
        'signal': {
            'gps': gps_signal,
            'pressure': pressure,
            'vibration': vibration,
            'stranger': False
        },
        'time': firestore.SERVER_TIMESTAMP,
        'video' : ""
    }

    doc_ref = db.collection('Vehicles').document('1234-ID').collection('Notifications').document()
    doc_ref.set(data)
    print("Sensor data sent to Firebase.")

def sensor_monitor():
    while True:
        read_and_send_data()
        time.sleep(3)

sensor_thread = threading.Thread(target=sensor_monitor)
sensor_thread.start()
