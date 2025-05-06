from machine import Pin, PWM
import uasyncio as asyncio
import time

FRECUENCIA_SERVO = 50
PIN_SERVO_A = 23
PIN_SERVO_B = 22
PIN_BOTON_SUBE_A = 14
PIN_BOTON_BAJA_A = 15
PIN_BOTON_SUBE_B = 16
PIN_BOTON_BAJA_B = 17
PIN_LED_ROJO = 1
PIN_LED_VERDE = 0
PIN_TIMBRE = 13

ANGULO_MIN = 0
ANGULO_MAX = 180
PULSO_MIN = 500_000      
RANGO_PULSO = 2_000_000  

servo_a = PWM(Pin(PIN_SERVO_A))
servo_a.freq(FRECUENCIA_SERVO)

servo_b = PWM(Pin(PIN_SERVO_B))
servo_b.freq(FRECUENCIA_SERVO)

boton_sube_a = Pin(PIN_BOTON_SUBE_A, Pin.IN, Pin.PULL_DOWN)
boton_baja_a = Pin(PIN_BOTON_BAJA_A, Pin.IN, Pin.PULL_DOWN)
boton_sube_b = Pin(PIN_BOTON_SUBE_B, Pin.IN, Pin.PULL_DOWN)
boton_baja_b = Pin(PIN_BOTON_BAJA_B, Pin.IN, Pin.PULL_DOWN)

led_rojo = Pin(PIN_LED_ROJO, Pin.OUT)
led_verde = Pin(PIN_LED_VERDE, Pin.OUT)
timbre = Pin(PIN_TIMBRE, Pin.OUT)

angulo_a = ANGULO_MIN
angulo_b = ANGULO_MIN
tope_alto_a = False
tope_bajo_a = False
tope_alto_b = False
tope_bajo_b = False

def establecer_led(led, estado):
    led.value(estado)

def pitido(duracion_on, duracion_off):
    timbre.on()
    time.sleep(duracion_on)
    timbre.off()
    time.sleep(duracion_off)

def bienvenida():
    for _ in range(3):
        pitido(0.1, 0.05)
    time.sleep(0.1)
    pitido(0.2, 0.1)
    pitido(0.1, 0.2)

def mover_servo(servo, angulo):
    duty = PULSO_MIN + int((angulo / ANGULO_MAX) * RANGO_PULSO)
    servo.duty_ns(duty)  

async def control_servo_a():
    global angulo_a, tope_alto_a, tope_bajo_a
    while True:
        if boton_sube_a.value():
            if angulo_a < ANGULO_MAX:
                angulo_a += 1
                mover_servo(servo_a, angulo_a)
                establecer_led(led_rojo, True)
                tope_alto_a = False
                print(f"Servo A: {angulo_a}°")
            elif not tope_alto_a:
                pitido(0.05, 0)
                tope_alto_a = True
        else:
            establecer_led(led_rojo, False)

        if boton_baja_a.value():
            if angulo_a > ANGULO_MIN:
                angulo_a -= 1
                mover_servo(servo_a, angulo_a)
                establecer_led(led_verde, True)
                tope_bajo_a = False
                print(f"Servo A: {angulo_a}°")
            elif not tope_bajo_a:
                pitido(0.05, 0)
                tope_bajo_a = True
        else:
            establecer_led(led_verde, False)

        await asyncio.sleep(0.01)

async def control_servo_b():
    global angulo_b, tope_alto_b, tope_bajo_b
    while True:
        if boton_sube_b.value():
            if angulo_b < ANGULO_MAX:
                angulo_b += 1
                mover_servo(servo_b, angulo_b)
                establecer_led(led_rojo, True)
                tope_alto_b = False
                print(f"Servo B: {angulo_b}°")
            elif not tope_alto_b:
                pitido(0.05, 0)
                tope_alto_b = True
        else:
            establecer_led(led_rojo, False)

        if boton_baja_b.value():
            if angulo_b > ANGULO_MIN:
                angulo_b -= 1
                mover_servo(servo_b, angulo_b)
                establecer_led(led_verde, True)
                tope_bajo_b = False
                print(f"Servo B: {angulo_b}°")
            elif not tope_bajo_b:
                pitido(0.05, 0)
                tope_bajo_b = True
        else:
            establecer_led(led_verde, False)

        await asyncio.sleep(0.01)

async def main():
    bienvenida()
    mover_servo(servo_a, angulo_a)
    mover_servo(servo_b, angulo_b)

    await asyncio.gather(
        control_servo_a(),
        control_servo_b()
    )

asyncio.run(main())

