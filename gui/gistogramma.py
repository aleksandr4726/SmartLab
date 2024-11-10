import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, \
    QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_processing.read_file import read  # Импортируйте функцию read

# Хранение figure и canvas как глобальных переменных
figure = None
canvas = None
table = None  # Глобальная переменная для таблицы


def show_gistogramma_window():
    """Создает главное окно гистограммы."""
    global figure, canvas

    # Создаем новое окно
    gistogramma_window = QMainWindow()
    gistogramma_window.setWindowTitle("Гистограмма")
    gistogramma_window.setGeometry(100, 200, 800, 600)

    central_widget = QWidget(gistogramma_window)
    gistogramma_window.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    button1 = QPushButton("Ввести данные из файла")
    button2 = QPushButton("Ввести данные вручную")

    layout.addWidget(button1)
    layout.addWidget(button2)

    # Создаем Figure и FigureCanvas для отображения гистограммы
    global figure
    global canvas
    figure = Figure()
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)

    # Подключаем кнопки к функциям
    button1.clicked.connect(lambda: load_data_from_file(gistogramma_window))
    button2.clicked.connect(lambda: manual_input(gistogramma_window))

    gistogramma_window.show()
    return gistogramma_window


def load_data_from_file(window):
    """Загружает данные из файла и строит гистограмму."""
    file_path, _ = QFileDialog.getOpenFileName(window, "Выберите файл", "", "Все файлы (*.*)")
    if file_path:
        try:
            gist_znach_1 = read(file_path, "1")
            if gist_znach_1:  # Проверяем, не пустые ли данные
                draw_gistogramma(gist_znach_1)
            else:
                show_error_message("Ошибка: данные пустые!")
        except ValueError as e:
            show_error_message(str(e))
        except Exception as e:
            show_error_message(f"Ошибка при загрузке данных: {str(e)}")


def show_error_message(message):
    """Отображает сообщение об ошибке в виде всплывающего окна."""
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setText(message)
    error_dialog.setWindowTitle("Ошибка")
    error_dialog.exec()


def manual_input(window):
    """Удаляет старые элементы интерфейса и добавляет новые для ввода данных вручную."""
    global table  # Используем глобальную переменную таблицы
    layout = window.centralWidget().layout()

    # Удаляем старую таблицу, если она существует
    if table is not None:
        layout.removeWidget(table)  # Удаляем таблицу из layout
        table.deleteLater()  # Освобождаем память

    # Удаляем старые кнопки, если они существуют
    while layout.count() > 3:  # Удаляем все элементы, кроме таблицы и двух кнопок
        item = layout.takeAt(3)  # Удаляем элементы начиная с 4-го
        if item.widget() is not None:
            item.widget().deleteLater()

    # Создаем новую таблицу с одним рядом и несколькими столбцами
    table = QTableWidget(window)
    table.setRowCount(1)  # Один ряд
    table.setColumnCount(1)  # Установите необходимое количество столбцов

    # Установка ширины и высоты колонок
    column_width = 60  # Установите желаемую ширину колонок
    table.setColumnWidth(0, column_width)  # Устанавливаем ширину первой колонки

    row_height = 60  # Установите желаемую высоту строк
    table.setRowHeight(0, row_height)  # Устанавливаем высоту первой строки

    # Кнопка для добавления новой колонки
    add_column_button = QPushButton("Добавить колонку")
    add_column_button.clicked.connect(lambda: add_new_column(table, column_width, row_height))

    # Кнопка для построения гистограммы на основе введенных данных
    plot_button = QPushButton("Построить гистограмму")
    plot_button.clicked.connect(lambda: plot_histogram_from_table(table))

    # Добавляем новые элементы в layout
    layout.addWidget(table)
    layout.addWidget(add_column_button)
    layout.addWidget(plot_button)


def add_new_column(table, width, height):
    """Добавляет новую колонку и устанавливает ее ширину и высоту."""
    table.insertColumn(table.columnCount())  # Добавляем новую колонку
    table.setColumnWidth(table.columnCount() - 1, width)  # Устанавливаем ширину новой колонки

    # Устанавливаем высоту всех строк в таблице
    for row in range(table.rowCount()):
        table.setRowHeight(row, height)


def plot_histogram_from_table(table):
    """Считывает данные из таблицы и строит гистограмму."""
    data = []
    for col in range(table.columnCount()):
        item = table.item(0, col)  # Обрабатываем только первую строку
        if item is not None and item.text().strip():
            try:
                # Преобразуем текст в число
                data.append(float(item.text()))
            except ValueError:
                show_error_message(f"Неверное значение в колонке {col + 1}: '{item.text()}'")

    if data:
        draw_gistogramma(data)
    else:
        show_error_message("Таблица пуста или содержит недопустимые значения.")


def draw_gistogramma(data, bins=10, title="Гистограмма", xlabel="Значения", ylabel="Частота"):
    try:
        if not data:  # Проверка на наличие данных
            show_error_message("Нет данных для построения гистограммы.")
            return

        figure.clear()  # Очищаем фигуру перед созданием нового графика
        ax = figure.add_subplot(111)  # Добавляем оси на фигуру
        ax.hist(data, bins=bins, color='blue', edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas.draw()  # Обновляем Canvas для отображения новой гистограммы

    except Exception as e:
        show_error_message(f"Ошибка при построении гистограммы: {e}")
