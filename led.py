import serial
import time
import tkinter as tk
from tkinter import ttk
import threading

# configura puerto serial
ser = serial.Serial('COM3', 115200)
time.sleep(2)

# estado de movimiento para motores y servos (variables de estado)
en_movimiento = {
    'a_right': False,
    'a_left': False,
    'b_right': False,
    'b_left': False,
    's0_inc': False,
    's0_dec': False,
    's1_inc': False,
    's1_dec': False
}

# angulos actuales de servos
angle0 = 0  # limite 0 a 114 grados
angle1 = 0  # limite 0 a 180 grados
angle_lock = threading.Lock()

# tiempos de espera para cada motor (cooldown)
motor_speeds = {'a': 0.2, 'b': 0.15}

# funcion para mover motor en bucle
def mover_motor(comando):
    motor = comando.split('_')[0]
    delay = motor_speeds.get(motor, 0.2)
    while en_movimiento[comando]:
        ser.write((comando + '\n').encode())
        time.sleep(delay)

# funcion para subir o bajar servo0
def mover_servo0():
    global angle0
    while en_movimiento['s0_inc'] or en_movimiento['s0_dec']:
        with angle_lock:
            if en_movimiento['s0_inc'] and angle0 < 114:
                angle0 += 1
            elif en_movimiento['s0_dec'] and angle0 > 0:
                angle0 -= 1
            ser.write(f"servo0_{angle0}\n".encode())
            pb0['value'] = angle0
        time.sleep(0.02)

# funcion para subir o bajar servo1
def mover_servo1():
    global angle1
    while en_movimiento['s1_inc'] or en_movimiento['s1_dec']:
        with angle_lock:
            if en_movimiento['s1_inc'] and angle1 < 180:
                angle1 += 1
            elif en_movimiento['s1_dec'] and angle1 > 0:
                angle1 -= 1
            ser.write(f"servo1_{angle1}\n".encode())
            pb1['value'] = angle1
        time.sleep(0.02)

# cambia estado de botones a disabled o normal
def cambiar_estado_botones(estado):
    for btn in botones:
        btn.config(state=estado)

# inicia movimiento si no hay otro en curso
def iniciar_movimiento(comando, tipo):
    if any(en_movimiento.values()):
        return
    en_movimiento[comando] = True
    cambiar_estado_botones('disabled')
    if tipo == 'motor':
        threading.Thread(target=mover_motor, args=(comando,), daemon=True).start()
    elif tipo == 's0':
        threading.Thread(target=mover_servo0, daemon=True).start()
    elif tipo == 's1':
        threading.Thread(target=mover_servo1, daemon=True).start()

# detiene movimiento y habilita botones
def detener_movimiento(comando):
    en_movimiento[comando] = False
    cambiar_estado_botones('normal')

# crea ventana y marco general
ventana = tk.Tk()
ventana.title('Control Motores y Servos')
ventana.geometry('600x700')
ventana.configure(bg='#F0F2F5')

# estilo sencillo para botones y marcos\style = ttk.Style(ventana)
style.theme_use('clam')
style.configure('TLabelFrame', background='#fff', font=('Helvetica', 14, 'bold'))
style.configure('Motor.TButton', font=('Helvetica', 12, 'bold'), padding=10)
style.configure('Servo0.TButton', font=('Helvetica', 12, 'bold'), padding=10)
style.configure('Servo1.TButton', font=('Helvetica', 12, 'bold'), padding=10)

botones = []  # lista de botones

general_frame = ttk.Frame(ventana, padding=20)
general_frame.pack(fill='both', expand=True)

# marco motores
motor_frame = ttk.LabelFrame(general_frame, text='Motores', padding=10)
motor_frame.grid(row=0, column=0, pady=10)

# motor A con flechas izquierda y derecha
subA = ttk.LabelFrame(motor_frame, text='Motor A', padding=10)
subA.grid(row=0, column=0, padx=10)
btn_a_left = ttk.Button(subA, text='<')
btn_a_left.grid(row=0, column=0, padx=5)
btn_a_left.bind('<ButtonPress>', lambda e: iniciar_movimiento('a_left','motor'))
btn_a_left.bind('<ButtonRelease>', lambda e: detener_movimiento('a_left'))
botones.append(btn_a_left)

btn_a_right = ttk.Button(subA, text='>')
btn_a_right.grid(row=0, column=1, padx=5)
btn_a_right.bind('<ButtonPress>', lambda e: iniciar_movimiento('a_right','motor'))
btn_a_right.bind('<ButtonRelease>', lambda e: detener_movimiento('a_right'))
botones.append(btn_a_right)

# motor B similar a A
subB = ttk.LabelFrame(motor_frame, text='Motor B', padding=10)
subB.grid(row=0, column=1, padx=10)
btn_b_left = ttk.Button(subB, text='<')
btn_b_left.grid(row=0, column=0, padx=5)
btn_b_left.bind('<ButtonPress>', lambda e: iniciar_movimiento('b_left','motor'))
btn_b_left.bind('<ButtonRelease>', lambda e: detener_movimiento('b_left'))
botones.append(btn_b_left)

btn_b_right = ttk.Button(subB, text='>')
btn_b_right.grid(row=0, column=1, padx=5)
btn_b_right.bind('<ButtonPress>', lambda e: iniciar_movimiento('b_right','motor'))
btn_b_right.bind('<ButtonRelease>', lambda e: detener_movimiento('b_right'))
botones.append(btn_b_right)

# marco servos
servo_frame = ttk.LabelFrame(general_frame, text='Servos', padding=10)
servo_frame.grid(row=1, column=0, pady=20)

# servo 0 con barra de progreso y flechas
ttk.Label(servo_frame, text='Servo 0 0-114').grid(row=0, column=0, columnspan=2)
pb0 = ttk.Progressbar(servo_frame, maximum=114, length=250)
pb0.grid(row=1, column=0, columnspan=2, pady=(0,10))
btn_s0_dec = ttk.Button(servo_frame, text='<')
btn_s0_dec.grid(row=2, column=0, padx=5)
btn_s0_dec.bind('<ButtonPress>', lambda e: iniciar_movimiento('s0_dec','s0'))
btn_s0_dec.bind('<ButtonRelease>', lambda e: detener_movimiento('s0_dec'))
botones.append(btn_s0_dec)

btn_s0_inc = ttk.Button(servo_frame, text='>')
btn_s0_inc.grid(row=2, column=1, padx=5)
btn_s0_inc.bind('<ButtonPress>', lambda e: iniciar_movimiento('s0_inc','s0'))
btn_s0_inc.bind('<ButtonRelease>', lambda e: detener_movimiento('s0_inc'))
botones.append(btn_s0_inc)

# servo 1 similar al 0
ttk.Label(servo_frame, text='Servo 1 0-180').grid(row=3, column=0, columnspan=2, pady=(15,0))
pb1 = ttk.Progressbar(servo_frame, maximum=180, length=250)
pb1.grid(row=4, column=0, columnspan=2, pady=(0,10))
btn_s1_dec = ttk.Button(servo_frame, text='<')
btn_s1_dec.grid(row=5, column=0, padx=5)
btn_s1_dec.bind('<ButtonPress>', lambda e: iniciar_movimiento('s1_dec','s1'))
btn_s1_dec.bind('<ButtonRelease>', lambda e: detener_movimiento('s1_dec'))
botones.append(btn_s1_dec)

btn_s1_inc = ttk.Button(servo_frame, text='>')
btn_s1_inc.grid(row=5, column=1, padx=5)
btn_s1_inc.bind('<ButtonPress>', lambda e: iniciar_movimiento('s1_inc','s1'))
btn_s1_inc.bind('<ButtonRelease>', lambda e: detener_movimiento('s1_inc'))
botones.append(btn_s1_inc)

# inicia bucle de eventos de la ventana
ventana.mainloop()
