from PyQt5 import QtCore, QtGui, QtWidgets
import time
import sys

class Bot(QtWidgets.QLabel):

    zone_locs_and_rots = [[(640, 900, 135), (640, 250, 235), (660, 250, 235)], [(1400, 900, 225), (1440, 250, 125), (1420, 250, 125)]]
    tower_locs_and_rots = [[(825, 945, 90), (710, 310, 90), (830, 340, 0), (880, 390, 45), (830, 980, 0), (1580, 310, 90), (1470, 945, 90)], [(825, 945, 270), (710, 800, 90), (1280, 340, 0), (1200, 710, 45), (1280, 980, 0), (1580, 800, 90), (1470, 945, 270)]]
    open_locs_and_rots = [[(840, 140, 0), (1260, 140, 0), (1030, 1190, 0), (1030, 1190, 0), (1680, 730, 90), (1680, 300, 90), (620, 300, 90), (620, 730, 90)], [(950, 320, 90), (1390, 320, 90), (780, 840, 45), (1300, 850, 135), (1320, 930, 0), (1320, 500, 0), (800, 500, 0), (800, 930, 0)]]

    def __init__(self, widget, color, team_name, x, y):

        full_pm = QtGui.QPixmap(401, 201)
        full_pm.fill(QtGui.QColor(0, 0, 0, 0))

        bot_frame = QtCore.QRectF(0, 0, 401, 201)

        if color == 0:
            bot_pixmap = QtGui.QPixmap("assets/TT_BOT_TOP_RED.png")
            text_frame = QtCore.QRectF(20, 65, 330, 61)
        else:
            bot_pixmap = QtGui.QPixmap("assets/TT_BOT_TOP_BLUE.png")
            text_frame = QtCore.QRectF(60, 65, 330, 61)

        font = QtGui.QFont()
        font.setFamily("Excluded")
        font.setPointSize(34)
        font.setItalic(True)
        
        painter = QtGui.QPainter(full_pm)
        painter.setFont(font)

        painter.drawPixmap(bot_frame, bot_pixmap, QtCore.QRectF(bot_pixmap.rect()))
        if color == 0:
            painter.setPen(QtGui.QPen(QtGui.QColor('#600000')))
            painter.drawText(text_frame, team_name)
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor('#000060')))
            painter.drawText(text_frame, QtCore.Qt.AlignRight, team_name)

        super(Bot, self).__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, 401, 201))
        self.setText("")

        self.setPixmap(full_pm)

        self.original_pixmap = full_pm

        self.setObjectName(team_name)

        #print("Completed bot init")

        painter.end()

    def update_position(self, x, y, rotation):
        transform = QtGui.QTransform().rotate(rotation)
        pixmap = self.original_pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        self.setPixmap(pixmap)
        self.setGeometry(QtCore.QRect(x, y, pixmap.width(), pixmap.height()))


class Cube(QtWidgets.QLabel):

    stack_top_locs = [[(650, 1310), (640, 160), (700, 160)], [(1800, 1310), (1800, 160), (1740, 160)]]
    full_stack_locs = [[(170, 1410), (110, 670), (180, 670)], [(2240, 1380), (2300, 680), (2240, 680)]]
    tower_locs = [(904, 1370), (785, 732), (1225, 410), (1223, 733), (1226, 1058), (1663, 733), (1543, 1370)]

    def __init__(self, widget, color, x, y, name):
        if color == 0:
            cube_pixmap = QtGui.QPixmap("assets/orangecube.png")
        elif color == 1:
            cube_pixmap = QtGui.QPixmap("assets/greencube.png")
        else:
            cube_pixmap = QtGui.QPixmap("assets/purplecube.png")

        super(Cube, self).__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, 51, 51))
        self.setText("")
        self.setScaledContents(True)

        self.setPixmap(cube_pixmap)

        self.setObjectName(name)

        #print("Completed cube init")


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(2522, 1586)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.bgimage = QtWidgets.QLabel(self.centralwidget)
        self.bgimage.setGeometry(QtCore.QRect(0, 0, 2531, 1541))
        self.bgimage.setText("")
        self.bgimage.setPixmap(QtGui.QPixmap("assets/field_smaller.png"))
        self.bgimage.setObjectName("bgimage")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2522, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def align(self):
        ag = QtWidgets.QDesktopWidget().screenGeometry()
        #print(ag)

        widget = self.geometry()
        x = ag.width() / 2 - widget.width()
        y = 320
        self.move(x, y)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def refresh(self):

        #print("Timing!")
        bot1 = self.findChild(QtWidgets.QLabel, "1A")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    bot1 = Bot(ui.centralwidget, 0, '1A', 420, 350)
    bot2 = Bot(ui.centralwidget, 0, '2B', 420, 950)
    bot3 = Bot(ui.centralwidget, 1, '3C', 1670, 350)
    bot4 = Bot(ui.centralwidget, 1, '4D', 1670, 950)
    timer = QtCore.QTimer()
    timer.start(1000)
    timer.timeout.connect(ui.refresh)
    print(timer)
    ui.show()
    #cube = Cube(ui.centralwidget, 0, 790, 730)
    bot1.update_position(620, 730, 90)
    bot2.update_position(800, 930, 0)
    bot4.update_position(710, 800, 90)
    bot3.update_position(1, 840, 135)
    #print(ui.findChildren(QtWidgets.QLabel))
    
    sys.exit(app.exec_())