import RPi.GPIO as GPIO
import spidev
import time

# GPIO 핀 번호 설정
mcp3008_channels = [0, 1, 2, 3]  # MCP3008의 사용할 채널 번호들

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# GPIO 설정
GPIO.setmode(GPIO.BCM)

filename = "/home/rpi/Documents/sensors/text/pressure_data.txt"  # 저장할 파일 경로

# MCP3008에서 데이터 읽기 함수
def read_mcp3008(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

#voltage_list = [0.13, 0.08, 0.13, 0.1]

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
        
        #if (voltage > voltage_list[channel]):
        if (voltage):
            FSR_detect_count += 1
            channels.append(channel)
            analog_values.append(analog_value)
            voltages.append(voltage)
            #읽은 아날로그 값과 계산된 전압 출력
            print(f"Channel {channels}: Analog Value = {analog_values}, Voltage = {voltages}")
        
        
    # 텍스트 파일 쓰기
    if (FSR_detect_count >= 2):
        #print(f"Channel {channels}: Analog Value = {analog_values}, Voltage = {voltages}")
        with open(filename, "w") as file:
            file.write("true")
        print(f"pressure Data written to file")
        time.sleep(10)
        
    # 데이터 스팸 방지 등을 위한 잠시 대기
    time.sleep(1)
    