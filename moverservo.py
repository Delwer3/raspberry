from machine import Pin, PWM
import uasyncio as asyncio
import time

servoprofe = PWM(Pin(16))
servoprofe.freq(50)
actualang = 0
i = 0
buzzer = Pin(13, Pin.OUT)
lrojo = Pin(1, Pin.OUT)
lverde = Pin(0, Pin.OUT)

def verde(val):
    lverde.value(val)
def rojo(val):
    lrojo.value(val)

def beep(on, off):
    buzzer.on()
    time.sleep(on)
    buzzer.off()
    time.sleep(off)
    
def bienvenida():
    beep(0.1, 0.05)
    beep(0.1, 0.05)
    beep(0.1, 0.05)
    time.sleep(0.1)
    beep(0.2, 0.1)
    beep(0.1, 0.2)

    
def mover_angulo(angulo):
    global actualang
    if 0 <= angulo <= 180:
        duty = int(500000 + (angulo / 180) * 2000000)
        servoprofe.duty_ns(duty)
        actualang = angulo

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(15, Pin.IN, Pin.PULL_DOWN)

limite_bajo_activado = False
limite_alto_activado = False

async def bucle():
    global actualang, i, limite_alto_activado
    while True:
        if button.value() == 1 and i < 180:
            print("Angulo = " + str(i))
            i += 1
            mover_angulo(actualang + 1)
            rojo(1)
            limite_alto_activado = False
            await asyncio.sleep(0.01)
        else:
            rojo(0)
            if button.value() == 1 and i == 180 and not limite_alto_activado:
                buzzer.on()
                await asyncio.sleep(0.05)
                buzzer.off()
                limite_alto_activado = True
            await asyncio.sleep(0.01)

async def bucleres():
    global actualang, i, limite_bajo_activado
    while True:
        if button2.value() == 1 and i > 0:
            print("Angulo = " + str(i))
            i -= 1
            mover_angulo(actualang - 1)
            verde(1)
            limite_bajo_activado = False
            await asyncio.sleep(0.01)
        else:
            verde(0)
            if button2.value() == 1 and i == 0 and not limite_bajo_activado:
                buzzer.on()
                await asyncio.sleep(0.05)
                buzzer.off()
                limite_bajo_activado = True
            await asyncio.sleep(0.01)

async def main():
    bienvenida()
    mover_angulo(0)
    rojo(1)
    await asyncio.gather(bucle(), bucleres())
 
asyncio.run(main())
