import math #Модуль math предоставляет обширный функционал для работы с числами
import matplotlib.pyplot as plt #Модуль для визуализации данных двумерной (2D) графикой (3D графика также поддерживается)
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np #NumPy это open-source модуль для python, 
                   #который предоставляет общие математические и числовые операции в виде пре-скомпилированных, быстрых функций
import scipy.special as ss #Модуль scipy для языка python добавляет множество численных типов, математических операторов
import scipy.integrate as si
import os #Модуль os предоставляет множество функций для работы с операционной системой
import random #Модуль random предоставляет функции для генерации случайных чисел, букв, 
              #случайного выбора элементов последовательности
import sys #Модуль sys обеспечивает доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором python


N = 1004 #Длина последовательности
#Коэффициенты генератора 
a = 3 #Коэффициент при X[i]
b = 8 #Коэффициент при X[i-2]
c = 5 #Свободный член
X = [19,1,7] #Последовательность
T = 0 #Период последовательности

def toFixed(numObj, digits=0): #Аналог функции toFixed() в JS, указываем, сколько знаков вывести после запятой
    return f"{numObj:.{digits}f}"

def Generator(): #Генерация последовательности псевдослучайных величин длиной N
    with open('sequence.txt', 'w', encoding='utf-8') as f: #Открыть файл на запись (явно)
        for i in range(2,N): #Цикл начинается с i=2, т.к. начальные значения уже заданы в исходной последовательности
            X.append((a * X[i] + b * X[i-2] + c) % N) #Метод append вставляет содержимое, заданное параметром, в конец каждого элемента в наборе соответствующих элементов (генератор из варианта)
        for i in range(N): #Цикл, производящий запись сгенерированной последовательности в файл
            f.write(str(X[i]) + '\n')
    f.close()

def Period1(): #тестовый период (не используется)
    X_ = list(reversed(X))
    T = 1
    max_len = len(X_) // 2 + 1
    for i in range(2, max_len):
        if X_[0:i] == X_[i:2*i]:
            return i
    print(T)
    return T

def Period(): #Подпрограмма, осуществляющая поиск периода псевдослучайной последовательности
    with open('output_period.txt', 'a', encoding='utf-8') as f: #Открыть файл на запись
        X_ = list(reversed(X)) #X_ содержит список псевдослучайной послежовательности X, записанной с конца 
        for i in range(N-5): #Внешний цикл
            for j in range(i+3,N-2): #Внутренний цикл
                if X_[i] == X_[j] and X_[i+2] == X_[j+2]: #Сравниваем 1 и 4 и 3 и 6 элементы и т.д. (поэтому внешний цикл 
                                                          #заканчивается раньше, цикл по j начинается как раз с 4-го элемента)
                    T = j - i
                    if T < 100:
                        f.write('Период последовательности: '+str(T)+'\n' + 'Работа программы остановлена, т.к. T < 100') #Записать в файл частоты попаданий
                        sys.exit()
                    else:
                        #print('Счетчик по j: j = ' + str(j)) #Выводим значение счетчика внутреннего цикла
                        #print('Счетчик по i: i = ' + str(i)) #Выводим значение счетчика внешнего цикла
                        #print('Период последовательности: ' + 'T = ' + str(T) + '\n') #Выводим период последовательности
                        f.write('Период последовательности: '+str(T)+'\n' + 'Условие T > 100 выполнено' + '\n') #Записать в файл частоты попаданий
                    return T

def Test1(X,n): #Тест на случайность (проверка перестановок)
    T = Period()
    #print(T)
        
    with open('output_test1.txt', 'a', encoding='utf-8') as f: #Открыть файл на запись
        #f.write('Последовательность: '+str(X)+'\n') #Записать в файл последовательность в виде строки
        print('Проверка перестановок (тест №1)...') #Уведомление о запуске 1-го теста
        a = 0.05 #Уровень значимости
        U = 1.959964 #Квантиль уровня 1-a/2 нормального распределения с M = 0 (мат ожидание) D = 1 (среднеквадратичное отклонение) | Из таблиц
        Q = 0 #Количество перестановок
        X = [X[i] for i in range(T)]
        #print(X)
        for i in range(n - 1): #Перебираем значения
            if X[i] > X[i + 1]: #Проверка соответствия наблюдаемого количества перестановок
                Q += 1 #Счетчик (число перестановок)
        #Чтобы выборка удовлетворяла условиям случайности, математическое ожидание числа перестановок, равное для случайной выборки числу n/2 , должно попадать в построенный доверительный интервал
        if Q - U * math.sqrt(n) / 2 < n / 2 and Q + U * math.sqrt(n) / 2 > n / 2: 
            #Если условие выполняется, тест пройден успешно (последовательность, создаваемая генератором, близка к случайной)
            result = 'Тест пройден'
        else:
            #Инче тест не считается пройденным
            result = 'Тест не пройден'
        #Записываем в файл значение оценки Q, построенный доверительный интервал и результат выполнения теста (True or False)
        f.write('Оценка Q: '+str(Q)+'\nДоверительный интервал: ['+str(Q - U * math.sqrt(n) / 2)+'; '+str(Q + U * math.sqrt(n) / 2)+']'+'\nРезультат: '+str(result)+'\n' +'\n')
        print('Q = '+str(Q)+' | Доверительный интервал: [' + str(Q - U * math.sqrt(n) / 2) + ' ; ' + str(Q + U * math.sqrt(n) / 2) + ' ] | Результат : ' + str(result)) #Вывод в консоль 
        f.close() #Закрыть файл
        return result #Вернуть результат выполнения теста

def Hist(X,K): #Подпрограмма для гистрограмм
    gfig, gax = plt.subplots() #plt.subplots() - это функция, которая возвращает кортеж, содержащий фигуру и объект осей
    gn, gbins, gpatches = gax.hist(X, K, density=1) #Построить гистрограмму с плотностью 1
    gax.set_title('Гистограмма частот (n=' + str(len(X)) + ')') #Название графика
    gfig.tight_layout() 
    plt.show() #показать график (гистрограммы)


def Hist1(data, n, m): #Подпрограмма для гистрограмм (исправленная)
    x = np.arange(len(data))
    data_min = min([x for x in data if x != 0])
    plt.bar(x, height=data, width=1, align='edge') 
    plt.xticks(x)
    plt.yticks(np.arange(0, max(data) + data_min, step=data_min/2))
    plt.title("Гистрограмма частот (n = {0}, m = {1})".format(n, m))
    plt.xlabel("Интервалы (K)")
    plt.ylabel("Частоты попаданий (v)")
    plt.grid(True)
    plt.show()


def Test2(X,K,n):
    T = Period()
    #print(T)
    with open('output_test2.txt', 'a', encoding='utf-8') as f: #Открыть файл на запись
        print('\nТест на равномерность (тест №2)...') #Уведомление о запуске 2-го теста
        a = 0.05 #Уровень значимости
        U = 1.959964 #Квантиль уровня 1-a/2 нормального распределения с M = 0 (мат ожидание) D = 1 (среднеквадратичное отклонение) | Из таблиц
        X = [X[i] for i in range(T)]
        #N = T
        #print(N)
        #print(X)
        rightXi = [0.001, 0.8312, 3.247, 6.2621, 9.5908, 13.12, 16.791, 20.569, 24.433, 28.366, 32.357] #Квантиль уровня 1-a/2 Хи квадрат | Из таблиц
        leftXi = [5.0239, 12.833, 20.483, 27.488, 34.17, 40.646, 46.979, 53.203, 59.342, 65.41, 71.42] #Квантиль уровня a/2 Хи квадрат | Из таблиц
        result = 'Тест пройден'
        
        if K == 10:
            #Относительные частоты попаданий в интервалы
            V = [0 for i in range(K)] #обнуляем все частоты
            M = 0 #Обнуляем мат ожидание
            D = 0 #Обнуляем дисперсию
            #n = len(X)
            for i in range(K):
                left = N / K * i
                right = N / K * (i + 1)
                for j in range(n):
                    if X[j] <= right and X[j] >= left: #попадает ли в интервал
                        V[i] += 1
            for i in range(K):
                V[i]/=n #Рассчитаем относительные частоты попаданий в интервалы
            Hist1(V, n, N)
            #Hist(X[0:n],K) #Гистрограмма частот на K отрезках интервала [0; n)
            f.write('Частоты попаданий: '+str(V)+'\n') #Записать в файл частоты попаданий
                #Вычислим оценку математического ожидания случайной величины (пункт 5)
            for i in range(n):
                M+=X[i]
            M /= n
                #Вычислим оценку дисперсии случайной величины (пункт 6)
            for i in range(n):
                D+=(X[i] - M) ** 2
            D /= (n - 1) 

            #Проверки

            #Частот
            for i in range(K): #пункт 8
                left = (V[i] - U / K * math.sqrt((K - 1) / n))  #Левое значение интервала 
                right = (V[i] + U / K * math.sqrt((K - 1) / n))  #Правое значение интервала
                f.write('Интервал для частот : ['+str(left)+';'+str(right)+']\n') #Записать в файл интервал для мат ожидания

                if ((1 / (K * 10) < left) or (1 / (K * 10) > right)): #Условие (1/K) не лежит в интервале
                    print('Тест не пройден: условие (1/K) не лежит в интервале')
                    result = 'Тест не пройден (не прошел проверку частот)' #Присвоить результату значение False
                    
            
            #Мат.ожиданий (пункт 9)
            left = M - U * math.sqrt(D) / math.sqrt(n) #Левое значение интервала
            right = M + U * math.sqrt(D) / math.sqrt(n) #Правое значение интервала
            f.write('Математическое ожидание: '+str(M)+'\n') #Записать в файл значение мат ожидания
            f.write('Теоретическое математическое ожидание: '+str(N/2)+'\n') #Записать в файл теоретическое значение мат ожидания
            f.write('Интервал для мат ожидания : ['+str(left)+';'+str(right)+']\n') #Записать в файл интервал для мат ожидания
            if ((N / 2 < left) or (N / 2 > right)):  #Условие (N/2) не лежит в интервале
                print('Тест не пройден: условие (N/2) не лежит в интервале')
                result = 'Тест не пройден (не прошел проверку мат ожиданий)' #Присвоить результату значение False
            
            #Дисперсий (тоже пункт 9)
            left = (n - 1) * D / leftXi[int(2)] / 10 #Левое значение интервала
            right = (n - 1) * D / rightXi[int(2)] / 10 #Правое значение интервала
            f.write('Дисперсия: '+str(D)+'\n') #Записать в файл значение дисперсии
            f.write('Теоретическая дисперсия: '+str(N ** 2 / 12)+'\n') #Записать в файл теоретическое значение дисперсии
            f.write('Интервал для дисперсии : ['+str(left)+';'+str(right)+']\n\n') #Записать в файл интервал для дисперсии
            if ((N ** 2 / 12 < left) or (N ** 2 / 12 > right)):   #Условие (N^2/12) не лежит в интервале
                print('Тест не пройден: условие (N^2/12) не лежит в интервале')
                result = 'Тест не пройден (не прошел проверку дисперсий)' #Присвоить результату значение False
        
    
        print('Результат теста : ' + str(result)) #Вывести в консоль результат теста
        f.close() #Закрыть файл
        return result #Вернуть результат

def Test1_3(X,n): #Тест на случайность (проверка перестановок)
    with open('output_test1_3.txt', 'a', encoding='utf-8') as f: #Открыть файл на запись
        #f.write('Последовательность: '+str(X)+'\n') #Записать в файл последовательность в виде строки
        print('Проверка перестановок (тест №1)...') #Уведомление о запуске 1-го теста
        f.write('Проверка перестановок (тест №1)...' + '\n') #Уведомление о запуске 1-го теста
        a = 0.05 #Уровень значимости
        U = 1.959964 #Квантиль уровня 1-a/2 нормального распределения с M = 0 (мат ожидание) D = 1 (среднеквадратичное отклонение) | Из таблиц
        Q = 0 #Количество перестановок
        n = len(X)
        for i in range(n - 1): #Перебираем значения
            if X[i] > X[i + 1]: #Проверка соответствия наблюдаемого количества перестановок
                Q += 1 #Счетчик (число перестановок)
        #Чтобы выборка удовлетворяла условиям случайности, математическое ожидание числа перестановок, равное для случайной выборки числу n/2 , должно попадать в построенный доверительный интервал
        if Q - U * math.sqrt(n) / 2 < n / 2 and Q + U * math.sqrt(n) / 2 > n / 2: 
            #Если условие выполняется, тест пройден успешно (последовательность, создаваемая генератором, близка к случайной)
            result = 'Тест пройден'
        else:
            #Инче тест не считается пройденным
            result = 'Тест не пройден'
        #Записываем в файл значение оценки Q, построенный доверительный интервал и результат выполнения теста (True or False)
        f.write('Оценка Q: '+str(Q)+'\nДоверительный интервал: ['+str(Q - U * math.sqrt(n) / 2)+'; '+str(Q + U * math.sqrt(n) / 2)+']'+'\nРезультат: '+str(result)+'\n' + '\n')
        print('Q = '+str(Q)+' | Доверительный интервал: [' + str(Q - U * math.sqrt(n) / 2) + ' ; ' + str(Q + U * math.sqrt(n) / 2) + ' ] | Результат : ' + str(result)) #Вывод в консоль 
        f.close() #Закрыть файл
        return result #Вернуть результат выполнения теста

def Test2_3(X,K,n):
    with open('output_test2_3.txt', 'a', encoding='utf-8') as f: #Открыть файл на запись
        print('\nТест на равномерность (тест №2)...') #Уведомление о запуске 2-го теста
        f.write('\nТест на равномерность (тест №2)...'+'\n') #Уведомление о запуске 2-го теста
        a = 0.05 #Уровень значимости
        U = 1.959964 #Квантиль уровня 1-a/2 нормального распределения с M = 0 (мат ожидание) D = 1 (среднеквадратичное отклонение) | Из таблиц
        #print(X)
        rightXi = [0.001, 0.8312, 3.247, 6.2621, 9.5908, 13.12, 16.791, 20.569, 24.433, 28.366, 32.357] #Квантиль уровня 1-a/2 Хи квадрат | Из таблиц
        leftXi = [5.0239, 12.833, 20.483, 27.488, 34.17, 40.646, 46.979, 53.203, 59.342, 65.41, 71.42] #Квантиль уровня a/2 Хи квадрат | Из таблиц
        result = 'Тест пройден'
        
        if K == 16:
            #Относительные частоты попаданий в интервалы
            V = [0 for i in range(K)]
            M = 0 #Обнуляем мат ожидание
            D = 0 #Обнуляем дисперсию
            n = len(X)
            for i in range(K):
                left = N / K * i
                right = N / K * (i + 1)
                for j in range(n):
                    if X[j] <= right and X[j] >= left:
                        V[i] += 1
            for i in range(K):
                V[i]/=n #Рассчитаем относительные частоты попаданий в интервалы
            #Hist(X[0:n],K) #Гистрограмма частот на K отрезках интервала [0; n)
                #Вычислим оценку математического ожидания случайной величины (пункт 5)
            for i in range(n):
                M+=X[i]
            M /= n
                #Вычислим оценку дисперсии случайной величины (пункт 6)
            for i in range(n):
                D+=(X[i] - M) ** 2
            D /= (n - 1)

            #Проверки

            #Частот
            for i in range(K): #пункт 8
                left = (V[i] - U / K * math.sqrt((K - 1) / n)) #Левое значение интервала 
                right = (V[i] + U / K * math.sqrt((K - 1) / n)) #Правое значение интервала
                f.write('Интервал для частот : ['+str(left)+';'+str(right)+']\n') #Записать в файл интервал для мат ожидания
                
                if ((1 / K < left) or (1 / K > right)): #Условие (1/K) не лежит в интервале
                    print('Тест не пройден:\nV[' + str(n) + '][' + str(i) + '] = ' + str(V[i]))
                    result = 'Тест не пройден (не прошел проверку частот)' #Присвоить результату значение False
            f.write('Частоты попаданий: '+str(V)+'\n') #Записать в файл частоты попаданий
            
            #Мат.ожиданий (пункт 9)
            left = M - U * math.sqrt(D) / math.sqrt(n) #Левое значение интервала (М - выборочное мат. ожидание)
            right = M + U * math.sqrt(D) / math.sqrt(n) #Правое значение интервала
            f.write('Математическое ожидание: '+str(M)+'\n') #Записать в файл значение мат ожидания
            f.write('Теоретическое математическое ожидание: '+str(N/2)+'\n') #Записать в файл теоретическое значение мат ожидания
            f.write('Интервал для мат ожидания : ['+str(left)+';'+str(right)+']\n') #Записать в файл интервал для мат ожидания
            if ((N / 2 < left) or (N / 2 > right)):  #Условие (N/2) не лежит в интервале
                print('Тест не пройден:\nM[' + str(n) + '] = ' + str(M))
                result = 'Тест не пройден (не прошел проверку мат ожиданий)' #Присвоить результату значение False
                
            #Дисперсий (тоже пункт 9)
            left = (n - 1) * D / leftXi[int(2)] / 10 #Левое значение интервала
            right = (n - 1) * D / rightXi[int(2)] / 10 #Правое значение интервала
            f.write('Дисперсия: '+str(D)+'\n') #Записать в файл значение дисперсии
            f.write('Теоретическая дисперсия: '+str(N ** 2 / 12)+'\n') #Записать в файл теоретическое значение дисперсии
            f.write('Интервал для дисперсии : ['+str(left)+';'+str(right)+']\n \n') #Записать в файл интервал для дисперсии
            if ((N ** 2 / 12 < left) or (N ** 2 / 12 > right)):   #Условие (N^2/12) не лежит в интервале
                print('Тест не пройден:\n D = ' + str(N ** 2 / 12) + ' | LEFT[' + str(n) + '] = ' + str(left) + ' | RIGHT[' + str(n) + '] =' + str(right))
                result = 'Тест не пройден (не прошел проверку дисперсий)' #Присвоить результату значение False
         
            
        print('Результат теста : ' + str(result)) #Вывести в консоль результат теста
        f.write('Результат теста : ' + str(result)) #Вывести в файл результат теста
        f.close() #Закрыть файл
        return result #Вернуть результат


def Test3(X,K,r):
    print('\nПроверка подпоследовательностей на случайность и равномерность (тест №3)...\n')
    T = Period()
    #print(T)
    
    X = [X[i] for i in range(T)]
    XrLen = int(len(X) / r)
    result = 'Тест пройден'
    for i in range(r):
        if not (Test1_3(X[i * (int(XrLen)):(i + 1) * (int(XrLen) - 1)], XrLen) and Test2_3(X[i * (int(XrLen)):(i + 1) * (int(XrLen) - 1)], 16, XrLen)):
            result = 'Тест не пройден'
    return result

def Xi2(l): #Критерий хи квадрат (единственный параметрический)
            #Проверяем гипотезу о согласии непрерывной случайной величины Х
    T = Period()
    #print(T)
        
    with open('output_Xi2.txt', 'a', encoding='utf-8') as f:
        print('\nПроверка простой гипотезы по критерию XI2...\n') #Уведомление о запуске проверки с помощью критерия хи квадрат
        a = 0.05 #Уровень значимости
        k = 0 #Обнуляем количество интервалов
        l = [l[i] for i in range(T)]
        #print(str(l))
        n = len(l) #Длина последовательности
        #k = int(5 * math.log10(n) - 5) 
        k = int(1 + math.log2(n)) #Количество интервалов
        Ni = [0 for i in range(k)] 
        #print(k)
        print('Длина последовательности N = ' + str(n) + ', количество интервалов K = ' + str(k)) #Вывести в консоль длину последовательности
                                                                                                  #и количество интервалов
        f.write('Длина последовательности: N = '+str(n)+'\n') #Вывести длину последовательности в файл
        f.write('Количество интервалов: К = '+str(k)+'\n') #Вывести количество интервалов в файл
        x = sorted(l) #Упорядочение элементов последовательности
        m = x[-1] + 0.0 #расчет максимального элемента
        print('Максимальный элемент max = ' + str(m)) #Вывести максимальный элемент в консоль
        f.write('Максимальный элемент: max =  '+str(m)+'\n') #Вывести максимальный элемент в файл
        interval = m / k #Шаг интервала
        print('Шаг интервала = ' + str(interval) + '\n') #Вывести шаг интервала в консоль
        f.write('Шаг интервала =  '+str(interval)+'\n') #Вывести шаг интервала в файл
        X = [ [] for i in range(k)]
        z = 0
        i = 0
        for j in range(k):
            while x[i] < interval * (j + 1):
                X[j].append(x[i])
                i+=1
        P = [] #массив вероятностей
        print('Теоретические вероятности попадания P(T)')
        
        f.write('Теоретические вероятности попадания P(T)'+'\n')
        SUMP = 0.0 #обнуляем сумму вероятностей
        for i in range(len(X)):
            P.append(1.0 / len(X))
            print(P[i]) #Вывод вероятностей в консоль
            f.write(str(P[i]) + '\n')
            SUMP += P[i] #Сумма вероятностей
            
        print('Сумма вероятностей: ' + toFixed(SUMP, 1)) #Вывести сумму вероятностей в консоль
        f.write('Сумма вероятностей: SUMP =  '+str(SUMP)+'\n') #Вывести сумму вероятностей в файл
        Sx = 0.0 #Это будет сигма в формуле (пункт 5)
        nn = float(len(x)) #А это п, на который домножается сигма в статистике хи квадрат 
        for i in range(k): #Перебираем интервалы
            ni = float(len(X[i])) #Lля каждого i-го интервала необходимо подсчитать количество попаданий элементов выборки в него (ni)
            ch = ((ni / nn - P[i]) ** 2) / P[i] #В статистике хи квадрат под знаком суммы
            Sx += ch #Заносим предыдущее значение под знак суммы
            Ni[i] = ni / nn
            print('ni = ' + str(ni) + '\tni/nn = ' + str(toFixed(ni / nn, 5)) + '\t\tPi = ' + str(P[i])) #Выводим в консоль количество попаданий
                                                                                           #элементов выборки в интервал, (ni/n) и
                                                                                           #значения теоретических вероятностей попадания в i-й интервал
            f.write('ni = ' + str(ni) + '\tni/nn = ' + str(ni / nn) + '\tPi = ' + str(P[i])+'\n')
        
        Hist1(Ni, k, N)
        print('sum = ' + str(Sx)) #Выводим в консоль сигму
        f.write('sum =  '+str(Sx)+'\n') # Выводим в файл сигму
        print('nn = ' + str(nn)) #Выводим в консоль значение n
        f.write('nn =  '+str(nn)+'\n') # Выводим в файл значение n
        Sx *= float(nn) #Домножаем сигму на n
        print('Sx = ' + str(Sx)) #Выводим статистику хи квадрат в консоль
        f.write('Sx =  '+str(Sx)+'\n') # Выводим статистику хи квадрат в файл

        r = k - 1 # число степеней свободы
        try: #Обработка исключений (конструкция try - except)
             #В блоке try мы выполняем инструкцию, которая может породить исключение
             #В блоке except мы перехватываем их
             #При этом перехватываются как само исключение, так и его потомки
            integral = si.quad(lambda s: s ** (r / 2.0 - 1) * math.exp(-s / 2.0), Sx, float('inf'))[0] #интеграл (пункт 6)
        except OverflowError: #Перехват
            integral = sys.float_info.max
        #print('integral = ' + str(integral)) #Вывести значение интеграла в консоль
        #f.write('integral =  '+str(integral)+'\n') #Вывести значение интеграла в файл
        Sresult = integral / (2 ** (r / 2.0) * math.gamma(r / 2.0)) # (пункт 6) значение P{S > S*}
        print('P {Sx > S*} = ' + str(Sresult))  #Выводим значение P {S > S*} в консоль
        f.write('P {Sx > S*} =   '+str(Sresult)+'\n') #Выводим значение P {S > S*} в файл
        print('a = ' + str(a)) #Выводим уровень значимости в консоль
        f.write('a = '+str(a)+'\n') #Выводим уровень значимости в файл
        print('r = ' + str(r)) #Выводим число степеней свободы в консоль
        f.write('r =  '+str(r)+'\n') #Выводим число степеней свободы в файл
   
        
        if Sresult > a: #Если P{S > S*} > a, где a – задаваемый уровень значимости, то нет оснований для отклонения 
                        #проверяемой гипотезы; в противном случае проверяемая гипотеза отвергается
            print('Гипотеза не отвергается')
            f.write('Гипотеза не отвергается')
        else:
            print('Гипотеза отвергается')
            f.write('Гипотеза отвергается')
        return Sresult > a #Возвращаем значение P{S > S*} > a

    
def Xi2R(l): #Критерий хи квадрат (единственный параметрический)
            #Проверяем гипотезу о согласии непрерывной случайной величины Х
    #T = Period()
    #print(T)
        
    with open('output_Xi2.txt', 'a', encoding='utf-8') as f:
        print('\nПроверка простой гипотезы по критерию XI2...\n') #Уведомление о запуске проверки с помощью критерия хи квадрат
        a = 0.05 #Уровень значимости
        k = 0 #Обнуляем количество интервалов
        #l = [l[i] for i in range(T)]
        #print(str(l))
        n = len(l) #Длина последовательности
        #k = int(5 * math.log10(n) - 5) 
        k = int(1 + math.log2(n)) #Количество интервалов
        Ni = [0 for i in range(k)] 
        #print(k)
        print('Длина последовательности N = ' + str(n) + ', количество интервалов K = ' + str(k)) #Вывести в консоль длину последовательности
                                                                                                  #и количество интервалов
        f.write('Длина последовательности: N = '+str(n)+'\n') #Вывести длину последовательности в файл
        f.write('Количество интервалов: К = '+str(k)+'\n') #Вывести количество интервалов в файл
        x = sorted(l) #Упорядочение элементов последовательности
        m = x[-1] + 0.0 #расчет максимального элемента
        print('Максимальный элемент max = ' + str(m)) #Вывести максимальный элемент в консоль
        f.write('Максимальный элемент: max =  '+str(m)+'\n') #Вывести максимальный элемент в файл
        interval = m / k #Шаг интервала
        print('Шаг интервала = ' + str(interval) + '\n') #Вывести шаг интервала в консоль
        f.write('Шаг интервала =  '+str(interval)+'\n') #Вывести шаг интервала в файл
        X = [ [] for i in range(k)]
        z = 0
        i = 0
        for j in range(k):
            while x[i] < interval * (j + 1):
                X[j].append(x[i])
                i+=1
        P = [] #массив вероятностей
        print('Теоретические вероятности попадания P(T)')
        
        f.write('Теоретические вероятности попадания P(T)'+'\n')
        SUMP = 0.0 #обнуляем сумму вероятностей
        for i in range(len(X)):
            P.append(1.0 / len(X))
            print(P[i]) #Вывод вероятностей в консоль
            f.write(str(P[i]) + '\n')
            SUMP += P[i] #Сумма вероятностей
            
        print('Сумма вероятностей: ' + toFixed(SUMP, 1)) #Вывести сумму вероятностей в консоль
        f.write('Сумма вероятностей: SUMP =  '+str(SUMP)+'\n') #Вывести сумму вероятностей в файл
        Sx = 0.0 #Это будет сигма в формуле (пункт 5)
        nn = float(len(x)) #А это п, на который домножается сигма в статистике хи квадрат 
        for i in range(k): #Перебираем интервалы
            ni = float(len(X[i])) #Lля каждого i-го интервала необходимо подсчитать количество попаданий элементов выборки в него (ni)
            ch = ((ni / nn - P[i]) ** 2) / P[i] #В статистике хи квадрат под знаком суммы
            Ni[i] = ni / nn
            Sx += ch #Заносим предыдущее значение под знак суммы
            print('ni = ' + str(ni) + '\tni/nn = ' + str(toFixed(ni / nn, 5)) + '\t\tPi = ' + str(P[i])) #Выводим в консоль количество попаданий
                                                                                           #элементов выборки в интервал, (ni/n) и
                                                                                           #значения теоретических вероятностей попадания в i-й интервал
            f.write('ni = ' + str(ni) + '\tni/nn = ' + str(ni / nn) + '\tPi = ' + str(P[i])+'\n')
        Hist1(Ni, k, N)
        print('sum = ' + str(Sx)) #Выводим в консоль сигму
        f.write('sum =  '+str(Sx)+'\n') # Выводим в файл сигму
        print('nn = ' + str(nn)) #Выводим в консоль значение n
        f.write('nn =  '+str(nn)+'\n') # Выводим в файл значение n
        Sx *= float(nn) #Домножаем сигму на n
        print('Sx = ' + str(Sx)) #Выводим статистику хи квадрат в консоль
        f.write('Sx =  '+str(Sx)+'\n') # Выводим статистику хи квадрат в файл

        r = k - 1 # число степеней свободы
        try: #Обработка исключений (конструкция try - except)
             #В блоке try мы выполняем инструкцию, которая может породить исключение
             #В блоке except мы перехватываем их
             #При этом перехватываются как само исключение, так и его потомки
            integral = si.quad(lambda s: s ** (r / 2.0 - 1) * math.exp(-s / 2.0), Sx, float('inf'))[0] #интеграл (пункт 6)
        except OverflowError: #Перехват
            integral = sys.float_info.max
        #print('integral = ' + str(integral)) #Вывести значение интеграла в консоль
        #f.write('integral =  '+str(integral)+'\n') #Вывести значение интеграла в файл
        Sresult = integral / (2 ** (r / 2.0) * math.gamma(r / 2.0)) # (пункт 6) значение P{S > S*}
        print('P {Sx > S*} = ' + str(Sresult))  #Выводим значение P {S > S*} в консоль
        f.write('P {Sx > S*} =   '+str(Sresult)+'\n') #Выводим значение P {S > S*} в файл
        print('a = ' + str(a)) #Выводим уровень значимости в консоль
        f.write('a = '+str(a)+'\n') #Выводим уровень значимости в файл
        print('r = ' + str(r)) #Выводим число степеней свободы в консоль
        f.write('r =  '+str(r)+'\n') #Выводим число степеней свободы в файл
   
        
        if Sresult > a: #Если P{S > S*} > a, где a – задаваемый уровень значимости, то нет оснований для отклонения 
                        #проверяемой гипотезы; в противном случае проверяемая гипотеза отвергается
            print('Гипотеза не отвергается')
            f.write('Гипотеза не отвергается')
        else:
            print('Гипотеза отвергается')
            f.write('Гипотеза отвергается')
        return Sresult > a #Возвращаем значение P{S > S*} > a

def A2(S): #Подпрограмма, вычисляющая значение A2 (жуткая формула с гаммой)
    res = 0 #Обнуляем значение результата
    n = 5 #Случайная выборка объема n
    try: #Обработка исключений (конструкция try - except)
         #В блоке try мы выполняем инструкцию, которая может породить исключение
         #В блоке except мы перехватываем их
         #При этом перехватываются как само исключение, так и его потомки
        for i in range(n):
            #Формула там громоздкая и тяжело читается, поэтому разобьем её на кусочки
            c = (4 * i + 1.0) #Этот кусочек отвечает за (4j+1) - уж очень часто повторяется
            s8 = 8 * S #Знаменатель в степени экспоненты
            A = (math.gamma(i + 0.5) * c) / (math.gamma(0.5) * math.gamma(i + 1.0)) #Множитель с гаммами
            B = math.exp(-(c ** 2 * math.pi ** 2 / s8)) #Множитель с первой экспонентой
            C = si.quad(lambda y: math.exp(S / (8 * (y ** 2 + 1.0)) - (c ** 2 * math.pi ** 2 * y ** 2) / s8), 0, float('inf'))[0] #Множитель-интеграл   
            res += A * B * C * (-1) ** i #Собираем по кусочкам выше описанные множители, заносим под знак суммы и внутри домножаем на (-1)^j (посчитали только сумму)
        res *= math.sqrt(2.0 * math.pi) / S #Теперь собираем всю красоту: домножаем сумму на sqrt(2Pi)/S
    except OverflowError: #Обработочка  
        print('Ошибка A2, переполнение')
    return res #Возвращаем результат (A2 по факту)

def F_rav(x, t): #F(xi,tetta)
    if x < t[0]: 
        return 0
    elif x >= t[1]:
        return 1
    return (float(x) - t[0]) / (t[1] - t[0] + 0.0)

def AndersDarling(X,N): #Критерий Андерсона-Дарлинга формулируют проверяемую гипотезу, выбирая теоретическое распределение 
                        #случайной величины, согласие которого с опытным распределением этой величины следует проверить
    print('\nПроверка гипотезы по критерию Андерсона-Дарлинга...\n') #Уведомление о запуске подпрограммы
    
    T = Period()
    X = [X[i] for i in range(T)]
    
    a = 0.05 #Уровень значимости
    X.sort() #Сортировка псевдослучайной последовательности 
             #(полученные результаты наблюдений располагают в порядке их возрастания, X[1]<X[2]<...<X[n])
    result = 0 #Обнулить значение результата
    n = len(X) #Случайная выборка (объем - длина последовательности)
    for i in range(1,n): #Цикл, пробегающий по случайной выборке
        A = (2.0 * i - 1.0) / (2.0 * n) #множитель в формуле статистики внутри суммы
        B = F_rav(X[i], [0.0, N])  #F(xi,tetta)
        result += A * math.log(B) + (1 - A) * math.log(1 - B) #Сигма в жуткой формуле критерия
    S = -n - 2 * result #Вычисление значения статистики
    print('Значение статистики: ' + 'S = ' + str(S)) #Вывод в консоль значения статистики
    a2 = A2(S) #Ещё одна жуткая формула с гаммой, вычисляется выше в отдельной подпрограмме, нам нужно a2(значения статистики S*)
    print('A2 = ' + str(a2)) #Вывод в консоль значения A2
    print('1 - A2 = ' + str(1.0 - a2)) #Вывод в консоль значния 1-A2
    result = 1 - a2 > a #В результат заносим условие 
    if result: #Если условие выполняется
        print('Гипотеза не отвергается')
    else: #Если условие не выполнено
        print('Гипотеза отвергается')
    return result #Возвращаем результат


def AndersDarlingR(X,N): #Критерий Андерсона-Дарлинга формулируют проверяемую гипотезу, выбирая теоретическое распределение 
                        #случайной величины, согласие которого с опытным распределением этой величины следует проверить
    print('\nПроверка гипотезы по критерию Андерсона-Дарлинга (встроенный генератор)...\n') #Уведомление о запуске подпрограммы

    a = 0.05 #Уровень значимости
    X.sort() #Сортировка псевдослучайной последовательности 
             #(полученные результаты наблюдений располагают в порядке их возрастания, X[1]<X[2]<...<X[n])
    result = 0 #Обнулить значение результата
    n = len(X) #Случайная выборка (объем - длина последовательности)
    for i in range(1,n): #Цикл, пробегающий по случайной выборке
        A = (2.0 * i - 1.0) / (2.0 * n) #множитель в формуле статистики внутри суммы
        B = F_rav(X[i], [0.0, N])  #F(xi,tetta)
        result += A * math.log(B) + (1 - A) * math.log(1 - B) #Сигма в жуткой формуле критерия
    S = -n - 2 * result #Вычисление значения статистики
    print('Значение статистики: ' + 'S = ' + str(S)) #Вывод в консоль значения статистики
    a2 = A2(S) #Ещё одна жуткая формула с гаммой, вычисляется выше в отдельной подпрограмме, нам нужно a2(значения статистики S*)
    print('A2 = ' + str(a2)) #Вывод в консоль значения A2
    print('1 - A2 = ' + str(1.0 - a2)) #Вывод в консоль значния 1-A2
    result = 1 - a2 > a #В результат заносим условие 
    if result: #Если условие выполняется
        print('Гипотеза не отвергается')
    else: #Если условие не выполнено
        print('Гипотеза отвергается')
    return result #Возвращаем результат


def main(): #Запуск всех подпрограмм

    if os.path.exists("output_period.txt"):
        os.remove("output_period.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    if os.path.exists("output_test1.txt"):
        os.remove("output_test1.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    if os.path.exists("output_test1_3.txt"):
        os.remove("output_test1_3.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    if os.path.exists("output_test2.txt"):
        os.remove("output_test2.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    if os.path.exists("output_test2_3.txt"):
        os.remove("output_test2_3.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    if os.path.exists("output_Xi2.txt"):
        os.remove("output_Xi2.txt") #Удаляем файл, чтобы не в нем не было лишнего после прохождения теста
    
    Generator() #Генерируем псевдослучайную последовательность
    Period() #Ищем период последовательности
    
    Test1(X,40) #Запускаем проверку перестановок (тест на случайность) для N = 40
    Test1(X,100) #Запускаем проверку перестановок (тест на случайность) для N = 100
    Test2(X,10,40) #Запускаем тест на равномерность для N = 40 и K = 10
    Test2(X,10,100) #Запускаем тест на равномерность для N = 100 и K = 10
    
    Test3(X,16,4) #Запускаем проверку подпоследовательностей на случайность и равномерность для K = 16 и r = 4  
    Xi2(X) #Запускаем проверку гипотезы с помощью критерия хи квадрат (параметрического критерия)
    Xi2R(np.random.randint(N,size=102))
    AndersDarling(X,N) #Запускаем проверку гипотезы с помощью критерия Андерсона-Дарлинга для нашей последовательности
    AndersDarlingR(np.random.randint(N,size=102),N) #Запускаем проверку гипотезы с помощью критерия Андерсона-Дарлинга для случайной последовательности
    print('\n^-^')



main()