from machine import Pin, PWM
import time
import sys

# — Motores paso a paso —
motor_A_pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)]
motor_B_pins = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
step_seq = [
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 0]
]
def step_motor(pins, steps=10, delay=0.003, reverse=False):
    seq = step_seq[::-1] if reverse else step_seq
    for _ in range(steps):
        for pattern in seq:
            for pin, v in zip(pins, pattern):
                pin.value(v)
            time.sleep(delay)
    # apaga bobinas
    for pin in pins:
        pin.value(0)

# — Servos —
servo0 = PWM(Pin(0)); servo0.freq(50)
servo1 = PWM(Pin(1)); servo1.freq(50)
def set_servo(servo, angle):
    # duty_u16: de 1638 (10%) a 8192 (50%) lineal con 0–180°
    duty = int(1638 + (angle/180) * (8192 - 1638))
    servo.duty_u16(duty)

print("Listo para comandos por USB serial...")
while True:
    line = sys.stdin.readline().strip().lower()
    if not line:
        continue

    # Motores A/B
    if line == "a_right":
        step_motor(motor_A_pins, reverse=False)
    elif line == "a_left":
        step_motor(motor_A_pins, reverse=True)
    elif line == "b_right":
        step_motor(motor_B_pins, reverse=False)
    elif line == "b_left":
        step_motor(motor_B_pins, reverse=True)

    # Servos 0 y 1
    # Comandos: "servo0_ANGLE" o "servo1_ANGLE"
    elif line.startswith("servo0_"):
        try:
            ang = float(line.split("_")[1])
            set_servo(servo0, ang)
        except:
            pass
    elif line.startswith("servo1_"):
        try:
            ang = float(line.split("_")[1])
            set_servo(servo1, ang)
        except:
            pass
