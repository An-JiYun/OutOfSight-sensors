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

import serial

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# 데이터 읽기
while True:
    data = ser.readline()
    if data:
        print(data.decode('ascii', errors='replace'))
