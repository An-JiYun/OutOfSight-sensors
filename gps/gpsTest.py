import serial
import pynmea2

while True:
    port = "/dev/ttyS0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    newdata = ser.readline()

    # 빈 데이터가 아닌 경우에만 처리
    if newdata:
        # NMEA 문장의 시작 부분 확인
        if newdata.startswith(b'$'):
            try:
                # NMEA 문장 파싱 시도
                newmsg = pynmea2.parse(newdata.decode('ascii', errors='ignore'))
                # 특정 NMEA 문장 타입에 따라 처리
                if hasattr(newmsg, 'latitude') and hasattr(newmsg, 'longitude'):
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
                    print(gps)
                else:
                    # 다른 타입의 NMEA 문장도 출력
                    print(newmsg)
            except pynmea2.ParseError as e:
                # 파싱 에러 출력
                print(f"Parse error: {e}")
                continue

# import serial
# import time
# import string
# import pynmea2

# while True:
# 	port="/dev/ttyS0"
# 	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
# 	dataout = pynmea2.NMEAStreamReader()
# 	newdata=ser.readline()
# 	if newdata[0:6] == "$GPRMC":
# 		newmsg=pynmea2.parse(newdata)
# 		lat=newmsg.latitude
# 		lng=newmsg.longitude
# 		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
# 		print(gps)

# import serial
# import pynmea2

# port = "/dev/ttyS0"
# ser = serial.Serial(port, baudrate=9600, timeout=0.5)

# while True:
#     try:
#         newdata = ser.readline().decode('ASCII', errors='replace').strip()
#         if newdata.startswith("$GPRMC"):
#             newmsg = pynmea2.parse(newdata)
#             lat = newmsg.latitude
#             lng = newmsg.longitude
#             gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
#             print(gps)
#     except serial.SerialException as e:
#         print("Serial port error: ", e)
#     except pynmea2.ParseError as e:
#         print("Parse error: ", e)
#     except KeyboardInterrupt:
#         print("\nProgram terminated by user")
#         break

# ser.close()

# import serial

# # 시리얼 포트 설정
# ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# # 데이터 읽기
# while True:
#     data = ser.readline()
#     if data:
#         print(data.decode('ascii', errors='replace'))
