from PyQt5.QtGui import QPixmap, QIcon, QFont, QCloseEvent
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QIODevice, QObject, QRunnable, pyqtSignal, QThreadPool
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QApplication, QMessageBox, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget

import sys

import cameraStream
import Perco_API


class MyMessageBox(QWidget):
    def __init__(self, flag):
        super(MyMessageBox, self).__init__()

        self.flag = flag
        self.initUI()

    def initUI(self):
        if self.flag:
            self.msg = QMessageBox(QMessageBox.Icon.Warning, "Операция совершена успешно!", "Операция прошла успешно!\n\n", buttons=QMessageBox.Ok)
            self.msg.setIconPixmap((QPixmap("icons//msgok.png").scaled(60, 60)))
            self.setWindowTitle("Ошибок нет :)")
            self.setWindowIcon(QIcon("icons//msgoktitle.png"))
        else:
            self.msg = QMessageBox(QMessageBox.Icon.Warning, "Что-то пошло не так :(", "Ошибка при отправке данных!\nПопробуйте еще раз!\n", buttons=QMessageBox.Ok)
            self.setWindowTitle("Что-то пошло не так :(")
            self.setWindowIcon(QIcon("icons//msgerrortitle.png"))
        self.msg.button(QMessageBox.Ok).clicked.connect(self.bc)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.msg)
        self.setLayout(self.layout)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #FFFFFF")
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.show()

    def bc(self):
        self.close()


class ChooseDPA(QWidget):
    def __init__(self, parent):
        super(ChooseDPA, self).__init__()

        self.parent = parent

        self.choosen_item = ""
        self.searchlist = []

        self.initUI()

    def initUI(self):

        main_layout = QVBoxLayout()

        head_layout = QVBoxLayout()
        sub_head_layout = QHBoxLayout()
        sub_head_layout.setSpacing(0)

        self.head_lbl = QLabel()
        self.head_lbl.setFont(QFont("Times", 16))
        find_lbl = QLabel()
        find_lbl.setPixmap(QPixmap("icons//loupe.jpeg").scaled(40, 40))
        find_lbl.setStyleSheet("background-color: #FFFFFF")
        self.le = QLineEdit()
        self.le.setPlaceholderText("Поиск")
        self.le.setFont(QFont("Times", 14))
        self.le.setFixedSize(500, 40)
        self.le.setStyleSheet("border-style: solid")
        self.le.textChanged.connect(self.update_search_le)

        sub_head_layout.addWidget(find_lbl)
        sub_head_layout.addWidget(self.le)

        head_layout.addWidget(self.head_lbl)
        head_layout.addLayout(sub_head_layout)

        self.list = QListWidget()
        self.list.itemClicked.connect(self.choose_item)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFont(QFont("Times", 14))
        self.save_btn.setFixedSize(100, 50)
        self.save_btn.setStyleSheet("background-color: #6298C8")

        main_layout.addLayout(head_layout)
        main_layout.addWidget(self.list)
        main_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)

        self.setLayout(main_layout)
        self.setWindowIcon(QIcon("icons//pdatitle.png"))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.show()

    def choose_item(self, item):
        self.choosen_item = item.text()

    def update_search_le(self):
        new_search_list = []
        search_list_for_display = []

        for item in self.searchlist:
            if self.le.text().lower() in item.lower():
                new_search_list.append(item)

        self.list.clear()
        self.list.addItems(new_search_list)
        new_search_list.clear()


class CameraScreen(QWidget):
    def __init__(self, parent):
        super(CameraScreen, self).__init__()

        self.initUI()

        self.parent = parent
        self.thread = None
        self.startStream()

        #self.stream = cameraStream.CameraStream(self)
        #self.stream.changePixmap.connect(self.showStream)
        #self.stream.start()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 15)

        self.image_lbl = QLabel("CAMERA STREAM")
        self.image_lbl.setFixedSize(940, 600)

        self.screen_btn = QPushButton("Сделать снимок")
        self.screen_btn.setFont(QFont("Times", 16))
        self.screen_btn.setFixedSize(200, 60)
        self.screen_btn.setStyleSheet("background-color: #6298C8")

        self.change_camera_btn = QPushButton("Поменять камеру")
        self.change_camera_btn.setFont(QFont("Times", 16))
        self.change_camera_btn.setFixedSize(200, 60)
        self.change_camera_btn.setStyleSheet("background-color: #6298C8")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.screen_btn, 1, alignment=Qt.AlignVCenter)
        button_layout.addWidget(self.change_camera_btn, 1, alignment=Qt.AlignVCenter)

        main_layout.addWidget(self.image_lbl, 4, alignment=Qt.AlignHCenter)
        main_layout.addLayout(button_layout)

        #main_layout.addWidget(self.screen_btn, 1, alignment=Qt.AlignHCenter)

        self.setGeometry(600, 300, 640, 560)
        self.setWindowTitle("PhotkaemRoju")
        self.setWindowIcon(QIcon("icons//cameratitle.png"))
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #C3FC94")
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.show()

    def startStream(self):
        #self.thread = cameraStream.CameraStream(self)
        #self.thread.changePixmap.connect(self.showStream)
        #self.thread.start()

        self.thread = cameraStream.ThreadClass(parent=None)
        self.thread.any_signal.connect(self.showStream)
        self.thread.start()

    def showStream(self, img):
        self.image_lbl.setPixmap(QPixmap(img).scaled(self.image_lbl.size()))

    def closeEvent(self, event: QCloseEvent) -> None:
        #self.thread.terminate()
        #self.thread = None
        self.thread.stop()


class PercoSignals(QObject):
    result = pyqtSignal(object)


class PercoWorker(QRunnable):

    def __init__(self, _user):
        super(PercoWorker, self).__init__()

        self.signals = PercoSignals()
        self.user = _user

    def run(self):
        self.signals.result.emit(Perco_API.main(self.user))


class DobavlyaemRoju(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DobavlyaemRoju, self).__init__(*args, **kwargs)

        self.user = Perco_API.User()

        self.initUI()
        self.mainWindow = QStackedWidget()
        self.threadpool = QThreadPool()

        self.searchlist = []

    def initUI(self):
        # главное окно для ввода данных
        inputWindow = QVBoxLayout()
        inputWindow.setContentsMargins(0, 0, 0, 0)

        # контейнер для всех widgets входных данных
        userDataContainer = QHBoxLayout()

        # левая часть окна с полями для ввода текстовых данных
        userDataLeftLayout = QVBoxLayout()

        # правая часть окна для загрузки изображения
        userImageLayout = QVBoxLayout()
        userImageLayout.setContentsMargins(5, 0, 5, 0)

        # верхняя часть окна
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #6298C8")
        headerLayout = QHBoxLayout()

        # нижняя часть окна с кнопками
        button_widget = QWidget()
        button_widget.setStyleSheet("background-color: #5DB5CE")
        buttonLayout = QHBoxLayout()

# !-----label'ы и поля ввода для userDataLeftLayout---------------------------
        last_name_lbl = QLabel("Фамилия")
        last_name_lbl.setFont(QFont("Times", 12))
        first_name_lbl = QLabel("Имя")
        first_name_lbl.setFont(QFont("Times", 12))
        middle_name_lbl = QLabel("Отчество")
        middle_name_lbl.setFont(QFont("Times", 12))

        division_lbl = QLabel("Подразделение")
        division_lbl.setFont(QFont("Times", 12))
        position_lbl = QLabel("Должность")
        position_lbl.setFont(QFont("Times", 12))
        access_template_lbl = QLabel("Шаблон доступа")
        access_template_lbl.setFont(QFont("Times", 12))

        self.last_name_le = QLineEdit()
        self.last_name_le.setFont(QFont("Times", 14))
        self.last_name_le.setFixedSize(200, 40)
        self.first_name_le = QLineEdit()
        self.first_name_le.setFont(QFont("Times", 14))
        self.first_name_le.setFixedSize(200, 40)
        self.middle_name_le = QLineEdit()
        self.middle_name_le.setFont(QFont("Times", 14))
        self.middle_name_le.setFixedSize(200, 40)

        self.division_le = QLineEdit()
        self.division_le.setFont(QFont("Times", 14))
        self.division_le.setFixedSize(200, 40)
        self.division_le.setReadOnly(True)
        self.position_le = QLineEdit()
        self.position_le.setFont(QFont("Times", 14))
        self.position_le.setFixedSize(200, 40)
        self.position_le.setReadOnly(True)
        self.access_template_le = QLineEdit()
        self.access_template_le.setText("Базовый")
        self.access_template_le.setFont(QFont("Times", 14))
        self.access_template_le.setFixedSize(200, 40)
        self.access_template_le.setReadOnly(True)

        division_btn = QPushButton()
        division_btn.setFixedSize(40, 40)
        division_btn.setStyleSheet("background-color: #6298C8")
        division_btn.clicked.connect(self.openDivisionList)

        position_btn = QPushButton()
        position_btn.setFixedSize(40, 40)
        position_btn.setStyleSheet("background-color: #6298C8")
        position_btn.clicked.connect(self.openPositionList)

        access_template_btn = QPushButton()
        access_template_btn.setFixedSize(40, 40)
        access_template_btn.setStyleSheet("background-color: #6298C8")
        access_template_btn.clicked.connect(self.openAccessTemplateList)

        icon_btn = QIcon(QPixmap("icons//list.png"))

        division_btn.setIcon(icon_btn)
        position_btn.setIcon(icon_btn)
        access_template_btn.setIcon(icon_btn)
# !---------------------------------------------------------------------------

# !-----widgets для userImageLayout-------------------------------------------
        image_lbl = QLabel("Фотография")
        image_lbl.setFont(QFont("Times", 14))
        self.user_face_lbl = QLabel()
        self.user_face_lbl.setFixedSize(600, 500)
        null_lbl = QLabel("\n")
        change_image_bnt = QPushButton()
        change_image_bnt.setFixedSize(100, 40)
        change_image_bnt.clicked.connect(self.openCamera)
# !---------------------------------------------------------------------------

# !---------------------------------------------------------
        add_user_lbl = QLabel("Добавить сотрудника")
        add_user_lbl.setFont(QFont("Times", 18))
        dt_lbl = QLabel("_________Учетные данные________________________________________________________\n")
        dt_lbl.setFont(QFont("Times", 14))
        add_user_btn = QPushButton("Отправить в базу")
        add_user_btn.clicked.connect(self.addUser)
        add_user_btn.setFixedSize(240, 60)
        add_user_btn.setFont(QFont("Times", 16))
        add_user_btn.setStyleSheet("background-color: #6298C8")
        refresh_token_btn = QPushButton("Обновить токен")
        refresh_token_btn.clicked.connect(self.refresh_token)
        refresh_token_btn.setFixedSize(240, 60)
        refresh_token_btn.setFont(QFont("Times", 16))
        refresh_token_btn.setStyleSheet("background-color: #6298C8")

# !-----layout для полей с label'-ами-----------------------------------------
        fio_data_main_layout = QHBoxLayout()
        fio_data_main_layout.setContentsMargins(15, 5, 5, 10)

        last_name_layout = QVBoxLayout()
        last_name_layout.setContentsMargins(15, 0, 0, 15)
        first_name_layout = QVBoxLayout()
        first_name_layout.setContentsMargins(15, 0, 0, 15)
        middle_name_layout = QVBoxLayout()
        middle_name_layout.setContentsMargins(15, 0, 0, 15)

        last_name_layout.addWidget(last_name_lbl)
        last_name_layout.addWidget(self.last_name_le)
        #last_name_layout.addStretch(1)

        first_name_layout.addWidget(first_name_lbl)
        first_name_layout.addWidget(self.first_name_le)
        #first_name_layout.addStretch(1)

        middle_name_layout.addWidget(middle_name_lbl)
        middle_name_layout.addWidget(self.middle_name_le)
        #middle_name_layout.addStretch(1)

        fio_data_main_layout.addLayout(last_name_layout)
        fio_data_main_layout.addLayout(first_name_layout)
        fio_data_main_layout.addLayout(middle_name_layout)
        fio_data_main_layout.addStretch(1)
# !---------------------------------------------------------------------------

# !-----layout для полей с доп. данными---------------------------------------
        other_user_data_main_layout = QHBoxLayout()
        other_user_data_main_layout.setContentsMargins(15, 5, 5, 10)

        division_layout = QVBoxLayout()
        division_layout.setContentsMargins(15, 0, 0, 15)
        position_layout = QVBoxLayout()
        position_layout.setContentsMargins(15, 0, 0, 15)
        access_template_layout = QVBoxLayout()
        access_template_layout.setContentsMargins(15, 0, 0, 15)

        sub_division_layout = QHBoxLayout()
        sub_division_layout.setSpacing(0)
        sub_position_layout = QHBoxLayout()
        sub_position_layout.setSpacing(0)
        sub_access_template_layout = QHBoxLayout()
        sub_access_template_layout.setSpacing(0)

        sub_division_layout.addWidget(self.division_le)
        sub_division_layout.addWidget(division_btn)

        sub_position_layout.addWidget(self.position_le)
        sub_position_layout.addWidget(position_btn)

        sub_access_template_layout.addWidget(self.access_template_le)
        sub_access_template_layout.addWidget(access_template_btn)

        division_layout.addWidget(division_lbl)
        division_layout.addLayout(sub_division_layout)

        position_layout.addWidget(position_lbl)
        position_layout.addLayout(sub_position_layout)
        position_layout.addStretch(1)

        access_template_layout.addWidget(access_template_lbl)
        access_template_layout.addLayout(sub_access_template_layout)
        access_template_layout.addStretch(1)

        other_user_data_main_layout.addLayout(division_layout)
        other_user_data_main_layout.addLayout(position_layout)
        other_user_data_main_layout.addLayout(access_template_layout)
# !-------------------------------------------------------------------------------------------

# !-----userImageLayout-----------------------------------------------------------------------
        self.user_face_lbl.setPixmap(QPixmap("icons//face.png").scaled(self.user_face_lbl.size()))
        change_image_bnt.setIcon(QIcon(QPixmap("icons//camera.png")))
        change_image_bnt.setIconSize(change_image_bnt.size())
        change_image_bnt.setStyleSheet("background-color: #6298C8")

        userImageLayout.addWidget(image_lbl)
        userImageLayout.addWidget(self.user_face_lbl)
        userImageLayout.addWidget(change_image_bnt, alignment=Qt.AlignCenter)
        userImageLayout.addWidget(null_lbl)
# !-------------------------------------------------------------------------------------------

# !-----headers-------------------------------------------------------------------------------
        headerLayout.addWidget(add_user_lbl, alignment=Qt.AlignVCenter)
# !-------------------------------------------------------------------------------------------

# !-----buttonLayout--------------------------------------------------------------------------
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(add_user_btn, alignment=Qt.AlignCenter)
        buttonLayout.addWidget(refresh_token_btn, alignment=Qt.AlignCenter)
        buttonLayout.addStretch(1)
# !-------------------------------------------------------------------------------------------

        userDataLeftLayout.addLayout(fio_data_main_layout)
        userDataLeftLayout.addWidget(dt_lbl)
        userDataLeftLayout.addLayout(other_user_data_main_layout)
        userDataLeftLayout.addStretch(1)

        userDataContainer.addLayout(userDataLeftLayout, 3)
        userDataContainer.addLayout(userImageLayout, 1)

        header_widget.setLayout(headerLayout)
        inputWindow.addWidget(header_widget)
        inputWindow.addLayout(userDataContainer)
        button_widget.setLayout(buttonLayout)
        inputWindow.addWidget(button_widget)

        widget = QWidget()
        widget.setLayout(inputWindow)
        self.setGeometry(450, 250, 1315, 600)
        self.setWindowTitle("DobavlyaemRoju")
        self.setWindowIcon(QIcon("icons//titleicon.png"))
        self.setStyleSheet("background-color: white")
        self.setCentralWidget(widget)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.show()

    def openCamera(self):
        self.screen_window = None
        self.screen_window = CameraScreen(self)
        self.screen_window.screen_btn.clicked.connect(self.setFaceImage)
        #self.screen_window.closeEvent.connect(self.closecamerastream)

    def setFaceImage(self):
        self.user_face_lbl.setPixmap(self.screen_window.image_lbl.pixmap().scaled(self.user_face_lbl.size(), Qt.KeepAspectRatio))

    def openDivisionList(self):
        self.dl = ChooseDPA(self)
        self.dl.head_lbl.setText("Выбрать подразделение")
        self.dl.searchlist = Perco_API.getDivisionList()
        self.dl.list.addItems(self.dl.searchlist)
        self.dl.save_btn.clicked.connect(self.setDivision)

    def setDivision(self):
        self.division_le.setText(self.dl.choosen_item)
        self.dl.close()

    def openPositionList(self):
        self.dl = ChooseDPA(self)
        self.dl.head_lbl.setText("Выбрать должность")
        self.dl.searchlist = Perco_API.getPositionList()
        self.dl.list.addItems(self.dl.searchlist)
        self.dl.save_btn.clicked.connect(self.setPosition)

    def setPosition(self):
        self.position_le.setText(self.dl.choosen_item)
        self.dl.close()

    def openAccessTemplateList(self):
        self.dl = ChooseDPA(self)
        self.dl.head_lbl.setText("Выбрать шаблон доступа")
        self.dl.searchlist = Perco_API.getAccessTemplateList()
        self.dl.list.addItems(self.dl.searchlist)
        self.dl.save_btn.clicked.connect(self.setAccessTemplate)

    def setAccessTemplate(self):
        self.access_template_le.setText(self.dl.choosen_item)
        self.dl.close()

    def addUser(self):
        self.user.fio = self.last_name_le.text() + " " + self.first_name_le.text() + " " + self.middle_name_le.text()
        self.user.division_name = self.division_le.text()
        self.user.position_name = self.position_le.text()
        self.user.access_template = self.access_template_le.text()

        pixmap = self.user_face_lbl.pixmap()
        bytes = QByteArray()
        buffer = QBuffer(bytes)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "JPG")
        encoded = b'data:image/jpeg;base64,' + buffer.data().toBase64()
        s = str(encoded, "UTF-8")
        self.user.image = s

        percoworker = PercoWorker(self.user)
        percoworker.signals.result.connect(self.resultUpdateDB)
        self.threadpool.start(percoworker)

        self.last_name_le.clear()
        self.first_name_le.clear()
        self.middle_name_le.clear()

        #self.division_le.clear()
        #self.position_le.clear()
        #self.access_template_le.clear()

        self.user_face_lbl.setPixmap(QPixmap("icons//face.png").scaled(500, 500))

    def refresh_token(self):
        Perco_API.refresh_token()

    def resultUpdateDB(self, flag):
        if flag:
            self.msg = MyMessageBox(True)
        else:
            self.msg = MyMessageBox(False)


def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    #window = MyMessageBox(True)
    window = DobavlyaemRoju()
    #window = CameraScreen()

    app.exec_()


if __name__ == '__main__':
    main()