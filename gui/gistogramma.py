# gistogramma.py 
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog,
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_processing.read_file import read  # Импортируйте функцию read
import sys

class GistogrammaWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Ссылка на главное окно
        self.setWindowTitle("Гистограмма")
        self.setGeometry(100, 200, 800, 600)

        # Инициализация Figure и Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Создание кнопок
        self.button_load_file = QPushButton("Ввести данные из файла")
        self.button_manual_input = QPushButton("Ввести данные вручную")
        self.button_back = QPushButton("Назад")  # Кнопка возврата

        # Подключение кнопок к методам
        self.button_load_file.clicked.connect(self.load_data_from_file)
        self.button_manual_input.clicked.connect(self.manual_input)
        self.button_back.clicked.connect(self.go_back)

        # Создание основного layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_load_file)
        buttons_layout.addWidget(self.button_manual_input)
        buttons_layout.addWidget(self.button_back)

        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.canvas)

        central_widget.setLayout(main_layout)

        # Инициализация таблицы как None
        self.table = None

    def load_data_from_file(self):
        """Загружает данные из файла и строит гистограмму."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*)")
        if file_path:
            try:
                gist_znach_1 = read(file_path, "1")
                if gist_znach_1:  # Проверяем, не пустые ли данные
                    self.draw_gistogramma(gist_znach_1)
                else:
                    self.show_error_message("Ошибка: данные пустые!")
            except ValueError as e:
                self.show_error_message(str(e))
            except Exception as e:
                self.show_error_message(f"Ошибка при загрузке данных: {str(e)}")

    def show_error_message(self, message):
        """Отображает сообщение об ошибке в виде всплывающего окна."""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.exec()

    def manual_input(self):
        """Удаляет старые элементы интерфейса и добавляет новые для ввода данных вручную."""
        layout = self.centralWidget().layout()

        # Удаляем старую таблицу, если она существует
        if self.table is not None:
            layout.removeWidget(self.table)
            self.table.deleteLater()
            self.table = None

        # Создаем новую таблицу с одной строкой и одним столбцом
        self.table = QTableWidget(1, 1)
        self.table.setVerticalHeaderLabels(["Значение"])  # Устанавливаем вертикальный заголовок
        self.table.setHorizontalHeaderLabels(["1"])        # Устанавливаем горизонтальный заголовок

        # Изначально пустые значения
        self.table.setItem(0, 0, QTableWidgetItem(""))

        # Установка ширины и высоты колонок
        column_width = 60  # Установите желаемую ширину колонок
        self.table.setColumnWidth(0, column_width)  # Устанавливаем ширину первой колонки

        row_height = 60  # Установите желаемую высоту строк
        self.table.setRowHeight(0, row_height)  # Устанавливаем высоту первой строки

        # Кнопка для добавления новой колонки
        self.add_column_button = QPushButton("Добавить колонку")
        self.add_column_button.clicked.connect(self.add_new_column)

        # Кнопка для построения гистограммы на основе введенных данных
        self.plot_button = QPushButton("Построить гистограмму")
        self.plot_button.clicked.connect(self.plot_histogram_from_table)

        # Горизонтальный layout для кнопок добавления колонки и построения графика
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_column_button)
        buttons_layout.addWidget(self.plot_button)

        # Добавляем новую таблицу и кнопки в layout
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)

    def add_new_column(self):
        """Добавляет новую колонку и устанавливает ее ширину и обновляет заголовки."""
        if self.table is not None:
            current_col_count = self.table.columnCount()
            self.table.insertColumn(current_col_count)
            self.table.setColumnWidth(current_col_count, 60)  # Устанавливаем ширину новой колонки

            # Обновляем горизонтальные заголовки
            headers = [str(i + 1) for i in range(self.table.columnCount())]
            self.table.setHorizontalHeaderLabels(headers)

            # Устанавливаем высоту всех строк в таблице
            row_count = self.table.rowCount()
            for row in range(row_count):
                self.table.setRowHeight(row, 100)

    def plot_histogram_from_table(self):
        """Считывает данные из таблицы и строит гистограмму."""
        data = []
        if self.table is not None:
            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item is not None and item.text().strip():
                        try:
                            # Преобразуем текст в число
                            data.append(float(item.text()))
                        except ValueError:
                            self.show_error_message(f"Неверное значение в ячейке ({row + 1}, {col + 1}): '{item.text()}'")
                            return

        if data:
            self.draw_gistogramma(data)
        else:
            self.show_error_message("Таблица пуста или содержит недопустимые значения.")

    def draw_gistogramma(self, data, title="Гистограмма", xlabel="Значения", ylabel="Частота"):
        try:
            if not data:  # Проверка на наличие данных
                self.show_error_message("Нет данных для построения гистограммы.")
                return

            self.figure.clear()  # Очищаем фигуру перед созданием нового графика
            ax = self.figure.add_subplot(111)  # Добавляем оси на фигуру

            # Автоматическое определение количества бинов
            bins = len(data)
            if bins < 1:
                bins = 1  # Минимум один бин

            ax.hist(data, bins=bins, color='blue', edgecolor='black')
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            self.canvas.draw()  # Обновляем Canvas для отображения новой гистограммы

        except Exception as e:
            self.show_error_message(f"Ошибка при построении гистограммы: {e}")

    def go_back(self):
        """Возвращает пользователя в главное окно."""
        self.main_window.show()
        self.close()

    def closeEvent(self, event):
        """Обработчик события закрытия окна."""
        self.main_window.show()
        event.accept()

# Код для самостоятельного запуска файла не требуется, так как управление осуществляется через main.py
