SmartLab

Описание проекта:
Умный обработчик данных для лабораторных работ

Для удобного использования интегрирован графический интерфейс (PyQt6), далее граф.окно

В начале дается на выбор 3 действия в терминале:

1 - Обработка массивов

2 - Построение графика

3 - Визуализация данных

Далее это окно пропадает и дальше все зависит от выбранного действия

Подробное описание каждой ветки:
-------

1 - появляется граф.окно, где появляется таблица, куда вписывается наш массив
Так же в этом окне на выбор есть несколько функций:

- min/max

- ср.знач + погрешность

---------

2 - появляется граф.окно с выбором действий:

- обычное построение графика

- построение линейного графика с подсчетом МНК

- построение сглажтвающей прямой для графика

---------
3 - появляется граф.окно с выбором действий:

-  гистограмма из файла

- гистограмма из таблицы, где можно вручную вбить значения 


  **Используемые библиотеки**:
  PyQt6: создание окон, кнопок, таблиц и других элементов GUI.
 - matplotlib: построение графиков и гистограмм.
 - numpy: математические операции и работа с массивами.
 - scipy: интерполяция данных с помощью B-сплайнов.
 - math: вычисления (например, стандартная ошибка).
 - main.py
  Точка входа в приложение.
 - 
**main.py**
- Функция run_app():
Инициализирует и запускает главное окно приложения, вызывая MainWindow из модуля first_window.py.

**gui/first_window.py**
Главное окно выбора действий.

Класс MainWindow
Создает основное окно с тремя кнопками:

Обработка массивов: открывает окно для анализа массивов.
Построение графика: открывает окно для работы с графиками.
Визуализация данных: открывает окно для создания гистограмм.
Методы:

- on_button1_click(): закрывает главное окно и вызывает show_array_window().
- on_button2_click(): закрывает главное окно и вызывает show_chart_window().
- on_button3_click(): закрывает главное окно и вызывает show_gistogramma_window().
Функция run_app():

Запускает приложение и отображает главное окно.

**gui/chart_gui.py**
Интерфейс для построения графиков.

Класс ChartWindow
- Создает окно с кнопками для ввода данных, построения графиков и выполнения анализа.

Методы:

- clear_previous_chart(): очищает предыдущий график перед построением нового.
- load_data_from_file(): загружает данные из файла и строит график.
- enter_data_manually(): позволяет пользователю ввести данные вручную через таблицу.
- plot_from_table(): строит график на основе данных из таблицы.
- draw_chart(x, y): отображает график на основе данных x и y.
- chart_line(): строит сглаживающую кривую с использованием B-сплайна.
- set_mnk(): выполняет анализ методом наименьших квадратов (МНК) и отображает уравнение прямой.
- linear_chart(): строит линейную экстраполяцию на основе коэффициентов МНК.

Функция show_chart_window(parent=None):

Создает и отображает окно ChartWindow.

**gui/array_analys_gui.py**
Интерфейс для анализа массивов данных.

Основные функции:
- show_array_window():
Создает окно с кнопками для ввода данных из файла, ручного ввода и отображения данных.
- load_data_from_file(window):
Загружает данные из выбранного файла и обрабатывает их.
Показывает сообщение об ошибке при неверном формате данных.
- manual_input(window):
Создает таблицу для ручного ввода данных.
Позволяет добавлять новые колонки в таблицу.
- add_new_column(table, width, height):
Добавляет новую колонку в таблицу с указанными параметрами ширины и высоты.
- display_data(window, data=[]):
Считывает данные из таблицы и отображает их статистические параметры (среднее, минимум, максимум).
- set_info(window, data):
Анализирует данные с помощью класса Array и выводит результаты анализа.

**data_processing/array_analys.py**
Анализ массивов данных.

Класс Array
 Методы:
- __init__(array): инициализирует объект с переданным массивом данных.
- find_min(): возвращает минимальное значение массива.
- find_max(): возвращает максимальное значение массива.
- find_avg(): вычисляет среднее значение и стандартную ошибку массива.
- sort(): метод заявлен, но не реализован. 


**data_processing/chart_analys.py**

Анализ данных графиков.

Класс Chart
Методы:
- __init__(x, y): инициализирует объект с массивами данных x и y.
- coefficient_reg_inv(): вычисляет коэффициенты линейной регрессии с помощью матричного умножения.
- MNK(): строит график данных и выполняет анализ методом наименьших квадратов (МНК).
- data_processing/read_file.py
Функции для чтения данных из файла.

- read(file_path, message):
Считывает данные из файла по указанному пути.
Возвращает список целых чисел из первой строки (вторая строка недоступна из-за ошибки в коде).
- read_chart(file_path):
Объявлена, но не реализована.

**gui/gistogramma.py**
Интерфейс для создания гистограмм.

Основные функции:
- show_gistogramma_window():
Создает окно с кнопками для ввода данных из файла и ручного ввода.
- load_data_from_file(window):
Загружает данные из файла и строит гистограмму.
- manual_input(window):
Создает таблицу для ручного ввода данных.
- add_new_column(table, width, height):
Добавляет новую колонку в таблицу.
- plot_histogram_from_table(table):
Считывает данные из таблицы и строит гистограмму.
- draw_gistogramma(data, bins=10, title, xlabel, ylabel):
Строит гистограмму на основе данных и настраивает параметры отображения.