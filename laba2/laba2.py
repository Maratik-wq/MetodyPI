# Задание 1 
""" x = "Нужно найти самое длинное слово в строке"
max = 0 
long_word = ""
i = 0
while i < len(x):
    end = x.find(" ", i)
    if end == -1:
        end = len(x)
    word = x[i:end]
    if word != "":
        if len(word) > max:
            max = len(word)
            long_word = word 
    i = end + 1 

print("Самое длинное слова в строке: ", long_word)  
 """

# Задание 2 
""" x = "Нужно;найти;самое;длинное;слово;в;строке"
max = 0 
long_word = ""
i = 0
while i < len(x):
    end = x.find(";", i)
    if end == -1:
        end = len(x)
    word = x[i:end]
    if word != "":
        if len(word) > max:
            max = len(word)
            long_word = word 
    i = end + 1 

print("Самое длинное слова в строке, разделенной точкой запятой: ", long_word)   """

# Задание 3
""" x = "Нужно?найти?самое?короткое?слово?в?строке"
y = input("Введите знак:")
min = None 
short_word = ""
i = 0
while i < len(x):
    end = x.find(y, i)
    if end == -1:
        end = len(x)
    word = x[i:end]
    if word != "":
        if min is None or len(word) < min:
            min = len(word)
            short_word = word 
    i = end +1 
print("Самое коротко слова в строке: ", short_word)  """

#задание 4
""" x = input("Введите строку: ")
y = input("Введите слово которое нужно искать: ")
f = 0
i = 0
while i < len(x): 
    end = x.find(y,i)
    if end == -1:
        break 
    print(f"слово '{y}' начинатся с позиции {end}")
    f = 1
    i = end + len(y)

if f == 0: 
    print("такого слово нету")
 """

# Задание 5 
""" x = input("Введите строку: ")
i = 0
word = 0
while i < len(x):
    end = x.find(" ", i)
    if end != -1:
        word +=1
        i = end + 1
    else:
        word +=1
        break

print("Количество слов в строке: ", word)
 """
     