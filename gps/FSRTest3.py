import RPi.GPIO as GPIO
import spidev
import time

# GPIO 핀 번호 설정
pressure_pin = 4  # 압력 센서 연결 핀 (디지털 입력용)
led_pin = 2       # LED 연결 핀
mcp3008_channel = 0  # MCP3008의 채널 번호

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 포트 0, 디바이스 0
spi.max_speed_hz = 1350000  # MCP3008의 최대 SPI 클록 속도

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(pressure_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)  # LED 핀을 출력으로 설정

# 이전 입력 상태
#prev_input = 0

# MCP3008에서 데이터 읽기 함수
def read_mcp3008(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

while True:
    # 압력 센서로부터 디지털 입력값 읽기
    #input = GPIO.input(pressure_pin)

    # MCP3008을 통해 아날로그 값 읽기
    analog_value = read_mcp3008(mcp3008_channel)
    voltage = analog_value * 3.3 / 1023  # 아날로그 값을 전압으로 변환 (0-3.3V)

    if (voltage > 0.05):
        GPIO.output(led_pin, GPIO.HIGH)  # LED 켜기
        print(f"Under Pressure - Analog value: {analog_value}, Voltage: {voltage}")
    # 압력이 없으면 LED 끄기
    elif (input):
        GPIO.output(led_pin, GPIO.LOW)  # LED 끄기

    # 압력 감지 시 LED 켜기 (0과 1로 보이기위해 큰 압력이 들어와야함)
    # if ((not prev_input) and input):
    #     GPIO.output(led_pin, GPIO.HIGH)  # LED 켜기
    #     print(f"Under Pressure - Analog value: {analog_value}, Voltage: {voltage}")
    # # 압력이 없으면 LED 끄기
    # elif (prev_input and not input):
    #     GPIO.output(led_pin, GPIO.LOW)  # LED 끄기

    # 이전 입력 상태 업데이트
    # prev_input = input

    # 데이터 스팸 방지를 위한 잠시 대기
    time.sleep(0.10)