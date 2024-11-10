import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, \
    QMessageBox, QScrollArea, QLabel

from data_processing.array_analys import Array

table = None
table_label = None
add_column_button = None  # Create a global variable for the "Add Column" button


def show_array_window():
    """Создает главное окно для обработки массива."""
    gistogramma_window = QMainWindow()
    gistogramma_window.setWindowTitle("Обработка массива")
    gistogramma_window.setGeometry(100, 200, 800, 600)

    central_widget = QWidget(gistogramma_window)
    gistogramma_window.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    button1 = QPushButton("Ввести данные из файла")
    button2 = QPushButton("Ввести данные вручную")
    button3 = QPushButton("Вывести данные")  # Кнопка для вывода данных

    # Добавляем кнопки в лэйаут
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)  # Добавляем кнопку "Вывести данные"

    # Добавляем пространство между кнопками и остальными элементами
    layout.addStretch()

    # Подключаем кнопки к функциям
    button1.clicked.connect(lambda: load_data_from_file(gistogramma_window))
    button2.clicked.connect(lambda: manual_input(gistogramma_window))
    button3.clicked.connect(lambda: display_data(gistogramma_window))  # Подключаем кнопку "Вывести данные"

    gistogramma_window.show()
    return gistogramma_window


def load_data_from_file(window):
    global table, table_label, add_column_button
    layout = window.centralWidget().layout()

    # Remove existing table, label, and add column button if they exist
    if table is not None:
        layout.removeWidget(table)
        table.deleteLater()
        table = None

    if table_label is not None:
        layout.removeWidget(table_label)
        table_label.deleteLater()
        table_label = None

    if add_column_button is not None:
        layout.removeWidget(add_column_button)
        add_column_button.deleteLater()
        add_column_button = None

    # Create a new QLabel for displaying information
    table_label = QLabel("")
    layout.addWidget(table_label)

    """Загружает данные из файла."""
    file_path, _ = QFileDialog.getOpenFileName(window, "Выберите файл", "", "Все файлы (*.*)")
    try:
        with open(file_path, 'r') as file:
            data = file.readline().strip().split()  # Считываем первую строку и удаляем лишние пробелы
            if data:
                try:
                    data = [float(item) for item in data]
                    print(data)
                    set_info(window, data)
                except:
                    QMessageBox.information(None, "Данные", f"Вы ввели неправильные данные")
            else:
                QMessageBox.warning(None, "Ввод из файла", "Файл пустой")
    except Exception:
        QMessageBox.warning(None, "Ввод из файла", "Произошла ошибка")


def manual_input(window):
    """Удаляет старые элементы интерфейса и добавляет новые для ввода данных вручную."""
    global table, table_label, add_column_button
    layout = window.centralWidget().layout()

    try:
        if table is not None:
            layout.removeWidget(table)
            table.deleteLater()

        while layout.count() > 3:
            item = layout.takeAt(3)
            if item.widget() is not None:
                item.widget().deleteLater()

        # Создаем новый QLabel для заголовка таблицы
        table_label = QLabel("")
        layout.addWidget(table_label)

        table = QTableWidget(window)
        table.setRowCount(1)
        table.setColumnCount(1)

        column_width = 60
        table.setColumnWidth(0, column_width)

        row_height = 120
        table.setRowHeight(0, row_height)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table)

        scroll_area.setMaximumHeight(150)

        add_column_button = QPushButton("Добавить колонку")
        add_column_button.clicked.connect(lambda: add_new_column(table, column_width, row_height))

        layout.addWidget(add_column_button)
        layout.addWidget(scroll_area)
        layout.addWidget(window.findChild(QPushButton, "Вывести данные"))
    except Exception as e:
        QMessageBox.critical(window, "Ошибка", f"Произошла ошибка: {e}")


def add_new_column(table, width, height):
    table.insertColumn(table.columnCount())
    table.setColumnWidth(table.columnCount() - 1, width)
    for row in range(table.rowCount()):
        table.setRowHeight(row, height)


def display_data(window, data=[]):
    global table
    if table is not None:
        data = []
        for col in range(table.columnCount()):
            item = table.item(0, col)
            if item is not None and item.text().strip():
                data.append(item.text())
        try:
            data = [float(item) for item in data]
        except:
            QMessageBox.information(None, "Данные", f"Вы ввели неправильные данные")
        if data:
            if all(isinstance(item, float) for item in data):
                set_info(window, data)
            else:
                QMessageBox.information(None, "Данные", f"Вы ввели неправильные данные")
        else:
            QMessageBox.warning(None, "Данные", "Нет введенных данных.")
    else:
        QMessageBox.warning(None, "Данные", "Таблица пуста.")


def set_info(window, data):
    global table_label
    arr = Array(data)
    avg = arr.find_avg()
    mn = arr.find_min()
    mx = arr.find_max()
    table_label.setText(f"""
           <span style="font-size: 16px;">  <!-- Увеличиваем размер шрифта -->
               Среднее значение: {avg}<br><br>  <!-- Два переноса строки для отступа -->
               Минимальное значение: {mn}<br><br>
               Максимальное значение: {mx}
           </span>
       """)
