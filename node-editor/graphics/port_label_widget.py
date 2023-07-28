from PySide2 import QtCore, QtWidgets, QtGui


class PortLabelWidget(QtWidgets.QWidget):
    def __init__(self, label : str, alignment="left"):
        super().__init__()
        self.alignment = alignment
        self.label_name = label
        self.create_widgets()
        self.create_ui_layout()

    def create_widgets(self):
        self.text_label = QtWidgets.QLabel(self.label_name)
        self.text_edit = QtWidgets.QLineEdit()
        self.text_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.text_edit.setFixedWidth(60)
        self.text_edit.setFixedHeight(25)
        self.text_label.setStyleSheet("color: #FFFFFF;")
        self.text_edit.setStyleSheet(
                        "color: #FFFFFF;"
                        "border-radius: 5px;"
                        "background-color: #262626;"
                        "border-style: none;");
        self.setStyleSheet("background-color: transparent;")

    def create_ui_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 0)

        if self.alignment == "left":
            main_layout.addWidget(self.text_label)
            main_layout.addWidget(self.text_edit)
            main_layout.addStretch()

        if self.alignment == "right":   
            main_layout.addStretch()
            main_layout.addWidget(self.text_edit)
            main_layout.addWidget(self.text_label)
            self.text_edit.setStyleSheet(
                            "color: #9c9c9c;"
                            "font-weight: bold;"
                            "border-radius: 5px;"
                            "background-color: #383838;"
                            "border-style: none;");
