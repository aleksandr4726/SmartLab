from PyQt6.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QApplication
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import re
import numpy as np  # Изменено с import numpy на import numpy as np
import math
from scipy.interpolate import make_interp_spline  # Добавлен импорт
from data_processing.chart_analys import Chart


class ChartWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Построение графика")
        self.setGeometry(200, 50, 1050, 800)
        self.is_exist_chart = False  # Показывает, есть ли график в окне
        self.mnk_coefficients = None  # Для хранения коэффициентов МНК

        # Создание кнопок
        button1 = QPushButton("Ввести данные из файла")
        button2 = QPushButton("Ввести данные вручную")
        button3 = QPushButton("МНК")
        button4 = QPushButton("Экстраполяция линейная")
        button5 = QPushButton("Сглаживающая кривая")

        button1.clicked.connect(self.load_data_from_file)
        button2.clicked.connect(self.enter_data_manually)
        button3.clicked.connect(self.set_mnk)
        button4.clicked.connect(self.linear_chart)
        button5.clicked.connect(self.chart_line)

        # Основной лэйаут окна
        self.layout = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()

        # Виджет для кнопок
        self.button_widget = QWidget()

        # Горизонтальные лэйауты для кнопок
        self.horizontal_button_layout_1 = QHBoxLayout()
        self.horizontal_button_layout_1.addWidget(button1, alignment=Qt.AlignmentFlag.AlignTop)
        self.horizontal_button_layout_1.addWidget(button2, alignment=Qt.AlignmentFlag.AlignTop)

        self.horizontal_button_layout_2 = QHBoxLayout()
        self.horizontal_button_layout_2.addWidget(button3, alignment=Qt.AlignmentFlag.AlignTop)
        self.horizontal_button_layout_2.addWidget(button4, alignment=Qt.AlignmentFlag.AlignTop)
        self.horizontal_button_layout_2.addWidget(button5, alignment=Qt.AlignmentFlag.AlignTop)

        # Соединяем оба горизонтальных лэйаута в один вертикальный
        self.button_layout = QVBoxLayout()
        self.button_layout.addLayout(self.horizontal_button_layout_1)
        self.button_layout.addLayout(self.horizontal_button_layout_2)
        self.button_layout.addStretch()

        self.button_widget.setLayout(self.button_layout)

        # Создание виджетов для графика и таблицы
        self.graph_widget = QWidget()
        self.graph_widget.setLayout(self.layout2)

        self.table_widget = QWidget()
        self.table_widget.setLayout(self.layout3)

        # Создание QLabel для отображения уравнения
        self.text_yx = QLabel("", self)  # Изначально пустой текст
        self.text_yx.setStyleSheet("font-size: 18px;")
        self.text_yx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout3.addWidget(self.text_yx)

        # Добавление виджетов в горизонтальный лэйаут
        self.horizontal_layout.addWidget(self.graph_widget)
        self.horizontal_layout.addWidget(self.table_widget)

        # Добавление виджетов в основной лэйаут
        self.layout.addWidget(self.button_widget)
        self.layout.addLayout(self.horizontal_layout)

        self.setLayout(self.layout)

    # Метод для очистки предыдущего графика
    def clear_previous_chart(self):
        print("Очистка предыдущего графика")
        for i in reversed(range(self.layout2.count())):
            widget = self.layout2.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        QApplication.processEvents()  # Обеспечить завершение удаления виджетов

    # Функция для загрузки данных из файла
    def load_data_from_file(self):
        print("Загрузка данных из файла")
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    lines = [line.strip() for line in lines]
                    if len(lines) == 1:
                        try:
                            pairs = re.findall(r"\(([^)]+),([^)]+)\)", lines[0])
                            tuples_list = [(float(x), float(y)) for x, y in pairs]

                            # Преобразуем кортежи в списки
                            self.x, self.y = list(zip(*tuples_list))

                            # Преобразуем их в списки, чтобы не были кортежами
                            self.x = list(self.x)
                            self.y = list(self.y)

                            # Отрисовка графика
                            print("Данные успешно загружены, отрисовка графика")
                            self.draw_chart(self.x, self.y)
                        except Exception as e:
                            print(f"Ошибка при обработке данных: {e}")
                            QMessageBox.warning(self, "Ошибка", "Некорректный формат данных в файле.")
            except Exception as e:
                print(f"Ошибка при открытии файла: {e}")
                QMessageBox.warning(self, "Ошибка", "Не удалось открыть файл.")
        else:
            print("Файл не выбран")
            QMessageBox.information(self, "Информация", "Файл не выбран.")

    # Функция для ручного ввода данных
    def enter_data_manually(self):
        print("Ручной ввод данных")

        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget and widget != self.text_yx:
                    widget.setParent(None)
                    widget.deleteLater()

        clear_layout(self.layout3)

        # Создаем таблицу с 2 строками и 2 столбцами
        self.table = QTableWidget(2, 2)
        self.table.setHorizontalHeaderLabels(["Х", "У"])

        # Изначально пустые значения
        self.table.setItem(0, 0, QTableWidgetItem(""))
        self.table.setItem(0, 1, QTableWidgetItem(""))
        self.table.setItem(1, 0, QTableWidgetItem(""))
        self.table.setItem(1, 1, QTableWidgetItem(""))

        self.table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setColumnWidth(0, 82)  # Установка ширины первого столбца
        self.table.setColumnWidth(1, 82)  # Установка ширины второго столбца
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        self.layout3.addWidget(self.table)
        self.layout3.addWidget(self.text_yx)

        # Кнопка для добавления строки
        self.add_row_button = QPushButton("Добавить строку")
        self.add_row_button.clicked.connect(self.add_row)
        self.layout3.addWidget(self.add_row_button)

        # Кнопка для построения графика
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_from_table)
        self.layout3.addWidget(self.plot_button)

    # Функция для добавления строки в таблицу
    def add_row(self):
        print("Добавление строки в таблицу")
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)
        self.table.resizeRowsToContents()

    # Функция для построения графика из данных таблицы
    def plot_from_table(self):
        print("Построение графика из таблицы")
        x_data = []
        y_data = []
        # Извлекаем данные из таблицы
        for row in range(self.table.rowCount()):
            try:
                # Получаем значения из таблицы
                x_item = self.table.item(row, 0)
                y_item = self.table.item(row, 1)

                # Проверяем, что ячейки не пустые
                if x_item is None or y_item is None:
                    continue  # Пропускаем строки с пустыми ячейками

                # Получаем текст из ячеек и проверяем на пустоту
                x_value = x_item.text().strip()
                y_value = y_item.text().strip()

                # Пропускаем строки с пустыми значениями
                if x_value == "" or y_value == "":
                    continue

                # Преобразуем в числа
                x_value = float(x_value)
                y_value = float(y_value)

                # Добавляем в список данных
                x_data.append(x_value)
                y_data.append(y_value)
                self.x = x_data
                self.y = y_data

            except ValueError:
                # Показать предупреждение, если невозможно преобразовать значение в float
                print(f"Ошибка: некорректные данные в строке {row + 1}")
                QMessageBox.warning(
                    self, "Ошибка",
                    f"Некорректные данные в строке {row + 1}. Убедитесь, что значения числовые."
                )
                return
            except Exception as e:
                # Общая обработка других ошибок
                print(f"Ошибка: {e}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
                return

        # Если данные корректные, строим график
        if x_data and y_data:
            print("Данные корректные, строим график")
            self.draw_chart(x_data, y_data)
        else:
            print("Ошибка: данные для построения графика не введены")
            QMessageBox.warning(
                self, "Ошибка",
                "Не введены данные для построения графика. Пожалуйста, заполните таблицу."
            )

    # Функция для отображения графика
    def draw_chart(self, x, y):
        print("Очистка предыдущего графика")
        # Очистка предыдущего графика
        self.clear_previous_chart()

        print("Создание нового графика")
        width_in_pixels = 800
        height_in_pixels = 700
        dpi = 100
        width_in_inches = width_in_pixels / dpi
        height_in_inches = height_in_pixels / dpi

        figure = Figure(figsize=(width_in_inches, height_in_inches), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        ax.plot(x, y, marker='o')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("График Y(X)")

        self.layout2.addWidget(canvas)
        canvas.draw()

        # Обновляем флаг наличия графика
        self.is_exist_chart = True
        print("График успешно создан")

    from scipy.interpolate import make_interp_spline
    import numpy as np

    def chart_line(self):
        print("Построение сглаживающей кривой")
        if not hasattr(self, 'x') or not hasattr(self, 'y') or len(self.x) < 2 or len(self.y) < 2:
            QMessageBox.warning(self, "Ошибка", "Недостаточно данных для построения сглаживающей кривой.")
            return
        if len(self.x) > 4:
            # Проверка на уникальность и сортировку x
            try:
                # Сортируем данные по x
                sorted_pairs = sorted(zip(self.x, self.y), key=lambda pair: pair[0])
                sorted_x, sorted_y = zip(*sorted_pairs)
                sorted_x = np.array(sorted_x)
                sorted_y = np.array(sorted_y)

                # Удаляем дубликаты в x, усредняя соответствующие y
                unique_x, indices = np.unique(sorted_x, return_index=True)
                unique_y = sorted_y[indices]

                if len(unique_x) < len(sorted_x):
                    print("Обнаружены дублирующиеся значения x. Дубликаты удалены.")
                    QMessageBox.information(self, "Информация",
                                            "Обнаружены дублирующиеся значения X. Дубликаты удалены.")

                self.x = unique_x
                self.y = unique_y

                if len(self.x) < 4:
                    k = len(self.x) - 1  # Степень сплайна не может превышать n-1
                    print(f"Недостаточно точек для кубического сплайна. Используется степень k={k}.")
                    QMessageBox.information(self, "Информация",
                                            f"Недостаточно точек для кубического сплайна. Используется степень k={k}.")
                else:
                    k = 3  # Кубический сплайн

                # Очистка предыдущего графика
                self.clear_previous_chart()

                # Инициализация графика
                width_in_pixels = 800
                height_in_pixels = 700
                dpi = 100
                width_in_inches = width_in_pixels / dpi
                height_in_inches = height_in_pixels / dpi

                figure = Figure(figsize=(width_in_inches, height_in_inches), dpi=dpi)
                canvas = FigureCanvas(figure)
                ax = figure.add_subplot(111)

                try:
                    # Создание сглаживающей кривой с использованием B-сплайна
                    x_smooth = np.linspace(self.x.min(), self.x.max(), 300)
                    spline = make_interp_spline(self.x, self.y, k=k,
                                                bc_type='natural')  # Заданы естественные условия на границах
                    y_smooth = spline(x_smooth)

                    ax.plot(self.x, self.y, 'o', label="Исходные данные")
                    ax.plot(x_smooth, y_smooth, label="Сглаживающая кривая")
                    ax.set_xlabel("X")
                    ax.set_ylabel("Y")
                    ax.set_title("Сглаживающая кривая")
                    ax.legend()
                    ax.grid(True)  # Добавляем сетку для лучшей читаемости

                    self.layout2.addWidget(canvas)
                    canvas.draw()
                    print("Сглаживающая кривая успешно построена")
                except Exception as e:
                    print(f"Ошибка при построении сглаживающей кривой: {e}")
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при построении сглаживающей кривой: {str(e)}")
            except Exception as e:
                print(f"Ошибка при обработке данных: {e}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка при обработке данных: {str(e)}")

    def set_mnk(self):
        print("Построение МНК")
        try:
            znach = Chart(self.x, self.y)
            w1, w0 = znach.coefficient_reg_inv()

            # Округление до 4 значащих цифр
            def round_to_significant_figures(value, sig_figs):
                if value == 0:
                    return 0
                else:
                    return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)

            w0 = round_to_significant_figures(w0, 4)
            w1 = round_to_significant_figures(w1, 4)

            # Сохраняем коэффициенты для использования в линейной экстраполяции
            self.mnk_coefficients = (w0, w1)

            # Обновляем текст в уже существующем QLabel
            if w1 >= 0:
                self.text_yx.setText(f"Y = {w0} X \n+ {w1}")
            else:
                self.text_yx.setText(f"Y = {w0} X \n- {abs(w1)}")
            print("Уравнение прямой обновлено")

        except Exception as e:
            print(f"Ошибка при построении МНК: {e}")
            QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")

    def linear_chart(self):
        print("Построение линейной экстраполяции")
        if self.mnk_coefficients is None:
            QMessageBox.warning(self, "Ошибка", "Сначала необходимо построить МНК для получения коэффициентов.")
            return

        w1, w0 = self.mnk_coefficients  # Обратите внимание на порядок коэффициентов

        # Очистка предыдущего графика
        self.clear_previous_chart()

        print("Создание нового графика с линейной экстраполяцией")
        width_in_pixels = 800
        height_in_pixels = 700
        dpi = 100
        width_in_inches = width_in_pixels / dpi
        height_in_inches = height_in_pixels / dpi

        figure = Figure(figsize=(width_in_inches, height_in_inches), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Построение исходных данных и линии по МНК
        ax.plot(self.x, self.y, 'o', label="Данные")
        x_min, x_max = min(self.x), max(self.x)
        x_line = [x_min, x_max]
        y_line = [w1 * x + w0 for x in x_line]
        ax.plot(x_line, y_line, '-', label="Линейная экстраполяция")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Линейная экстраполяция по МНК")
        ax.legend()

        self.layout2.addWidget(canvas)
        canvas.draw()

        print("Линейная экстраполяция успешно создана")


# Функция для создания и возврата экземпляра окна
def show_chart_window(parent=None):
    window = ChartWindow(parent)
    window.show()
    return window


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = show_chart_window()
    sys.exit(app.exec())
