# first_window.py
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox
)
from array_gui import ArrayWindow  # Импортируем класс из array_gui.py
from chart_gui import ChartWindow  # Импортируем класс из chart_gui.py
from gistogramma import GistogrammaWindow  # Импортируем класс из gistogramma.py


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка основного окна
        self.setWindowTitle("Выбор действия")
        self.setGeometry(100, 100, 300, 200)

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание вертикального layout и кнопок
        layout = QVBoxLayout()
        self.button_first = QPushButton("Обработка массивов")
        self.button_second = QPushButton("Построение графика")
        self.button_third = QPushButton("Визуализация данных")

        # Изменение стиля кнопок с помощью QSS
        button_style = """
            QPushButton {
                height: 50px;  /* Высота кнопок */
                padding: 10px; /* Внутренние отступы */
            }
        """
        self.button_first.setStyleSheet(button_style)
        self.button_second.setStyleSheet(button_style)
        self.button_third.setStyleSheet(button_style)

        # Добавление кнопок в layout
        layout.addWidget(self.button_first)
        layout.addWidget(self.button_second)
        layout.addWidget(self.button_third)

        # Назначение layout центральному виджету
        central_widget.setLayout(layout)

        # Подключение кнопок к методам для обработки нажатий
        self.button_first.clicked.connect(self.open_array_window)
        self.button_second.clicked.connect(self.open_chart_window)
        self.button_third.clicked.connect(self.open_gistogramma_window)

        # Атрибуты для дополнительных окон
        self.array_window = None
        self.chart_window = None
        self.gistogramma_window = None

    # Метод для открытия окна обработки массивов
    def open_array_window(self):
        """Открывает окно обработки массивов."""
        if self.array_window is None or not self.array_window.isVisible():
            self.array_window = ArrayWindow(main_window=self)  # Передаём ссылку на главное окно
            self.array_window.show()
            self.hide()  # Скрываем главное окно

    # Метод для открытия окна построения графика
    def open_chart_window(self):
        """Открывает окно построения графика."""
        try:
            if self.chart_window is None or not self.chart_window.isVisible():
                self.chart_window = ChartWindow(main_window=self)  # Передаём ссылку на главное окно
                self.chart_window.show()
                self.hide()
        except ImportError:
            QMessageBox.warning(self, "Ошибка", "Модуль chart_gui не найден.")

    # Метод для открытия окна визуализации данных (гистограмма)
    def open_gistogramma_window(self):
        """Открывает окно визуализации данных (гистограмма)."""
        try:
            if self.gistogramma_window is None or not self.gistogramma_window.isVisible():
                self.gistogramma_window = GistogrammaWindow(main_window=self)  # Передаём ссылку на главное окно
                self.gistogramma_window.show()
                self.hide()
        except ImportError:
            QMessageBox.warning(self, "Ошибка", "Модуль gistogramma не найден.")

    # Метод для возврата в главное окно
    def show_main_window(self):
        """Показывает главное окно."""
        self.show()


def run_app():
    """Запуск приложения."""
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
