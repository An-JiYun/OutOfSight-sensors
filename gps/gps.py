import serial
import time
import string
import pynmea2
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'out-of-sight-814f2.appspot.com'
})

port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=9600, timeout=1)
ser.flushInput()
try:
    while True:
        if ser.in_waiting > 0:
            newdata = ser.readline()

            if newdata[0:6] == b"$GPRMC":
                newmsg = pynmea2.parse(newdata.decode('ascii', errors='replace'))
                lat = newmsg.latitude
                lng = newmsg.longitude
                gps = {"latitude": lat, "longitude": lng}

                # Firebase Realtime Database에 데이터 저장
                ref = db.reference('/gps_data')
                ref.push(gps)

                print("Latitude=" + str(lat) + " and Longitude=" + str(lng))
        # else :
        #     print("ser.in_waiting < 0 : 읽을거리가 없대")

except KeyboardInterrupt:
    print("Program terminated by user")
    ser.close()