import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]
coord1 = float(input())
coord2 = float(input())
size = float(input())


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = 'map.png'
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.getImage()

    def getImage(self):
        print(size)
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord1},{coord2}&spn={size},{size}&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.change_pic()

    def change_pic(self):
        pixmap = QPixmap(self.map_file)
        self.image.setPixmap(pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        global size
        if event.key() == Qt.Key_PageDown and size > 0.001:
            size -= 0.001
        if event.key() == Qt.Key_PageUp:
            size += 0.001
            print(size)
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())