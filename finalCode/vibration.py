import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) 
PIN_NUM = 23 
CHECK_ON=1 
GPIO.setup(PIN_NUM, GPIO.IN) 
PREV_TIME=time.time() 
CUR_TIME=time.time() 

vibration_counts = []
filename = "/home/rpi/Documents/sensors/text/vibration_data.txt"  # 저장할 파일 경로

try:
    i = 0
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

            # 리스트에 3개 값이 있으면 파이어베이스에 데이터 보내기
            if len(vibration_counts) >= 3:
                with open(filename, "w") as file:
                    file.write("true")
                print(f"vibration Data written to file (3 value in list)")
                
                # 10초 동안 멈추기
                time.sleep(10)
                vibration_counts = []  # 리스트 초기화

        time.sleep(0.01)

finally:
    GPIO.cleanup()