import math

class Array:
    def __init__(self, array):
        if not array:
            raise ValueError("Массив не должен быть пустым.")
        self.array = array

    def find_min(self):
        """Находит минимальное значение."""
        return min(self.array)

    def find_max(self):
        """Находит максимальное значение."""
        return max(self.array)

    def find_avg(self):
        """Находит среднее значение и погрешность."""
        n = len(self.array)
        if n == 1:
            return self.array[0], 0  # avg, error
        avg = sum(self.array) / n
        variance = sum((x - avg) ** 2 for x in self.array)
        error = math.sqrt(variance / (n * (n - 1)))
        return avg, error

    def get_statistics(self):
        """Возвращает среднее значение, погрешность, минимум и максимум."""
        avg, error = self.find_avg()
        mn = self.find_min()
        mx = self.find_max()
        return avg, error, mn, mx
