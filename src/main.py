import ctypes
import sys
import sdl2
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg


class Joystick:
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        self.axis = {}
        self.button = {}

    def update(self):
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_JOYDEVICEADDED:
                self.device = sdl2.SDL_JoystickOpen(event.jdevice.which)
            elif event.type == sdl2.SDL_JOYAXISMOTION:
                self.axis[event.jaxis.axis] = event.jaxis.value
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.button[event.jbutton.button] = True
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.button[event.jbutton.button] = False

class CephWindow(qtw.QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.yes_button = qtw.QPushButton('Yes')

        self.setCentralWidget(self.yes_button)


if __name__ == "__main__":
    joystick = Joystick()
    app = qtw.QApplication(sys.argv)
    window = CephWindow()
    window.show()
    sys.exit(app.exec())
    # while True:
    #     joystick.update()
    #     time.sleep(0.1)
    #     print(joystick.axis)
    #     print(joystick.button)