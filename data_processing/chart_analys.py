import matplotlib.pyplot as plt
import numpy as np

class Chart:
    def __init__(self, *arrays):
        # Преобразуем x и y в массивы numpy для более удобной работы
        self.x = np.array(arrays[0])
        self.y = np.array(arrays[1])

    def coefficient_reg_inv(self):
        size = len(self.x)
        # формируем и заполняем матрицу размерностью 2x2
        A = np.empty((2, 2))
        A[0, 0] = sum((self.x[i]) ** 2 for i in range(size))
        A[0, 1] = sum(self.x)
        A[1, 0] = sum(self.x)
        A[1, 1] = size
        # находим обратную матрицу
        A = np.linalg.inv(A)
        # формируем и заполняем матрицу размерностью 2x1
        C = np.empty((2, 1))
        C[0, 0] = sum(self.x[i] * self.y[i] for i in range(size))
        C[1, 0] = sum(self.y)
        # умножаем матрицу на вектор
        ww = np.dot(A, C)
        return ww[1].item(), ww[0].item()  # Используем item() для извлечения значения

    def MNK(self):
        # НАСТРОЙКИ ГРАФИКА
        plt.plot(self.x, self.y, 'o')
        plt.xlabel('x', fontsize=14)
        plt.ylabel('y', fontsize=14)
        plt.show()
        # ПОДСЧЁТ МНК
        # ВЫВОД КОЭФФ.КОРРЕЛЯЦИИ И ЛИНЕЙНОГО КОЭФФ.
        w0_1, w1_1 = self.coefficient_reg_inv()
        # Округление до 4 значащих цифр
        w0_1 = round(w0_1, 4)
        w1_1 = round(w1_1, 4)
       # return w0_1, w1_1
