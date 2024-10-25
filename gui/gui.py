from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from first_area import FirstWorkArea
from action_1 import create_table_in_first_area
from action_2 import *
from action_3 import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SmartLab")
        self.setGeometry(100, 100, 1200, 700)  # Положение и размер окна

        # Основной лэйаут
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Отступы для всего окна
        layout.setSpacing(0)  # Устанавливаем интервал между элементами на 0

        # Лэйаут для кнопок
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)  # Отступы между кнопками

        # Создаем кнопки
        self.button1 = QPushButton("ОБРАБОТКА\n\nДАННЫХ")
        self.button2 = QPushButton("ГРАФИК")
        self.button3 = QPushButton("ДРУГАЯ\n\nВИЗУАЛИЗАЦИЯ\n\nДАННЫХ")

        # Устанавливаем фиксированную ширину кнопок
        self.button1.setFixedSize(100, 150)
        self.button2.setFixedSize(100, 150)
        self.button3.setFixedSize(100, 150)

        # Добавляем кнопки в лэйаут
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)

        # Создаем рабочие зоны
        self.first_work_area = FirstWorkArea()

        # Соединяем кнопки с функциями
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3.clicked.connect(self.on_button3_clicked)

        # Добавляем лэйауты в основной
        layout.addLayout(button_layout)
        layout.addWidget(self.first_work_area)  # Первая рабочая зона

        self.setLayout(layout)

    def clear_all_layouts(widget):
        """Удаляет все лэйауты и виджеты из указанного виджета"""
        layout = widget.layout()

        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)

                if child.widget():
                    # Удаляем виджет
                    child.widget().deleteLater()
                elif child.layout():
                    # Рекурсивно очищаем вложенные лэйауты
                    clear_all_layouts(child.layout())

            # Удаляем сам лэйаут у виджета
            widget.setLayout(None)

    def update_first_area(first_work_area):
        # Очищаем все лэйауты и виджеты из first_area
        clear_all_layouts(first_work_area)

        # Создаем новый лэйаут или виджеты
        new_layout = QVBoxLayout()
        label = QLabel("Новый элемент")
        new_layout.addWidget(label)

        first_work_area.setLayout(new_layout)

    def on_button1_clicked(self):
        clear_all_layouts(self.first_work_area)
    def on_button2_clicked(self):
        self.clear_work_areas()

    def on_button3_clicked(self):
        self.clear_work_areas()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
