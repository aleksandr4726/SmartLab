import math

from fontTools.designspaceLib import AbstractAxisDescriptor


class Array:
    def __init__(self, array):
        self.array = array

    def find_min(self):  # находит минимум
        return (min(self.array))

    def find_max(self):  # находит максимум
        return (max(self.array))

    def find_avg(self):  # находит среднее знач и погрешность
        if len(self.array) == 1:
            return(self.array[0])
        avg = sum(self.array) / len(self.array)
        x = [(i - avg) ** 2 for i in self.array]
        y = sum(x)
        return (f"{avg} ±  {math.sqrt(y / (len(self.array) * (len(self.array) - 1)))}")

    def sort(self):  # сортирует массив
        pass
