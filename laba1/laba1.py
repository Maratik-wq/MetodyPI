# Задание 1 
""" import math
x = int(input("Введите чилсло от 1 до 9: "))
if x >= 1 and x <= 3:
    s = input("Введите строку: ")
    n = int(input("Введите число для повторов строки: "))
    for _ in range(n):
        print(s)
elif x >= 4 and x <= 6:
    m = int(input("Введите степень в которую следует возвести число: "))
    print(pow(x, m))
elif x >= 7 and x <= 9:
    for _ in range(10):
        x+=1
        print(x)
else:
    print("Ошибка ввода") """
    

# Задание 2
print("Общество в начале XXI века")
x = int(input("Введите свой возраст: "))
if x > 0 and x < 7:
    print("Вам в детский сад")
elif x >= 7 and x < 18:
    print("Вам в школу")
elif x >= 18 and x < 25:
    print("Вам в профессиональное учебное заведение")
elif x >= 25 and x < 60:
    print("Вам на работу")
elif x >= 60 and x <= 120:
    print("Вам предоставляется выбор")
else: 
    for _ in range(5): 
        print("Ошибка! Это программа для людей!")
