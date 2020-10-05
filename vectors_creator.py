# Программа генерации массива n-мерных векторов и записи их в файл vectors.csv с разделителем - ','
import csv
import random

def get_input_data():
    while True:
        print('Введите количество векторов (от 500 до 1000):')
        try:
            N = int(input())
        except ValueError:
            print('Необходимо ввести число')
            continue
        if N<500 or N>1000:
            print('Количество векторов не соответствует диапазону от 500 до 1000')
            continue
        print('Введите количество введите размерность векторов (от 10 до 50):')
        try:
            m = int(input())
        except ValueError:
            print('Необходимо ввести число')
            continue
        if m<10 or m>50:
            print('Размерность векторов не соответствует диапазону от 10 до 50')
            continue
        return N, m

if __name__=='__main__':
    N, m = get_input_data()
    with open('vectors.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for vector in range(N):
            writer.writerow([random.uniform(-1.0, 1.0) for i in range(m)])
    print('Вектора успешно созданы в файле vectors.csv, нажмите любую клавишу чтобы продолжить')
    input()
    
