def sleep(self, ms=1000):
    from PyQt5.QtCore import QEventLoop, QTimer
    loop = QEventLoop(self)
    QTimer.singleShot(ms, loop.quit)
    loop.exec()