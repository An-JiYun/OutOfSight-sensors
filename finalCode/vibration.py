import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) 
PIN_NUM = 23 
CHECK_ON=1 
GPIO.setup(PIN_NUM, GPIO.IN) 
PREV_TIME=time.time() 
CUR_TIME=time.time() 

filename = "/home/rpi/Documents/sensors/text/vibration_data.txt"  # 저장할 파일 경로

try:
    i = 0
    while True:
        if GPIO.input(PIN_NUM) == CHECK_ON:
            i += 1

        CUR_TIME = time.time()

        # 1초마다 진동 카운트 검사 및 리스트에 추가
        if CUR_TIME - PREV_TIME > 1:
            print("Vibration count in last 1 seconds:", i)
            if i > 0: #내지는 1
                with open(filename, "w") as file:
                    file.write("true")
                print(f"vibration Data written to file (3 value in list)")
            
            i = 0
            PREV_TIME = CUR_TIME

        time.sleep(0.01)

finally:
    GPIO.cleanup()
