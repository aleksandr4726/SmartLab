import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


# Функция для создания второго окна (gistogramma)
def show_gistogramma_window():
    gistogramma_window = QMainWindow()
    gistogramma_window.setWindowTitle("Второе окно")
    gistogramma_window.setGeometry(100, 200, 800, 600)

    central_widget = QWidget(gistogramma_window)
    gistogramma_window.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)
    label = QLabel("Гистограмма", central_widget)
    layout.addWidget(label)

    button1 = QPushButton("Ввести данные из файла")
    button2 = QPushButton("Ввести данные вручную")

    layout.addWidget(button1)
    layout.addWidget(button2)

    button1.clicked.connect(lambda: clear_window(gistogramma_window, "Ввод данных из файла"))
    button2.clicked.connect(lambda: clear_window(gistogramma_window, "Ввод данных вручную"))

    gistogramma_window.show()
    return gistogramma_window


def clear_window(window, message):
    """Очищает содержимое окна и добавляет сообщение."""
    # Очищаем центральный виджет
    central_widget = window.centralWidget()
    layout = central_widget.layout()

    # Удаляем все виджеты из компоновки
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    # Добавляем новое сообщение
    label = QLabel("", central_widget)
    layout.addWidget(label)


# Главное окно с кнопкой для открытия второго окна
class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 400, 300)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создаем кнопку для открытия второго окна
        self.open_gistogramma_button = QPushButton("Открыть второе окно", self)
        layout.addWidget(self.open_gistogramma_button)

        # Подключаем кнопку к функции открытия второго окна
        self.open_gistogramma_button.clicked.connect(show_gistogramma_window)

