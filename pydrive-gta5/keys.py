import time
import ctypes
import win32api as wapi


SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
t_time = 0.09

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class Keys:
    def __init__(self):
        self.key_list = []
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
            self.key_list.append(c)

    def check(self):
        keys = []
        for key in self.key_list:
            if wapi.GetAsyncKeyState(ord(key)):
                keys.append(key)
        return keys

    def keys_to_onehot(self, keys):
        output = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        one_index = None

        if "W" in keys and "A" in keys:     # WA
            one_index = 0
        elif "W" in keys and "D" in keys:   # WD
            one_index = 1
        elif "S" in keys and "A" in keys:   # SA
            one_index = 2
        elif "S" in keys and "D" in keys:   # SD
            one_index = 3
        elif "W" in keys:                   # W
            one_index = 4
        elif "S" in keys:                   # S
            one_index = 5
        elif "A" in keys:                   # A
            one_index = 6
        elif "D" in keys:                   # D
            one_index = 7
        else:                               # NO KEY PRESSED
            one_index = 8

        if one_index is not None:
            output[one_index] = 1

        return output



def execute_input(move_index=-1):
    def press_key(hex_code):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hex_code, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def release_key(hex_code):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hex_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    if move_index == 0:     # WA
        release_key(S)
        release_key(D)
        press_key(W)
        press_key(A)
        time.sleep(t_time)
    elif move_index == 1:   # WD
        release_key(A)
        release_key(S)
        press_key(W)
        press_key(D)
        time.sleep(t_time)
    elif move_index == 2:   # SA
        release_key(W)
        release_key(D)
        press_key(S)
        press_key(A)
        time.sleep(t_time)
    elif move_index == 3:   # SD
        release_key(W)
        release_key(A)
        press_key(S)
        press_key(D)
        time.sleep(t_time)
    elif move_index == 4:   # W
        release_key(A)
        release_key(S)
        release_key(D)
        press_key(W)
        time.sleep(t_time)
    elif move_index == 5:   # S
        release_key(W)
        release_key(A)
        release_key(D)
        press_key(S)
        time.sleep(t_time)
    elif move_index == 6:   # A
        release_key(W)
        release_key(S)
        release_key(D)
        press_key(A)
        time.sleep(t_time)
    elif move_index == 7:   # D
        release_key(W)
        release_key(A)
        release_key(S)
        press_key(D)
        time.sleep(t_time)
    else:                   # NO KEY PRESSED
        release_key(W)
        release_key(A)
        release_key(S)
        release_key(D)
