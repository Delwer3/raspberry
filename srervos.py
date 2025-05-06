from machine import Pin, PWM
import uasyncio as asyncio

servo0 = PWM(Pin(0))  # Servo que va hasta 180°
servo1 = PWM(Pin(1))  # Servo que va hasta 94°

servo0.freq(50)
servo1.freq(50)

def set_servo(servo, angle):
    # Convierte ángulo en señal PWM (duty cycle)
    duty = int(1638 + (angle / 180) * (8192 - 1638))
    servo.duty_u16(duty)

def print_state(angle0, angle1):
    print(f"Servo0: {angle0:.1f}°, Servo1: {angle1:.1f}°")

async def sweep_servos():
    angle = 0
    direction = 1

    while True:
        # Servo0 se mueve de 0 a 180
        angle0 = angle

        # Servo1 se mueve proporcionalmente hasta 94°
        angle1 = (angle / 180) * 94

        # Aplicamos movimiento
        set_servo(servo0, angle0)
        set_servo(servo1, angle1)
        print_state(angle0, angle1)

        await asyncio.sleep(0.01)

        # Si servo1 llegó a 50° exactos (con tolerancia), reiniciamos
        if 49.5 <= angle1 <= 50.5:
            print("Servo1 llegó a 50°. Reiniciando...")
            angle = 0
            direction = 1
            await asyncio.sleep(1)
            continue

        # Continuamos movimiento
        angle += direction
        if angle >= 180:
            angle = 180
            direction = -1
        elif angle <= 0:
            angle = 0
            direction = 1

asyncio.run(sweep_servos())
