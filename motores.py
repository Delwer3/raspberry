from machine import Pin, PWM
import uasyncio as asyncio

motor1 = [Pin(5, Pin.OUT), Pin(4, Pin.OUT), Pin(3, Pin.OUT), Pin(2, Pin.OUT)]
motor2 = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
motor3 = [Pin(11, Pin.OUT), Pin(13, Pin.OUT), Pin(10, Pin.OUT), Pin(12, Pin.OUT)]

servo = PWM(Pin(0))
servo.freq(50)

step_seq = [
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 0]
]

def set_servo(angle):
    duty = int(1638 + (angle / 180) * (8192 - 1638))
    servo.duty_u16(duty)

async def step_motor(pins, delay=0.003, steps=10, reverse=False):
    seq = step_seq[::-1] if (reverse and pins in [motor2, motor3]) or (not reverse and pins == motor1) else step_seq
    for _ in range(steps):
        for step in seq:
            for pin, val in zip(pins, step):
                pin.value(val)
            await asyncio.sleep(delay)

async def main():
    while True:

        set_servo(94)
        await asyncio.gather(
            step_motor(motor2)
        )
        await asyncio.sleep(1)

asyncio.run(main())