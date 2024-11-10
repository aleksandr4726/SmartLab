import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from .gistogramma import show_gistogramma_window
from .array_gui import show_array_window
from .chart_gui import show_chart_window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка основного окна
        self.setWindowTitle("Выбор действия")
        self.setGeometry(100, 100, 300, 200)

        # Создание виджета для кнопок
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание вертикального layout и кнопок
        layout = QVBoxLayout()
        self.button1 = QPushButton("Обработка массивов")
        self.button2 = QPushButton("Построение графика")
        self.button3 = QPushButton("Визуализация данных")

        # Изменение толщины кнопок с помощью QSS
        button_style = """
            QPushButton {
                height: 50px;  /* Высота кнопок */
                padding: 10px; /* Внутренние отступы */
            }
        """
        self.button1.setStyleSheet(button_style)
        self.button2.setStyleSheet(button_style)
        self.button3.setStyleSheet(button_style)

        # Добавление кнопок в layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        # Назначение layout центральному виджету
        central_widget.setLayout(layout)

        # Подключение кнопок к методам для обработки нажатий
        self.button1.clicked.connect(self.on_button1_click)
        self.button2.clicked.connect(self.on_button2_click)
        self.button3.clicked.connect(self.on_button3_click)

        # Атрибут для второго окна, чтобы оно не закрывалось
        self.second_window = None

    # Методы для обработки нажатий кнопок
    def on_button1_click(self):
        self.close()
        self.array_window = show_array_window()

    def on_button2_click(self):
        self.close()
        self.chart_window = show_chart_window()

    def on_button3_click(self):
        # Закрытие текущего окна и открытие второго окна
        self.close()
        self.gistogramma_window = show_gistogramma_window()

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
