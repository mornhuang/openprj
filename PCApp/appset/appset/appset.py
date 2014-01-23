#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-11 17:03

"""

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

from PySide import QtGui
from PySide import QtCore

from appmain.winmain.appmain import MainWindow
from modules.resume.window.rsmmod import PostRrdMod
from modules.lunar.lunarmod import LunarMod
from utils import log

if os.name == 'nt':
    import ctypes
    import ctypes.wintypes

    def errCheck(result, func, args):
        if not result:
            log.warning(ctypes.WinError())

        return args

    ctypes.windll.user32.RegisterHotKey.errcheck = errCheck
    ctypes.windll.user32.UnregisterHotKey.errcheck = errCheck
    ctypes.windll.user32.GetMessageA.errcheck = errCheck

    MOD_ALT = 1
    MOD_CONTROL = 2
    MOD_SHIFT = 4
    MOD_WIN = 8
    WM_HOTKEY = 786

    def getHWND(winId):
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        return ctypes.pythonapi.PyCapsule_GetPointer(winId, None)

    ############### Another implement router #######################################
    #from ctypes import c_int
    #from ctypes.wintypes import BOOL, HWND, UINT, LPMSG
    #prototype = ctypes.WINFUNCTYPE(BOOL, HWND, c_int, UINT, UINT)
    #paramflags = (1, 'hWnd'), (1, 'id'), (1, 'fsModifiers'), (1, 'vk')
    #RegisterHotKey = prototype(('RegisterHotKey', ctypes.windll.user32), paramflags)
    #RegisterHotKey.errcheck = errCheck

    class MyHotKey(QtCore.QThread):
        """
        PySide has no message attribute when call winEventFilter, so can not capture
        Hotkey event. To archive capture event, use this crack method. Fuck!
        This method can't unregist hotkey.
        """
        press = QtCore.Signal()

        def run(self):
            ctypes.windll.user32.RegisterHotKey(None, 1,
                                                MOD_CONTROL | MOD_ALT,
                                                ord('Z'))
            try:
                msg = ctypes.wintypes.MSG()
                while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == WM_HOTKEY:
                        self.press.emit()
                    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                    ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
            finally:
                ctypes.windll.user32.UnregisterHotKey(None, 1)


class MyApplication(QtGui.QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        # load translation file
        locate = QtCore.QLocale.system().name()
        fileName = "appset." + locate
        translator = QtCore.QTranslator()
        translator.load(fileName)
        self.installTranslator(translator)

        #regist/initial modules
        self.winmain = MainWindow()
        self.winmain.registModule(PostRrdMod)
        self.winmain.registModule(LunarMod)
        self.winmain.initModules()

        # Regist HotKey in windows platform
        if os.name == 'nt':
            self.hotkey = MyHotKey()
            self.hotkey.press.connect(self.winmain.actionRestore)
            self.hotkey.start()

        #self.winmain.show()

    def quit(self):
        """
        Extend the built-in event filtering to handle UnregisterHotKey.
        """
        if os.name == 'nt':
            self.hotkey.terminate()
            self.hotkey.wait(10)

        super().quit()


def main():
    """
    AppSet application's entry
    """

    # Create a Qt application
    app = MyApplication(sys.argv)

    # run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

