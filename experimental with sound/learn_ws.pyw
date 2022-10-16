#!/usr/bin/env python3
"""
автор программы: Султанов Искандер (BigIskander@gmail.com)
подробнее о программе:
https://iskandersultanov.wordpress.com/xuexihanzi2/

эта версия с озвучкой текста
без танцев с бубном не заработает
"""
#импортируем нужные библиотеки
import os
import sys
import os
import sys
import tkinter as tk
import tkinter.messagebox as msgb
import tkinter.filedialog as fd
import random

#для компиляции с pyinstaller
if getattr(sys, 'frozen', False):
    cdir = os.path.dirname(sys.executable)
else:
    cdir = os.path.dirname(os.path.abspath(__file__))

#глобальные переменные
file=cdir+'/words.txt'
p_article=""
words=[]
number_of_words=0
wo=0
file_load=False
option=0
correct_answer=0
answer_text=""

#Здесь и далее основные функции программы

#функция для отладки
def test():
    block()

#текст в звук
def text_to_speach(text):
    os.popen('py "' + cdir + '\play_speach.py" "' + text +'"')

#выбрать файл
def select_file():
    global file
    filename = fd.askopenfilename(filetypes=[("Text files",".txt")],
     initialdir=cdir)
    if filename!="":
        file=filename
        read_file(filename)

#открыть и прочитать файл
def read_file(filename):
    global option
    global wo
    global p_article
    global words
    global number_of_words
    try:
        with open(filename, 'rt', encoding='utf-8') as input_file:
            p_article=input_file.read()
    except:
        #действие на случай если не удалось прочитать файл
        #msgb.showinfo(title='我', message="Произошла ошибка!")
        label_1.config(text="Файл со словами: '"+os.path.basename(filename)+"'")
        option=5
        error(True)
        return None
    #написать в окне название файла
    label_1.config(text="Файл со словами: '"+os.path.basename(filename)+"'")
    #удалить первый ненужный символ из строки (похожий на пробел)
    if p_article[0:1]==u"\uFEFF":
        p_article=p_article[1:]
    #выделение отдельных слов и расположение их в случайном порядке
    words=p_article.split('\n')
    random.shuffle(words)
    number_of_words=len(words)
    #сбросить текущий прогресс
    option=0
    wo=0
    options()
    key_b()

#текст на случай ошибки
def error(opf=False):
    global file
    #заблокировать кнопки
    block()
    if opf:
        text="Не удалось открыть файл: '" + os.path.basename(file) + "'"
        text=text+"\nПроверьте наличие текстового файла '" + os.path.basename(file) + "' в папке '" + os.path.dirname(os.path.abspath(file)) + "' !"
        text=text+"\n---------------------------------------------------------------------------------------------------\n"
    else:
        text=""
    text=text+"В работе программы произошла ошибка!"
    text=text+"\nПроверьте корректность текстового файла '" + os.path.basename(file) + "' в папке '" + os.path.dirname(os.path.abspath(file)) + "' ."
    text=text+"\n---------------------------------------------------------------------------------------------------"
    text=text+"\nПравильное оформление файла:"
    text=text+"\n1) кодировка файла: utf-8"
    text=text+"\n2) в файле не должно быть пустых строк"
    text=text+"\n3) каждая строка в файле должна содержать два значения: слово на китайском 汉字 и перевод, разделенные знаком табуляции."
    text=text+"\n---------------------------------------------------------------------------------------------------"
    text=text+"\nПример строки в файле:"
    text=text+"\n汉字\tкитайские иероглифы (hànzì)"
    #text=text+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nТы долистал до конца. Поздравляю!"
    write_text(text)

#отобразить выбор опций
def options():
    #заблокировать кнопки
    block()
    #показать текст
    text="Выберите опцию:"
    text=text+"\n---------------------------------------------------------------------------------------------------"
    text=text+"\n1: тест слово перевод CNY -> RUS"
    text=text+"\n2: тест слово перевод RUS -> CNY"
    text=text+"\n3: ввести ответ 汉字"
    text=text+"\n---------------------------------------------------------------------------------------------------"
    write_text(text)
    #разблокировать только нужные кнопки
    button_2_1['state'] = 'normal'
    button_2_2['state'] = 'normal'
    button_2_3['state'] = 'normal'

#слово перевод
def chose4():
    global option
    global number_of_words
    global wo
    global correct_answer
    global word_answer
    global word_answer
    global answer_text

    try:
        #выбрать (слова) неправильные ответы
        other_words=words[:wo] + words[wo+1:]
        select_words=random.sample(other_words,3)

        #случайно выбрать правильный ответ (1-4) и смешать с неправильными
        correct_answer = random.randrange(4)
        select_words=select_words[:correct_answer] + [words[wo]] + select_words[correct_answer:]

        #отобразить варианты ответов
        if option==1:
            w_1=0
            w_2=1
        else:
            w_1=1
            w_2=0
        word_answer=words[wo].split('\t')
        answer_text=word_answer[w_1]
        answered=False
        text="Просмотрено слов: " + str(wo+1) + " из " + str(number_of_words)
        text=text+"\nВыберите правильный вариант перевода:"
        text=text+"\n----------------------------------------------------------------------------------------"
        text=text+"\n"+word_answer[w_1]
        text=text+"\n----------------------------------------------------------------------------------------"
        text=text+"\nВарианты перевода:"
        num_of_answer=0;
        for line in select_words:
            num_of_answer=num_of_answer+1
            word=line.split('\t')
            text=text+"\n"+str(num_of_answer) + ": " + word[w_2]
        write_text(text)
    except:
        #в случае ошибки
        option=5
        error()

#свободный ответ
def free():
    global option
    global wo
    global answer_text
    try:
        text="Просмотрено слов: " + str(wo+1) + " из " + str(number_of_words)
        text=text+"\nНапечатайте иероглифами 汉字 перевод:"
        word=words[wo].split('\t')
        answer_text=word[0]
        text=text+"\n----------------------------------------------------------------------------------------"
        text=text+"\n"+word[1]
        write_text(text)
    except:
        #в случае ошибки
        option=5
        error()

#все слова просмотрены
def watched():
    text="Все слова просмотрены:"
    text=text+"\n----------------------------------------------------------------------------------------"
    text=text+"\n1: Вернуться в главное меню"
    write_text(text)

#функция запускаемая 1 раз сразу после загрузки окна
def start():
    root.unbind('<Visibility>')
    #прочитать файл
    read_file(file)

#очистить текстовое поле и напечатать текст
def write_text(write):
    text['state']='normal'
    text.delete(1.0, tk.END)
    text.insert(tk.END, write)
    text['state']='disabled'

#заблокировать кнопки и поля ввода
def block():
    text['state'] = 'disabled'
    button_2_1['state'] = 'disabled'
    button_2_2['state'] = 'disabled'
    button_2_3['state'] = 'disabled'
    button_2_4['state'] = 'disabled'
    entry['state'] = 'disabled'
    button_3['state'] = 'disabled'
    button_4['state'] = 'disabled'
    button_5['state'] = 'disabled'
    button_6['state'] = 'disabled'

#кнопки клавиатуры
#привязка кнопок клавиатуры 1 - 4 может не работать с китайской раскладкой
def key_b():
    if option==0:
        root.unbind('<Return>')
        root.unbind('<Key-4>')
        root.bind('<Key-1>', lambda event: button_2_1_press())
        root.bind('<Key-2>', lambda event: button_2_2_press())
        root.bind('<Key-3>', lambda event: button_2_3_press())
        root.unbind('<Key-plus>')
    elif option==1 or option==2:
        root.unbind('<Return>')
        root.bind('<Key-1>', lambda event: button_2_1_press())
        root.bind('<Key-2>', lambda event: button_2_2_press())
        root.bind('<Key-3>', lambda event: button_2_3_press())
        root.bind('<Key-4>', lambda event: button_2_4_press())
        if option==1:
            root.bind('<Key-plus>', lambda event: button_6_press())
        else:
            root.unbind('<Key-plus>')
    elif option==3:
        root.unbind('<Key-1>')
        root.unbind('<Key-2>')
        root.unbind('<Key-3>')
        root.unbind('<Key-4>')
        root.bind('<Return>', lambda event: button_3_press())
        root.bind('<Key-plus>', lambda event: button_6_press())
    elif option==4:
        root.unbind('<Return>')
        root.unbind('<Key-2>')
        root.unbind('<Key-3>')
        root.unbind('<Key-4>')
        root.bind('<Key-1>', lambda event: button_2_1_press())
        root.unbind('<Key-plus>')

#функции обработчики нажатий кнопок
def button_1_press():
    main(1)
def button_2_1_press():
    main(2)
def button_2_2_press():
    main(3)
def button_2_3_press():
    main(4)
def button_2_4_press():
    main(5)
def button_3_press():
    main(6)
def button_4_press():
    main(7)
def button_5_press():
    main(8)
def button_6_press():
    main(9)

#главная функция программы
def main(button_p):
    global option
    global wo
    global answer_text
    if button_p==1:
        if option!=0 and option!=4 and option!=5:
            op_nfile = msgb.askyesno(message="Открыть новый файл? Текущий прогресс будет сброшен.")
        else:
            op_nfile = True
        if op_nfile:
            select_file()
        return None
    elif button_p==8:
        if option!=4:
            go_to_start = msgb.askyesno(message="Вернуться в главное меню? Текущий прогресс будет сброшен.")
        else:
            go_to_start = True
        if go_to_start:
            option=0
            wo=0
            options()
            key_b()
        return None

    if option==0:
        if button_p in range(2, 5, 1):
            if button_p==2:
                option=1
                chose4()
                button_2_4['state'] = 'normal'
                button_5['state'] = 'normal'
                button_6['state'] = 'normal'
                key_b()
            elif button_p==3:
                option=2
                chose4()
                button_2_4['state'] = 'normal'
                button_5['state'] = 'normal'
                key_b()
            else:
                option=3
                block()
                free()
                entry['state'] = 'normal'
                button_3['state'] = 'normal'
                button_4['state'] = 'normal'
                button_5['state'] = 'normal'
                button_6['state'] = 'normal'
                key_b()
                entry.focus_set()
        else:
            return None
    elif option==1 or option==2:
        if option==1 and button_p==9:
            text_to_speach(answer_text)
            return None
        #проверить ответ
        if button_p - 2 == correct_answer:
            wo=wo+1
            if wo < number_of_words:
                chose4()
            else:
                option=4
                block()
                watched()
                button_2_1['state'] = 'normal'
                button_5['state'] = 'normal'
                key_b()
    elif option==3:
        if button_p==9:
            text_to_speach(answer_text)
            return None
        if button_p==6:
            answ=entry.get()
            entry.delete(0, tk.END)
            if answer_text==answ:
                wo=wo+1
                if wo < number_of_words:
                    free()
                else:
                    option=4
                    block()
                    watched()
                    button_2_1['state'] = 'normal'
                    button_5['state'] = 'normal'
                    key_b()
        elif button_p==7:
            msgb.showinfo(message=answer_text)
            entry.focus_set()
    elif option==4:
        if button_p==2:
            option=0
            wo=0
            random.shuffle(words)
            options()
            key_b()

#msgb.showinfo(title='我', message="Все слова просмотрены!")

#Отсюда и ниже код отвечающий за графический интерфейс программы

#создать окно и задать свойства
root = tk.Tk()
#root.protocol("WM_DELETE_WINDOW", exit)
root.title("我学习汉字")
root.geometry("700x550")
root.resizable(False, False)
root.bind('<Visibility>', lambda event: start())
#root.bind('<Key>', lambda event: msgb.showinfo(title='我', message=event))

#отобразить какой файл со словами выбран
frame_1 = tk.Frame(root, pady=5, padx=5)
label_1 = tk.Label(frame_1, text="Файл со словами: 'words.txt'", font=("Helvetica", 14))
frame_1.pack(side='top', fill='x', expand=True)
label_1.pack(side='left')

#кнопка открыть другой файл со словами и кнопка главное меню
frame_2 = tk.Frame(root, padx=5)
button_1 = tk.Button(frame_2, text="Открыть другой файл", font=("Helvetica", 12), command=button_1_press)
button_6 = tk.Button(frame_2, text="Озвучить", font=("Helvetica", 12), command=button_6_press)
button_5 = tk.Button(frame_2, text="Главное меню", font=("Helvetica", 12), command=button_5_press)
frame_2.pack(side='top', fill='x', expand=True)
button_1.pack(side='left')
button_5.pack(side='right')
button_6.pack(side='right')

#создать большое текстовое поле и задать свойства
frame_3 = tk.Frame(root, pady=5, padx=5)
text = tk.Text(frame_3, height=15, font=("Helvetica", 14))
scroll = tk.Scrollbar(frame_3)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
frame_3.pack(fill='x')
scroll.pack(side='right', fill='both')
text.pack(side='left', fill='x')

#ряд кнопок 1 - 4
frame_4 = tk.Frame(root, pady=5, padx=5)
button_2_1 = tk.Button(frame_4, text="1", font=("Helvetica", 12), command=button_2_1_press)
button_2_2 = tk.Button(frame_4, text="2", font=("Helvetica", 12), command=button_2_2_press)
button_2_3 = tk.Button(frame_4, text="3", font=("Helvetica", 12), command=button_2_3_press)
button_2_4 = tk.Button(frame_4, text="4", font=("Helvetica", 12), command=button_2_4_press)
frame_4.pack(fill='x',expand=True)
button_2_1.pack(fill='x',expand=True,side='left')
button_2_2.pack(fill='x',expand=True,side='left')
button_2_3.pack(fill='x',expand=True,side='left')
button_2_4.pack(fill='x',expand=True,side='left')

#свободный ответ
frame_5 = tk.Frame(root, pady=5, padx=5)
entry = tk.Entry(frame_5, font=("Helvetica", 14))
button_3 = tk.Button(frame_5, text="Ответить <Enter>", font=("Helvetica", 12), command=button_3_press)
button_4 = tk.Button(frame_5, text="Ответ", font=("Helvetica", 12), command=button_4_press)
frame_5.pack(fill='x',expand=True)
entry.pack(fill='x',expand=True,side='left')
button_3.pack(fill='x',side='left')
button_4.pack(fill='x',side='left')

#о программе, ссылка на сайт
frame_6 = tk.Frame(root, padx=5)
label_2 = tk.Label(frame_6, text="О программе:", font=("Helvetica", 12))
frame_6.pack(fill='x',expand=True)
label_2.pack(fill='x',side='left')
frame_7 = tk.Frame(root, padx=5)
label_3 = tk.Label(frame_7, text="https://iskandersultanov.wordpress.com/xuexihanzi2/", font=("Helvetica", 12))
frame_7.pack(fill='x',expand=True)
label_3.pack(fill='x',side='left')

#отобразить окно
root.mainloop()
