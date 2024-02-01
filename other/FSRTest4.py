import RPi.GPIO as GPIO
import spidev
import time

import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred)

# Firestore 인스턴스 초기화
db = firestore.client()



# GPIO 핀 번호 설정
#pressure_pins = [4, 17, 27, 22]  # 4개의 압력 센서 연결 핀 (디지털 입력용)
mcp3008_channels = [0, 1, 2, 3]  # MCP3008의 사용할 채널 번호들

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# GPIO 설정
GPIO.setmode(GPIO.BCM)
#for pin in pressure_pins:
#    GPIO.setup(pin, GPIO.IN)


# Firestore에 데이터를 저장하는 함수
def log_pressure_data(channels, analog_values, voltages):
    doc_ref = db.collection('pressure_data').document()
    doc_ref.set({
        'channel': channels,
        'analog_value': analog_values,
        'voltage': voltages,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def log_vibration_data():
    doc_ref = db.collection('vibration_data').document()
    doc_ref.set({
        'voltage': voltages,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

# MCP3008에서 데이터 읽기 함수
def read_mcp3008(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# 메인 루프
while True:
    FSR_detect_count = 0
    channels = []
    analog_values = []
    voltages = []
    
    for i, channel in enumerate(mcp3008_channels):
        # MCP3008을 통해 아날로그 값 읽기
        analog_value = read_mcp3008(channel)

        # 아날로그 값을 3.3V 기준으로 변환하여 전압으로 계산
        voltage = analog_value * 3.3 / 1023
        
        if (voltage > 0.1):
            FSR_detect_count += 1
            channels.append(channel)
            analog_values.append(analog_value)
            voltages.append(voltage)
            #읽은 아날로그 값과 계산된 전압 출력
            print(f"Channel {channels}: Analog Value = {analog_values}, Voltage = {voltages}")
            
        
    # 파이어베이스에 데이터 값 넣기
    if (FSR_detect_count >= 2):
        log_pressure_data(channels, analog_values, voltages) 

    # 데이터 스팸 방지를 위한 잠시 대기
    time.sleep(0.10)
    