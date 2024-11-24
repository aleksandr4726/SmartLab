# array_gui.py
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QTableWidget, QMessageBox, QScrollArea, QLabel
)
from PyQt6.QtCore import Qt

from data_processing.array_analys import Array  # Убедитесь, что путь корректен


class ArrayWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Ссылка на главное окно
        self.setWindowTitle("Обработка массива")
        self.setGeometry(100, 200, 800, 600)

        self.table = None
        self.table_label = None
        self.add_column_button = None
        self.scroll_area = None  # Добавляем атрибут для ScrollArea

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Создание кнопок
        self.button_load_file = QPushButton("Ввести данные из файла")
        self.button_manual_input = QPushButton("Ввести данные вручную")
        self.button_display_data = QPushButton("Вывести данные")
        self.button_back = QPushButton("Назад")  # Кнопка "Назад"

        # Добавление кнопок в лэйаут
        self.layout.addWidget(self.button_load_file)
        self.layout.addWidget(self.button_manual_input)
        self.layout.addWidget(self.button_display_data)
        self.layout.addWidget(self.button_back)  # Добавление кнопки "Назад"

        # Добавляем пространство между кнопками и остальными элементами
        self.layout.addStretch()

        # QLabel для отображения информации
        self.table_label = QLabel("")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.table_label)

        # Подключаем кнопки к методам
        self.button_load_file.clicked.connect(self.load_data_from_file)
        self.button_manual_input.clicked.connect(self.manual_input)
        self.button_display_data.clicked.connect(self.display_data)
        self.button_back.clicked.connect(self.go_back)  # Подключаем кнопку "Назад"

    def go_back(self):
        """Возвращает в главное окно."""
        if self.main_window:
            self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем текущее окно

    def load_data_from_file(self):
        """Загружает данные из файла и отображает их."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Все файлы (*.*)"
        )
        if not file_path:
            return  # Пользователь отменил выбор файла

        try:
            with open(file_path, 'r') as file:
                data_line = file.readline().strip()
                data = data_line.split()  # Разделение по пробелам
                if data:
                    try:
                        data = [float(item) for item in data]
                        print(f"Загруженные данные: {data}")
                        # Создаём объект Array и получаем статистику
                        arr = Array(data)
                        stats = arr.get_statistics()
                        self.set_info(stats)
                    except ValueError:
                        QMessageBox.information(
                            self, "Данные", "Вы ввели неправильные данные."
                        )
                else:
                    QMessageBox.warning(
                        self, "Ввод из файла", "Файл пустой."
                    )
        except Exception as e:
            QMessageBox.warning(
                self, "Ввод из файла", f"Произошла ошибка: {e}"
            )

    def manual_input(self):
        """Позволяет пользователю вводить данные вручную через таблицу."""
        # Очистка существующих виджетов, кроме кнопок и QLabel
        self.clear_table_widgets()

        # Создание таблицы для ввода данных
        self.table = QTableWidget(self)
        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.setColumnWidth(0, 60)
        self.table.setRowHeight(0, 120)

        # Добавление таблицы в ScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.table)
        self.scroll_area.setMaximumHeight(150)

        # Кнопка для добавления колонок
        self.add_column_button = QPushButton("Добавить колонку")
        self.add_column_button.clicked.connect(self.add_new_column)

        # Добавление виджетов в лэйаут
        self.layout.addWidget(self.add_column_button)
        self.layout.addWidget(self.scroll_area)

    def add_new_column(self):
        """Добавляет новую колонку в таблицу."""
        if self.table is None:
            return

        current_column_count = self.table.columnCount()
        self.table.insertColumn(current_column_count)
        self.table.setColumnWidth(current_column_count, 60)

        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 120)

    def display_data(self):
        """Считывает данные из таблицы и отображает информацию."""
        if self.table is not None:
            data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(0, col)
                if item is not None and item.text().strip():
                    data.append(item.text())
            try:
                data = [float(item) for item in data]
            except ValueError:
                QMessageBox.information(
                    self, "Данные", "Вы ввели неправильные данные."
                )
                return

            if data:
                try:
                    arr = Array(data)
                    stats = arr.get_statistics()
                    self.set_info(stats)
                except ValueError as ve:
                    QMessageBox.warning(
                        self, "Ошибка", str(ve)
                    )
            else:
                QMessageBox.warning(
                    self, "Данные", "Нет введенных данных."
                )
        else:
            QMessageBox.warning(
                self, "Данные", "Таблица пуста."
            )

    def set_info(self, stats):
        """Отображает статистическую информацию о массиве."""
        avg, error, mn, mx = stats
        self.table_label.setText(f"""
            <span style="font-size: 16px;">
                Среднее значение: {avg} ± {error}<br><br>
                Минимальное значение: {mn}<br><br>
                Максимальное значение: {mx}
            </span>
        """)

    def clear_table_widgets(self):
        """Удаляет таблицу и кнопку добавления колонок, если они существуют."""
        if self.table and self.scroll_area and self.add_column_button:
            self.layout.removeWidget(self.add_column_button)
            self.add_column_button.deleteLater()
            self.add_column_button = None

            self.layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

            self.table.deleteLater()
            self.table = None

        elif self.add_column_button:
            self.layout.removeWidget(self.add_column_button)
            self.add_column_button.deleteLater()
            self.add_column_button = None

        elif self.scroll_area:
            self.layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None


def show_array_window(main_window=None):
    """Создает и возвращает экземпляр окна обработки массива."""
    window = ArrayWindow(main_window=main_window)
    window.show()
    return window
