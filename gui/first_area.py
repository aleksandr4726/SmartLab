from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class FirstWorkArea(QWidget):
    def __init__(self):
        super().__init__()

        # Настраиваем первую рабочую зону
        self.label = QLabel("Рабочая зона 1")
        self.label.setStyleSheet("border: 1px solid black; padding: 10px;")

        # Устанавливаем лэйаут для первой рабочей зоны
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        layout.setSpacing(0)  # Убираем промежутки между элементами
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Столбец 1", "Столбец 2"])

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedWidth(1100)

    def update_text(self, text):
        self.label.setText(text)
