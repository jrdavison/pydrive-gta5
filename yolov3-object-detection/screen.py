import cv2
import win32gui
import numpy as np
from mss import mss


def record_screen(resize=None, region=None):
    if not region:
        region = win32gui.GetWindowRect(win32gui.GetForegroundWindow())

    left, top, x2, y2 = region
    height = y2 - top + 1
    width = x2 - left + 1
    bbox = {'top': top, 'left': left, 'width': width, 'height': height}

    screenshot = mss()
    while 1:
        frame = np.array(screenshot.grab(bbox))
        if resize:
            frame = cv2.resize(frame, dsize=resize)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        yield np.array(frame)


if __name__ == '__main__':
    for frame in record_screen((800, 640)):
        cv2.imshow('screen', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
