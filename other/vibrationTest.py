import RPi.GPIO as GPIO
import time 

#import firebase_admin
#from firebase_admin import credentials, firestore

# Firebase 초기화
#cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
#firebase_admin.initialize_app(cred)
# Firestore 인스턴스 초기화
#db = firestore.client()

GPIO.setmode(GPIO.BCM) 
PIN_NUM = 23 
CHECK_ON=1 
GPIO.setup(PIN_NUM, GPIO.IN) 
PREV_TIME=time.time() 
CUR_TIME=time.time() 

try:
    i = 0
    vibration_counts = []
    while True:
        if GPIO.input(PIN_NUM) == CHECK_ON:
            i += 1

        CUR_TIME = time.time()

        # 3초마다 진동 카운트 검사 및 리스트에 추가
        if CUR_TIME - PREV_TIME > 3:
            print("Vibration count in last 3 seconds:", i)
            if i > 20:
                vibration_counts.append(i)
            i = 0
            PREV_TIME = CUR_TIME

            # 리스트에 4개 값이 있으면 파이어베이스에 데이터 보내기
            if len(vibration_counts) >= 4:
                # 예시: 파이어베이스에 데이터 보내기
                #doc_ref = db.collection('vibration_data').document()
                #doc_ref.set({'counts': vibration_counts, 'timestamp': firestore.SERVER_TIMESTAMP})
                print("Data sent to Firebase")

                # 1분 동안 멈추기
                time.sleep(30)
                vibration_counts = []  # 리스 초기화

        time.sleep(0.01)

finally:
    GPIO.cleanup()