"""
Пример карусели для выбора конкретной модели одежды.
Для скролла можно использовать стрелки на клавиатруре (вправо, влево), мышку.
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl

if __name__ == '__main__':

    app = QApplication()
    view = QQuickWidget()

    view.setSource(QUrl("source/Carousel.qml"))
    print(view.errors())
    view.show()
    sys.exit(app.exec())