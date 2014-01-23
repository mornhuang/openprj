#!usr/bin/env python
#-*- coding:utf-8 -*-

""" 
Date: 2013-11-06 21:25
AppSet application's main
"""

from appmain.winmain.appmain_ui import *
from appmain.setting.appconf import *
from appmain.setting.syssetting import *
from abstract.appqtmod import *
from utils import log


def getModCls(mod):
    """
    Get module's class
    """
    if isinstance(mod, str) and mod in globals().keys():
        mod = globals()[mod]

    if isinstance(mod, type) and issubclass(mod, AppMod):
        return mod

    else:
        return None


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Application's main window class.
    """

    def __init__(self, parent=None):
        """
        Class initial method.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.__trayIcon = QSystemTrayIcon(self)
        self.__appConf = AppConf()
        self.__modSubWin = {}
        self.__modAction = {}
        self.__modules = []

        # restore settings
        self.__appConf.loadConf()
        self.__loadSystemSetting()

        # setup icon
        appIcon = QIcon(":/images/appset.ico")
        self.setWindowIcon(appIcon)
        self.__trayIcon.setIcon(appIcon)

        # setup tray icon
        self.__restoreAction = QAction(self.tr("Restore"), self, triggered=self.actionRestore)
        self.__quitAction = QAction(self.tr("Quit"), self, triggered=self.on_actionQuit_triggered)
        menu = QMenu()
        menu.addAction(self.__restoreAction)
        menu.addSeparator()
        menu.addAction(self.__quitAction)
        self.__trayIcon.setContextMenu(menu)
        self.__trayIcon.setToolTip(self.tr("AppSet"))
        self.__trayIcon.activated.connect(self.__trayIconActivated)

        # show tray icon
        if QSystemTrayIcon.isSystemTrayAvailable() and self.__appConf.isHideInTray():
            self.__trayIcon.show()

        # connect sub window active
        self.mdiArea.subWindowActivated.connect(self.__activeSubWindow)

        # enable toolbar
        self.toolBar.setEnabled(True)
        self.toolBar.setIconSize(QSize(16, 16))
        self.toolBar.actionTriggered.connect(self.__toolBarAction)

    @Slot()
    def __trayIconActivated(self, reason):
        """
        Click system tray icon, if window has closed and tray icon is
        available, restore window. At the same time, if application's configuration
         (asking quit) is true, close the tray icon also.
        """
        if reason == (QSystemTrayIcon.ActivationReason.Trigger
                      or QSystemTrayIcon.ActivationReason.DoubleClick):
            if not self.isVisible():
                self.show()
                if self.__appConf.isAskQuit():
                    self.__trayIcon.setVisible(False)

    def setVisible(self, visible):
        """
        @override method
        Set whether restore action enable when main window become visible or invisible
        """
        super().setVisible(visible)
        self.__restoreAction.setEnabled(not visible)

    def closeEvent(self, event):
        """
        @override method
        Deal window close event.
        """
        canExit = True

        # if config set ask when quit and platform support tray icon,
        # show message box to select quit modal
        if self.__appConf.isAskQuit() and QSystemTrayIcon.isSystemTrayAvailable():
            canExit = self.__AskQuit()

        if not canExit:
            event.ignore()

        elif self.__trayIcon.isVisible():   # if tray icon enable, hide main window
            self.hide()
            event.ignore()

        else:
            self.__exitAppMain()
            event.accept()

    @Slot()
    def on_actionQuit_triggered(self):
        """
        Action quit method.
        """
        self.__exitAppMain()
        QApplication.instance().quit()

    @Slot()
    def actionRestore(self):
        """
        Action restore method.
        """
        self.setWindowState(Qt.WindowNoState)
        self.show()

    def __loadSystemSetting(self):
        """
        Load system settings and restore these settings.
        """
        try:
            pos = consttype.SysSetting.value("position")
            size = consttype.SysSetting.value("size")
            self.resize(size)
            self.move(pos)
        except Exception as e:
            log.exception(e)

    def __saveSystemSetting(self):
        """
        Save current system settings.
        """
        consttype.SysSetting.setValue("position", self.pos())
        consttype.SysSetting.setValue("size", self.size())

    def __AskQuit(self):
        """
        When quit application, show a message box to let user select the
        quit mode.
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle(self.tr("QUIT"))
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(self.tr("Are you want exit to tray icon?"))

        # add a checkbox to message box. QMessage doesn't allow to add new widget,
        # so we use a special method (add layout method) to achieve.
        boxLayout = QHBoxLayout()
        boxLayout.setContentsMargins(40, 0, 0, 0)
        askCheckBox = QCheckBox(self.tr("Don't ask again"))
        askCheckBox.setChecked(True)
        boxLayout.addWidget(askCheckBox)
        msgBox.layout().addLayout(boxLayout, 1, 1)

        yesBtn = msgBox.addButton(self.tr("Yes"), QMessageBox.YesRole)
        noBtn = msgBox.addButton(self.tr("No"), QMessageBox.NoRole)
        msgBox.addButton(self.tr("Cancel"), QMessageBox.RejectRole)
        msgBox.exec_()

        if msgBox.clickedButton() == yesBtn:
            self.__appConf.setHideInTray(True)
            self.__appConf.setAskQuit(not askCheckBox.isChecked())
            self.__trayIcon.show()
            return True
        elif msgBox.clickedButton() == noBtn:
            self.__appConf.setHideInTray(False)
            self.__appConf.setAskQuit(not askCheckBox.isChecked())
            return True
        else:
            return False

    def __exitAppMain(self):
        """
        Do some special operation before exit
        """
        self.__trayIcon.setVisible(False)
        self.__saveSystemSetting()
        self.__appConf.saveConf()
        self.__finiModules()

    def registModule(self, mod, icon=None, tip=None):
        """
        Regist external module to main frame.
        Only add toolbar action, not create module instance.
        """
        self.__addModTBIcon(mod, icon, tip)

        modCls = getModCls(mod)
        if modCls is not None:
            self.__modules.append(modCls)

    def unRegistModule(self, mod):
        """
        UnRegist external module
        """
        self.__delModTBIcon(mod)

        modCls = getModCls(mod)
        if (modCls is not None) and (modCls in self.__modules):
            self.__modules.remove(modCls)

    def initModules(self):
        """
        Initialize all registed application module.
        """
        defMod = self.__appConf.getConfItem("default_mod")
        for modCls in self.__modules:
            if defMod == modCls.__name__:
                self.__createAppMod(modCls)
                break

    def __finiModules(self):
        """
        Finish module operation.
        """
        for subWin in self.mdiArea.subWindowList():
            module = subWin.widget()
            if isinstance(module, AppMod):
                try:
                    module.fini()
                except Exception as e:
                    log.exception(e)

    def __createAppMod(self, modCls):
        """
        Create module.
        """
        if issubclass(modCls, AppQtMod):                    # AppQtMod instance
            if modCls.__name__ in self.__modSubWin.keys():
                subWin = self.__modSubWin[modCls.__name__]

            else:
                try:
                    module = modCls()
                    if module.init():
                        subWin = self.__addSubWin(module)
                except Exception as e:
                    log.exception(e)
                    self.__delSubWin(modCls)
                    return

            if subWin != self.mdiArea.activeSubWindow():
                self.mdiArea.setActiveSubWindow(subWin)

            subWin.showMaximized()

    def __addSubWin(self, module):
        """
        Add module sub window.
        """
        subWin = self.mdiArea.addSubWindow(module)
        subWin.setSystemMenu(None)
        subWin.setWindowIcon(QIcon(":/images/appset.svg"))
        #subWin.setWindowFlags(Qt.FramelessWindowHint)
        subWin.setAttribute(Qt.WA_DeleteOnClose)
        module.showMaximized()
        self.__modSubWin[module.__class__.__name__] = subWin
        subWin.installEventFilter(self)
        return subWin

    def __delSubWin(self, modCls):
        """
        Delete module sub window.
        """
        if modCls.__name__ in self.__modSubWin.keys():
            subWin = self.__modSubWin[modCls.__name__]
            if subWin:
                self.mdiArea.removeSubWindow(subWin)
            del self.__modSubWin[modCls.__name__]

    def __addModTBIcon(self, mod, icon, tip):
        """
        add module icon in window's toolbar according to registed modules
        """
        modCls = getModCls(mod)

        if modCls is not None:
            icon = modCls.getIcon()
            if (icon is None) or (not isinstance(icon, QIcon)):
                icon = QIcon(":/images/default.png")
            action = QAction(icon, modCls.getShowName(), self)
            action.setData([0, modCls])
            action.setToolTip(self.tr(modCls.getShowName()))
            action.setStatusTip(self.tr(modCls.getShowName()))
            self.toolBar.addAction(action)
            self.__modAction[modCls.__name__] = action

            return action

    def __delModTBIcon(self, mod):
        """
        del module icon in window's toolbar according to registed modules
        """
        modCls = getModCls(mod)
        if (modCls is not None) and (modCls.__name__ in self.__modAction.keys()):
            action = self.__modAction[modCls.__name__]
            if action:
                self.toolBar.removeAction(action)
            del self.__modAction[modCls.__name__]

    @Slot(QAction)
    def __toolBarAction(self, action):
        if 0 == action.data()[0]:
            modCls = action.data()[1]
            self.__createAppMod(modCls)

    @Slot(QObject)
    def __onSubWinClose(self, subWin):
        if subWin and isinstance(subWin, QMdiSubWindow):
            modCls = subWin.widget().__class__
            self.__delSubWin(modCls)

    @Slot(QMdiSubWindow)
    def __activeSubWindow(self, window):
        """
        When select a window from windows, set selected window to activated.
        """
        if not window:
            return

        self.__updateMainUI()

    def __updateMainUI(self):
        """
        Update main window's UI after loading/activate application modules.
        """
        pass

    def eventFilter(self, obj, event):
        """
        Extend the built-in event filtering to handle sub window close.
        When sub window close, remove sub window from sub window map.
        """
        if isinstance(obj, QMdiSubWindow) and event.type() == QEvent.Close:
            self.__onSubWinClose(obj)

        return QMainWindow.eventFilter(self, obj, event)



