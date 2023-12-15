import ctypes
import sys
import time
import sdl2
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from x3d_indicator import Ui_MainWindow


# class Joystick:
#     def __init__(self):
#         sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
#         self.axis = {}
#         self.button = {}

#     def update(self):
#         event = sdl2.SDL_Event()
#         while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
#             if event.type == sdl2.SDL_JOYDEVICEADDED:
#                 self.device = sdl2.SDL_JoystickOpen(event.jdevice.which)
#             elif event.type == sdl2.SDL_JOYAXISMOTION:
#                 self.axis[event.jaxis.axis] = event.jaxis.value
#             elif event.type == sdl2.SDL_JOYBUTTONDOWN:
#                 self.button[event.jbutton.button] = True
#             elif event.type == sdl2.SDL_JOYBUTTONUP:
#                 self.button[event.jbutton.button] = False

class CephWindow(qtw.QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.setText("Press this")
        self.ui.pushButton.clicked.connect(self.useOtherThread)

        self.setWindowTitle('Extreme 3d Pro Indicator')

    def useOtherThread(self):
        self.otherThread = qtc.QThread()

        self.worker = USBWorker()

        self.worker.moveToThread(self.otherThread)

        self.otherThread.started.connect(self.worker.run)
        self.worker.finished.connect(self.otherThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.otherThread.finished.connect(self.otherThread.deleteLater)

        self.worker.data.connect(self.showData)

        self.otherThread.start()

    def showData(self, n):
            print("Entered showData in CephWindow")
            self.ui.label_5.setText(f"Data from worker obj w/ another thread: {n}")


class USBWorker(qtc.QObject):
    finished = qtc.Signal()
    data = qtc.Signal(int)

    def run(self):
        self.data.emit(109)
        self.finished.emit()

if __name__ == "__main__":
    # joystick = Joystick()
    app = qtw.QApplication(sys.argv)
    window = CephWindow()
    window.show()
    sys.exit(app.exec())
    # while True:
    #     joystick.update()
    #     time.sleep(0.1)
    #     print(joystick.axis)
    #     print(joystick.button)