import typing
from PySide2.QtCore import *
import PySide2.QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import PySide2.QtWidgets


class PortLabelWidget(QWidget):
    def __init__(self, label : str, alignment="left"):
        super().__init__()
        self.alignment = alignment
        self.label_name = label
        self.create_widgets()
        self.create_ui_layout()

    def create_widgets(self):
        self.text_label = QLabel(self.label_name)
        self.text_edit = QLineEdit()
        self.text_edit.setFixedWidth(40)
        self.setStyleSheet("background-color: transparent; color: white;")

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 0)

        if self.alignment == "left":
            main_layout.addWidget(self.text_label)
            main_layout.addWidget(self.text_edit)
            main_layout.addStretch()

        if self.alignment == "right":
            main_layout.addStretch()
            main_layout.addWidget(self.text_edit)
            main_layout.addWidget(self.text_label)
