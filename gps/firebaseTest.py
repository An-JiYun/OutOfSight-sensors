import time
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred)
# Firestore 인스턴스 초기화
db = firestore.client()

filename = "/home/rpi/Documents/sensors/vibration_data.txt"  # 읽을 파일 경로

while True:
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                first_line = file.readline().strip()
                vibration_count = int(first_line.split()[0])  # 첫 줄의 첫 숫자만 추출
            
            if vibration_count:
                doc_ref = db.collection('vibration_data').document()
                doc_ref.set({'counts': vibration_count, 'timestamp': firestore.SERVER_TIMESTAMP})

                # 파일 삭제하여 다음 데이터 세트 준비
                os.remove(filename)
                print(f"{vibration_count} set Data sent to Firebase and file deleted")

    except FileNotFoundError:
        print("File not found. Waiting for data...")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 파일 확인 주기 조정
    time.sleep(1)