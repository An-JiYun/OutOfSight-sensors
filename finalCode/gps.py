import serial
import time
import string
import pynmea2
from datetime import datetime

port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=9600, timeout=1)
ser.flushInput()

filename = "/home/rpi/Documents/sensors/text/gps_data.txt"  # 저장할 파일 경로

pre_lat = -1
pre_lng = -1

try:
    while True:
        if ser.in_waiting > 0:
            newdata = ser.readline()

            # GPRMC 데이터만 파싱
            if newdata[0:6] == b"$GPRMC":
                newmsg = pynmea2.parse(newdata.decode('ascii', errors='replace'))
                lat = newmsg.latitude #위도 N
                lng = newmsg.longitude #경도 E
                #timestamp = datetime.utcnow()  # 현재 UTC 시간
                
                
                if (lat == 0 or lng ==0 ):
                    print("can't gps sensing")
                    
                elif(pre_lat == -1 or pre_lng ==-1 ):
                    #파일에 값 넣기
                    with open(filename, "w") as file:
                        file.write(f"{lat} {lng}")
                    print(f"Latitude={lat} and Longitude={lng} GPS Data written to file")
                    pre_lat = lat
                    pre_lng = lng
                    
                else:   
                    #이전 값 있으면 이전 값과 비교해서 좀 큰차이가 나면 파일에 값 넣기
                    sub_lat = abs(pre_lat - lat)
                    sub_lng = abs(pre_lng - lng)                    
                    
                    if(sub_lat>0.0001 or sub_lng>0.0001):
                        with open(filename, "w") as file:
                            file.write(f"{lat} {lng}")
                        print(f"Latitude={lat} and Longitude={lng} GPS Data written to file")
                        pre_lat = lat
                        pre_lng = lng
                    else : 
                        print(f"Latitude={lat} and Longitude={lng} very small distance, don't write")
                
            time.sleep(0.1)
                
except KeyboardInterrupt:
    print("Program terminated by user")
    ser.close()
