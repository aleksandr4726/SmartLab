from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем таблицу с двумя столбцами
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Столбец 1", "Столбец 2"])

        # Устанавливаем фиксированную ширину для столбцов
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)

        # Создаем кнопку "Добавить строку"
        self.add_button = QPushButton("Добавить строку")
        self.add_button.clicked.connect(self.add_row)

        # Настраиваем ширину кнопки равной ширине обоих столбцов вместе
        total_table_width = self.table.columnWidth(0) + self.table.columnWidth(1)
        self.add_button.setFixedWidth(total_table_width)

        # Лэйаут
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def add_row(self):
        # Добавляем новую строку в таблицу
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Добавляем пустые ячейки в каждый столбец новой строки
        self.table.setItem(row_position, 0, QTableWidgetItem(""))
        self.table.setItem(row_position, 1, QTableWidgetItem(""))

        # Обновляем ширину кнопки после добавления строки (если это требуется)
        total_table_width = self.table.columnWidth(0) + self.table.columnWidth(1)
        self.add_button.setFixedWidth(total_table_width)

# Пример использования в другом файле, который управляет first_area
def create_table_in_first_area(first_area):
    # Очистка содержимого рабочей зоны
    for i in reversed(range(first_area.layout().count())):
        widget = first_area.layout().itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    # Создание виджета с таблицей
    table_widget = TableWidget()
    first_area.layout().addWidget(table_widget)
