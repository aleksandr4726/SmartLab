import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from data_processing.read_file import read  # Импортируйте функцию read

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

    # Добавляем Figure и FigureCanvas для отображения гистограммы
    figure = Figure()
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)

    # Подключаем кнопки к функциям
    button1.clicked.connect(lambda: load_data_from_file(gistogramma_window, figure, canvas))
    button2.clicked.connect(lambda: manual_input(figure, canvas))

    gistogramma_window.show()
    return gistogramma_window

def load_data_from_file(window, figure, canvas):
    """Загружает данные из файла и строит гистограмму."""
    file_path, _ = QFileDialog.getOpenFileName(window, "Выберите файл", "", "Все файлы (*.*)")
    if file_path:
        gist_znach_1 = read(file_path, "1")
        print("Данные из файла:", gist_znach_1)  # Отладочная информация
        if gist_znach_1:  # Проверяем, не пустые ли данные
            draw_gistogramma(gist_znach_1, figure, canvas)
        else:
            print("Ошибка: данные пустые!")

def manual_input(figure, canvas):
    """Генерирует случайные данные для тестирования."""
    test_data = np.random.normal(0, 1, 100)  # Генерация 100 случайных чисел
    draw_gistogramma(test_data, figure, canvas)

def draw_gistogramma(data, figure, canvas, bins=10, title="Гистограмма", xlabel="Значения", ylabel="Частота"):
    figure.clear()  # Очищаем фигуру перед созданием нового графика
    ax = figure.add_subplot(111)  # Добавляем оси на фигуру
    ax.hist(data, bins=bins, color='blue', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas.draw()  # Обновляем Canvas для отображения новой гистограммы
