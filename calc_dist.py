# Программа для расчета максимального и минимального расстояния в массиве n-мерных векторов
#  и отрисовки гистограммы распределения расстояний между векторами
# Вектора должны быть помещены в директорию с программой в файл vectors.csv с разделителем - ','
import csv
import numpy
import math
import matplotlib.pyplot as plot
from itertools import combinations


STEP=0.1 # шаг областей гистограммы

def simple_init_gen(func):
    # Декоратор для простой инициации генератора
    def init_gen(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return init_gen

@simple_init_gen
def distribution_calc(step=0.1):
    # Генератор для подсчета распределения расстояния
    distribution = {}
    while True:
        dist = yield(distribution)
        steps_range =  int(dist/STEP)*STEP
        distribution[steps_range] = distribution.get(steps_range, 0) + 1

@simple_init_gen
def min_max_calc(len_field):
    # Генератор для нахождения максимального и минимального значений расстояний
    max_dist = (0, 0, 0)
    min_dist = (0, 0, 0)
    vector_a = 0
    vector_b = 1
    while True:
        dist = yield(max_dist, min_dist)
        if max_dist[0]==0 or max_dist[0]<dist:
            max_dist = (dist, vector_a, vector_b)
        if min_dist[0]==0 or min_dist[0]>dist:
            min_dist = (dist, vector_a, vector_b)
        # Подсчет номеров векторов при комбинировании itertools.combinations(,2)
        vector_b += 1
        if vector_b>len_field-1:
            vector_a += 1
            vector_b = vector_a+1

def find_dist(vectors_field):
    # Возвращает максимальное и минимальное значение в виде (значение, вектор_а, вектор_б),
    # Возвращает распределение в виде словаря {правая_граница_области:кол-во_расстояний_в_области}
    mm_calc = min_max_calc(len(vectors_field))
    d_calc = distribution_calc(STEP)
    print('Проводится расчет...')
    for vector_a, vector_b in combinations(vectors_field, 2):
        dist = numpy.linalg.norm(vector_a-vector_b)
        max, min = mm_calc.send(dist)
        distrib = d_calc.send(dist)
    return max, min, distrib

def drow_histogramm(distribution):
    # Отрисовывает гистограмму
    x = sorted(distribution.keys())
    y = [distribution[pos] for pos in x]
    fig, axs = plot.subplots()
    axs.bar(x, y)
    plot.show()

if __name__=='__main__':
    with open('vectors.csv', 'r', newline='') as vectors_file:
        csv_reader = csv.reader(vectors_file, delimiter=',')
        vectors_field = [numpy.array(vector, float) for vector in csv_reader]
        max, min, distrib = find_dist(vectors_field)
    print('Максимальное расстояние между векторами = %.3f, между векторами %s и %s' %max)
    print('Минимальное расстояние между векторами = %.3f, между векторами %s и %s' %min)
    drow_histogramm(distrib)
