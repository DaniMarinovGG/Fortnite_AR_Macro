import mouse
import time
import ctypes
from pynput.mouse import Controller

MOUSEEVENTF_MOVE = 0x0001


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]


def move_mouse_relative(x, y):
    mouse_input = MOUSEINPUT(dx=x, dy=y, mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0, dwExtraInfo=None)
    input_structure = INPUT(type=0, mi=mouse_input)  # 0 is INPUT_MOUSE
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_structure), ctypes.sizeof(INPUT))


def control_recoil():
    for i in range(30):
        if mouse.is_pressed("left"):
            move_mouse_relative(1, 3)
            time.sleep(0.02)
        else:
            break
    time.sleep(0.5)
    for i in range(11):
        if mouse.is_pressed("left"):
            move_mouse_relative(-3, 2)
            time.sleep(0.05)
        else:
            break


left_button_pressed = False


monkey = Controller()
while True:
    if bool(ctypes.windll.user32.GetKeyState(0x14) & 0x0001):   # check for capslock if it is ON or OFF
        if mouse.is_pressed("left"):
            if not left_button_pressed:
                control_recoil()
                left_button_pressed = True
        else:
            left_button_pressed = False
    time.sleep(0.1)
