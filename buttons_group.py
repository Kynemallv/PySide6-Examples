"""
Пример виджета с кнопками для выбора типа одежды.
Чтобы пролистать на следующий тип, следует зажать кнопку.
"""

import sys
import pathlib

from typing import NamedTuple, TypeVar
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtStateMachine import QFinalState, QState, QStateMachine


PathLike = TypeVar("PathLike", str, pathlib.Path)


class ItemClothing(NamedTuple):
    name: str
    icon: PathLike


class Clothes(QState):
    def __init__(self, childs: list[ItemClothing], button: QPushButton,
                 parent: QState | None = None) -> None:
        super(Clothes, self).__init__(parent=parent)

        self.childs = []
        self.button = button
        self.timer = QTimer()

        self.button.pressed.connect(self._on_press)
        self.button.released.connect(self._on_release)

        if childs:
            for child in childs:
                self.add_child(child_info=child)
                self.childs.append(self.get_child(child.name))
        else:
            raise ValueError

        self.setInitialState(self.childs[0])

    def add_child(self, child_info: ItemClothing):
        child = QState(self)
        child.setObjectName(child_info.name)

        icon = QIcon(child_info.icon)
        child.assignProperty(self.button, 'icon', icon)

        if self.childs:
            previous_child = self.childs[-1]

            previous_child.removeTransition(previous_child.transitions()[0])
            previous_child.addTransition(self.timer.timeout, child)
            child.addTransition(self.timer.timeout, self.childs[0])
        else:
            child.addTransition(self.timer.timeout, child)

        self.childs.append(child)
        setattr(self, child_info.name, child)

    def get_child(self, child_name):
        return self.__getattribute__(child_name)

    def del_child(self, child_name):
        if isinstance(self.get_child(child_name), QState):
            delattr(self, child_name)

    def _on_press(self):
        self.timer.start(700)

    def _on_release(self):
        self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_widget = QWidget()

    main_widget.setLayout(QVBoxLayout())

    button1 = QPushButton()
    button2 = QPushButton()

    button1.resize(200, 200)
    button1.setIconSize(QSize(100, 100))
    button2.resize(QSize(100, 100))
    button2.setIconSize(QSize(100, 100))

    main_widget.layout().addWidget(button1)
    main_widget.layout().addWidget(button2)

    machine = QStateMachine()

    main_state = QState(childMode=QState.ChildMode.ParallelStates)
    upper = Clothes(
        [ItemClothing('hat', 'source/textures/i.jpeg'), ItemClothing('panama', 'source/textures/panama.jpeg')],
        button1,
        parent=main_state
    )
    lower = Clothes(
        [ItemClothing('hat', 'source/textures/i.jpeg'), ItemClothing('panama', 'source/textures/panama.jpeg')],
        button2,
        parent=main_state
    )

    machine.addState(main_state)
    machine.setInitialState(main_state)
    machine.start()

    main_window.setCentralWidget(main_widget)
    main_window.show()

    sys.exit(app.exec())
