#автор программы: Султанов Искандер (BigIskander@gmail.com)
#подробнее о программе:
# https://iskandersultanov.wordpress.com/xuexihanzi/
from os import system, name
import random

#название текстового файла со словами
file='words.txt'

#очистка экрана
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

#поменять кодировку консоли, для отображения китайских символов
if name == 'nt':
    system('chcp 936')

#текст на случай ошибки в программе
def error_text():
    print("В работе программы произошла ошибка!")
    print("Проверьте корректность текстового файла " + file + " в папке с программой")
    print("правильное оформление файла:")
    #по английски так как руские надписи в китайской кодировке отображаются криво
    print("1) file encoding: utf-8")
    print("2) no empty lines")
    print("3) each line should consists of 汉字 and translation separate by tabulation symbol:")
    print("for example:")
    print("汉字\tchinese characters (hànzì)")

#прочитать файл со словами сохраненный в кодировке utf-8
try:
    with open(file, 'rt', encoding='utf-8') as input_file:
        p_article=input_file.read()
except:
    #если файл не открывается то вывести ошибку
    clear()
    print('Не удалось открыть файл: ' + file)
    print('Проверьте наличие текстового файла ' + file + ' в папке с программой!')
    print("--------------------------------------------")
    error_text()
    input()
    exit()

#отловить ошибки
try:
    #основная часть программы
    #удалить первый ненужный символ из строки (похожий на пробел)
    if p_article[0:1]==u"\uFEFF":
        p_article=p_article[1:]
    #выделение отдельных слов и расположение их в случайном порядке
    words=p_article.split('\n')
    random.shuffle(words)
    number_of_words=len(words)

    #выбрать опцию
    opt_selected=False
    while not opt_selected:
        clear()
        print("Выбрать опцию:", sep='')
        print("--------------------------------------------")
        print("1: тест слово перевод CNY -> RUS")
        print("2: тест слово перевод RUS -> CNY")
        print("3: ввести ответ 汉字")
        print("--------------------------------------------")
        print("Выбранная опция:")
        opt=input()
        if opt.isdigit():
            opt=int(opt)
            if opt==1 or opt==2 or opt==3:
                opt_selected=True

    #цикл слово перевод
    if opt==1 or opt==2:
        for wo in range(len(words)):
            #выбрать (слова) неправильные ответы
            other_words=words[:wo] + words[wo+1:]
            select_words=random.sample(other_words,3)

            #случайно выбрать правильный ответ (1-4) и смешать с неправильными
            correct_answer = random.randrange(4)
            select_words=select_words[:correct_answer] + [words[wo]] + select_words[correct_answer:]

            #отобразить варианты ответов
            #цикл пока правильно не ответишь
            word_answer=words[wo].split('\t')
            answered=False
            while not answered:
                clear()
                print(str(wo) + " из " + str(number_of_words))
                print("--------------------------------------------")
                print("Слово:")
                print(word_answer[opt-1])
                print("--------------------------------------------")
                print("Варианты ответа:")
                num_of_answer=0;
                for line in select_words:
                    num_of_answer=num_of_answer+1
                    word=line.split('\t')
                    print(str(num_of_answer) + ":" + word[opt-2])

                print("--------------------------------------------")
                print("Ответ:")
                answer=input()
                print(answer)
                if answer.isdigit():
                    if int(answer) - 1 == correct_answer:
                        answered=True

    elif opt==3:
        #цикл по словам, ввод правильного ответа в консоль
        counter=-1
        for line in words:
            counter=counter+1
            word=line.split('\t')
            input_word="\n"
            #цикл пока правильно не введешь слово
            while input_word!=word[0]:
                clear()
                print(str(counter) + " из " + str(number_of_words))
                print("--------------------------------------------")
                print("Слово:")
                print(word[1])
                print("--------------------------------------------")
                print("Перевод 汉字:")
                input_word=input()

    clear()
    print("Все слова просмотрены, для повтора запустите программу заново!")
    input()

#вывести текст в случае ошибки в программе
except:
    clear()
    error_text()
    input()
