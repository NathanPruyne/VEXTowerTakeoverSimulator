from PyQt5 import QtCore, QtGui, QtWidgets

class Bot(QtWidgets.QLabel):
    def __init__(self, widget, color, team_name, x, y):

        full_pm = QtGui.QPixmap(401, 201)
        full_pm.fill(QtGui.QColor(0, 0, 0, 0))

        bot_frame = QtCore.QRectF(0, 0, 401, 201)

        if color == 0:
            bot_pixmap = QtGui.QPixmap("assets/TT_BOT_TOP_RED.png")
            text_frame = QtCore.QRectF(20, 65, 261, 61)
        else:
            bot_pixmap = QtGui.QPixmap("assets/TT_BOT_TOP_BLUE.png")
            text_frame = QtCore.QRectF(150, 65, 261, 61)

        font = QtGui.QFont()
        font.setFamily("Excluded")
        font.setPointSize(22)
        font.setItalic(True)
        
        painter = QtGui.QPainter(full_pm)
        painter.setFont(font)

        painter.drawPixmap(bot_frame, bot_pixmap, QtCore.QRectF(bot_pixmap.rect()))
        if color == 0:
            painter.setPen(QtGui.QPen(QtGui.QColor('#600000')))
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor('#000060')))
        painter.drawText(text_frame, team_name)

        super(Bot, self).__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, 401, 201))
        self.setText("")

        self.setPixmap(full_pm)

        self.setObjectName(team_name)

        #print("Completed bot init")

        painter.end()

class Cube(QtWidgets.QLabel):
    def __init__(self, widget, color, x, y):
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

        self.setObjectName("cube" + str(x) + "_" + str(y))

        print("Completed cube init")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2522, 1586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.bgimage = QtWidgets.QLabel(self.centralwidget)
        self.bgimage.setGeometry(QtCore.QRect(0, 0, 2531, 1541))
        self.bgimage.setText("")
        self.bgimage.setPixmap(QtGui.QPixmap("assets/field_smaller.png"))
        self.bgimage.setObjectName("bgimage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2522, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    bot1 = Bot(ui.centralwidget, 0, '1A', 420, 350)
    bot2 = Bot(ui.centralwidget, 0, '2B', 420, 950)
    bot3 = Bot(ui.centralwidget, 1, '3C', 1670, 350)
    bot4 = Bot(ui.centralwidget, 1, '4D', 1670, 950)
    cube = Cube(ui.centralwidget, 0, 790, 730)
    MainWindow.show()
    sys.exit(app.exec_())
