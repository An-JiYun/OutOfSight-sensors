# import serial
# import time
# import string
# import pynmea2
# import firebase_admin
# from firebase_admin import credentials, firestore

# cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
# # firebase_admin.initialize_app(cred, {
# #     'storageBucket': 'out-of-sight-814f2.appspot.com'
# # })
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # 차량 번호판 읽기
# # with open('/home/rpi/Documents/sensors/licensePlate.txt', 'r') as file:
# #     license_plate = file.read().strip()
# license_plate = 12345
# port = "/dev/ttyS0"
# ser = serial.Serial(port, baudrate=9600, timeout=1)
# ser.flushInput()
# try:
#     while True:
#         if ser.in_waiting > 0:
#             newdata = ser.readline()

#             if newdata[0:6] == b"$GPRMC":
#                 newmsg = pynmea2.parse(newdata.decode('ascii', errors='replace'))
#                 lat = newmsg.latitude
#                 lng = newmsg.longitude
                

#                 # Firestore 'Vehicles' 컬렉션에서 해당 차량 문서 찾기
#                 vehicles_ref = db.collection('Vehicles')
#                 query = vehicles_ref.where('licensePlate', '==', license_plate)
#                 docs = query.stream()
                
#                  # GPS 좌표 업데이트
#                 for doc in docs:
#                     doc_ref = vehicles_ref.document(doc.id)
#                     doc_ref.update({'gps': firestore.GeoPoint(lat, lng)})
#                 print("Latitude=" + str(lat) + " and Longitude=" + str(lng))
#         # else :
#         #     print("ser.in_waiting < 0 : 읽을거리가 없대")

# except KeyboardInterrupt:
#     print("Program terminated by user")
#     ser.close()

import serial
import time
import string
import pynmea2
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase 초기화
cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

license_plate = "12345"  # 차량 번호판 설정
port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=9600, timeout=1)
ser.flushInput()

try:
    while True:
        if ser.in_waiting > 0:
            newdata = ser.readline()

            # GPRMC 데이터만 파싱
            if newdata[0:6] == b"$GPRMC":
                newmsg = pynmea2.parse(newdata.decode('ascii', errors='replace'))
                lat = newmsg.latitude
                lng = newmsg.longitude
                timestamp = datetime.utcnow()  # 현재 UTC 시간

                # Firestore에 데이터 저장
                data = {
                    'latitude': lat,
                    'longitude': lng,
                    'licensePlate': license_plate,
                    'timestamp': timestamp  # Firestore의 Timestamp 형식으로 자동 변환
                }
                # GPS 데이터를 포함하는 새 문서 생성
                db.collection('GPS').add(data)
                
                print(f"Latitude={lat} and Longitude={lng}, Timestamp={timestamp}")
                time.sleep(30)
except KeyboardInterrupt:
    print("Program terminated by user")
    ser.close()
