import cv2
import win32gui
import numpy as np
from mss import mss


def record_screen(resize=None, region=None):
    if not region:
        region = win32gui.GetWindowRect(win32gui.GetForegroundWindow())

    left, top, x2, y2 = region
    top += 40  # remove the window title bar from the image
    height = y2 - top
    width = x2 - left
    bbox = {"top": top, "left": left, "width": width, "height": height}

    screenshot = mss()
    while 1:
        frame = np.array(screenshot.grab(bbox))
        if resize:
            frame = cv2.resize(frame, dsize=resize)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        yield np.array(frame)


if __name__ == '__main__':
    import time
    from settings import _WIDTH, _HEIGHT

    print("Starting in...")
    for i in range(4)[::-1]:
        print(i + 1)
        time.sleep(1)

    for frame in record_screen((_WIDTH, _HEIGHT)):
        cv2.imshow("screen", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
