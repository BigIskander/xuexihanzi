#!/usr/bin/env python3
"""
автор программы: Султанов Искандер (BigIskander@gmail.com)
подробнее о программе:
https://iskandersultanov.wordpress.com/xuexihanzi2/
"""
#импортируем нужные библиотеки
import os
import sys
import tkinter as tk
import tkinter.messagebox as msgb
import tkinter.filedialog as fd
import random
import webbrowser

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
option=-1
correct_answer=0
answer_text=""
#временная подцветка кнопок
wait=200
correct_color="#00FF00"
wrong_color="#FF0000"

#Здесь и далее основные функции программы

#на сайт программы
site_link="https://iskandersultanov.wordpress.com/xuexihanzi2/"
def about():
    op_site = msgb.askyesno(message="Перейти на сайт программы?")
    if op_site:
        webbrowser.open_new(site_link)

#функция для отладки
def test():
    block()

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
    #проверка корректности файлами
    if not check_me():
        option=-2
        main()
        return None
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
        text=text+"\n-------------------------------------"
    else:
        text=""
    text=text+"В работе программы произошла ошибка!"
    text=text+"\nПроверьте корректность текстового файла '" + os.path.basename(file) + "' в папке '" + os.path.dirname(os.path.abspath(file)) + "' ."
    text=text=text+"\n-------------------------------------"
    text=text+"\nПравильное оформление файла:"
    text=text+"\n1) кодировка файла: utf-8"
    text=text+"\n2) в файле не должно быть пустых строк"
    text=text+"\n3) каждая строка в файле должна содержать два значения: слово на китайском 汉字 и перевод, разделенные знаком табуляции."
    text=text=text+"\n-------------------------------------"
    text=text+"\nПример строки в файле:"
    text=text+"\n汉字\tкитайские иероглифы (hànzì)"
    #text=text+"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nТы долистал до конца. Поздравляю!"
    write_text(text)

def incorrect_file():
    block()
    text="Файл со словами оформлен не верно."
    text=text+"\n"
    text=text+"\nПрожалуйста, проверьте корректность оформления текстового файла '" + os.path.basename(file) + "' в папке '" + os.path.dirname(os.path.abspath(file)) + "' ."
    text=text+"\nИли выберите другой файл."
    text=text+"\n"
    text=text+"\nПравильное оформление файла со словами:"
    text=text+"\n1) файл с расширением .txt в кодировке: utf-8"
    text=text+"\n2) в файле не должно быть пустых строк"
    text=text+"\n3) каждая строка в файле должна содержать два значения: слово на китайском 汉字 и перевод, разделенные знаком табуляции."
    text=text+"\n(знак табуляции \t - это знак, который печатается когда на клавиатуре нажимаешь клавишу Tab)"
    text=text+"\n"
    text=text+"\nПример строки в файле:"
    text=text+"\n汉字\tкитайские иероглифы (hànzì)"
    write_text(text)

def intital():
    block()
    label_1.config(text="Файл со словами: не выбран")
    text="Добро пожаловать!"
    text=text+"\nЭто программа для запоминания китайских слов."
    text=text+"\nПожалуйста, откроте текстовый файл со словами, которые желаете запомнить."
    text=text+"\n"
    text=text+"\nПравильное оформление файла со словами:"
    text=text+"\n1) файл с расширением .txt в кодировке: utf-8"
    text=text+"\n2) в файле не должно быть пустых строк"
    text=text+"\n3) каждая строка в файле должна содержать два значения: слово на китайском 汉字 и перевод, разделенные знаком табуляции."
    text=text+"\n(знак табуляции \t - это знак, который печатается когда на клавиатуре нажимаешь клавишу Tab)"
    text=text+"\n"
    text=text+"\nПример строки в файле:"
    text=text+"\n汉字\tкитайские иероглифы (hànzì)"
    write_text(text)

#отобразить выбор опций
def options():
    #заблокировать кнопки
    block()
    #показать текст
    text="Колличество слов для изучения: " + str(number_of_words)
    text=text+"\n"
    text=text+"\nВыберите упражнение:"
    text=text+"\n-------------------------------------"
    text=text+"\n1: тест слово перевод CNY -> RUS"
    text=text+"\n2: тест слово перевод RUS -> CNY"
    text=text+"\n3: ввести передов слова на китайский 汉字"
    text=text+"\n-------------------------------------"
    text=text+"\n"
    write_text(text)
    #разблокировать только нужные кнопки
    button_2_1['state'] = 'normal'
    button_2_2['state'] = 'normal'
    button_2_3['state'] = 'normal'

#функция экспресс проверки корректности файла со словами
def check_me():
    if len(p_article)<=0:
        return False
    words=p_article.split('\n')
    num=len(words)
    if num<=0:
        return False
    else:
        for word in words:
            sp_word=word.split('\t')
            if not len(sp_word)==2:
                return False;
            else:
                if (sp_word[0]=="" or sp_word[1]=="") or (sp_word[0]==None or sp_word[1]==None):
                    return False
    return True

#слово перевод
def chose4():
    global option
    global number_of_words
    global wo
    global correct_answer

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
        answered=False
        text="Просмотрено слов: " + str(wo+1) + " из " + str(number_of_words)
        text=text+"\nВыберите правильный вариант перевода:"
        text=text+"\n-------------------------------------"
        text=text+"\n"+word_answer[w_1]
        text=text+"\n-------------------------------------"
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
        text=text+"\n-------------------------------------"
        text=text+"\n"+word[1]
        write_text(text)
    except:
        #в случае ошибки
        option=5
        error()

#все слова просмотрены
def watched():
    text="Все слова просмотрены:"
    text=text+"\n-------------------------------------"
    text=text+"\n1: Вернуться в главное меню"
    write_text(text)

#функция запускаемая 1 раз сразу после загрузки окна
def start():
    root.unbind('<Visibility>')
    #
    main()

#очистить текстовое поле и напечатать текст
def write_text(write):
    text['state']='normal'
    text.delete(1.0, tk.END)
    text.insert(tk.END, write)
    text['state']='disabled'

#заблокировать кнопки и поля ввода
def block():
    entry.delete(0, tk.END)
    text['state'] = 'disabled'
    button_2_1['state'] = 'disabled'
    button_2_2['state'] = 'disabled'
    button_2_3['state'] = 'disabled'
    button_2_4['state'] = 'disabled'
    entry['state'] = 'disabled'
    button_3['state'] = 'disabled'
    button_4['state'] = 'disabled'
    button_5['state'] = 'disabled'

#кнопки клавиатуры
#привязка кнопок клавиатуры 1 - 4 может не работать с китайской раскладкой
def key_b():
    if option==-1 or option==-2:
        root.unbind('<Return>')
        root.unbind('<Key-1>')
        root.unbind('<Key-2>')
        root.unbind('<Key-3>')
        root.unbind('<Key-4>')
    elif option==0:
        root.unbind('<Return>')
        root.unbind('<Key-4>')
        root.bind('<Key-1>', lambda event: button_2_1_press())
        root.bind('<Key-2>', lambda event: button_2_2_press())
        root.bind('<Key-3>', lambda event: button_2_3_press())
    elif option==1 or option==2:
        root.unbind('<Return>')
        root.bind('<Key-1>', lambda event: button_2_1_press())
        root.bind('<Key-2>', lambda event: button_2_2_press())
        root.bind('<Key-3>', lambda event: button_2_3_press())
        root.bind('<Key-4>', lambda event: button_2_4_press())
    elif option==3:
        root.unbind('<Key-1>')
        root.unbind('<Key-2>')
        root.unbind('<Key-3>')
        root.unbind('<Key-4>')
        root.bind('<Return>', lambda event: button_3_press())
    elif option==4:
        root.unbind('<Return>')
        root.unbind('<Key-2>')
        root.unbind('<Key-3>')
        root.unbind('<Key-4>')
        root.bind('<Key-1>', lambda event: button_2_1_press())

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

#color back to default
def color_default(obj):
    if os.name=="nt":
        obj['bg']="SystemButtonFace"

#главная функция программы
def main(button_p=None):
    global option
    global wo
    if button_p==1:
        if option not in [-2, -1, 0, 4, 5]:
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

    if option==-1:
        key_b()
        intital()
    elif option==-2:
        key_b()
        incorrect_file()
    elif option==0:
        if button_p in range(2, 5, 1):
            if button_p==2:
                option=1
                chose4()
                button_2_4['state'] = 'normal'
                button_5['state'] = 'normal'
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
                key_b()
                entry.focus_set()
        else:
            return None
    elif option==1 or option==2:
        #проверить ответ
        if button_p - 2 == correct_answer:
            #временное окрашивание кнопки
            if os.name == "nt":
                butt_num="!button"
                if (button_p - 1)!=1:
                    butt_num=butt_num + str(button_p - 1)
                root.children['!frame4'].children[butt_num]['bg']=correct_color
                root.after(ms=wait, func=lambda: color_default(root.children['!frame4'].children[butt_num]))
            #конец временное окрашивание кнопки

            #действие на случай верного ответа
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
        elif button_p in range(2, 6, 1):
            #временное окрашивание кнопки
            if os.name == "nt":
                butt_num="!button"
                if (button_p - 1)!=1:
                    butt_num=butt_num + str(button_p - 1)
                root.children['!frame4'].children[butt_num]['bg']=wrong_color
                root.after(ms=wait, func=lambda: color_default(root.children['!frame4'].children[butt_num]))
            #конец временное окрашивание кнопки
    elif option==3:
        if button_p==6:
            answ=entry.get()
            entry.delete(0, tk.END)
            if answer_text==answ:
                #временное окрашивание кнопки
                if os.name == "nt":
                    butt_num="!button"
                    root.children['!frame5'].children[butt_num]['bg']=correct_color
                    root.after(ms=wait, func=lambda: color_default(root.children['!frame5'].children[butt_num]))
                #конец временное окрашивание кнопки

                #действие на случай верного ответа
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
            else:
                #временное окрашивание кнопки
                if os.name == "nt":
                    butt_num="!button"
                    root.children['!frame5'].children[butt_num]['bg']=wrong_color
                    root.after(ms=wait, func=lambda: color_default(root.children['!frame5'].children[butt_num]))
                #конец временное окрашивание кнопки
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

def font_change(*args):
    text['font']=("Helvetica", font_size.get())
    entry['font']=("Helvetica", font_size.get())


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
#выбор шрифта
font_size_options=(12, 14, 16, 18 , 20)
font_size=tk.StringVar(frame_2)
font_size.set(14)
font_size.trace("w", font_change)
#
select_font_menu=tk.OptionMenu(frame_2, font_size, *font_size_options)
select_font_label=tk.Label(frame_2, text="Размер шрифта:", font=("Helvetica", 12))
button_5 = tk.Button(frame_2, text="Главное меню", font=("Helvetica", 12), command=button_5_press)
frame_2.pack(side='top', fill='x', expand=True)
button_1.pack(side='left')

button_5.pack(side='right')
select_font_menu.pack(side='right')
select_font_label.pack(side='right')

#создать большое текстовое поле и задать свойства
frame_3 = tk.Frame(root, pady=5, padx=5, height=345)
frame_3.pack_propagate(False)
text = tk.Text(frame_3, font=("Helvetica", 14))
scroll = tk.Scrollbar(frame_3)
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
frame_3.pack(fill='x')
scroll.pack(side='right', fill='y')
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
label_3 = tk.Label(frame_7, text=site_link, font=("Helvetica", 12))
frame_7.pack(fill='x',expand=True)
label_3.pack(fill='x',side='left')
label_3.bind("<Button-1>", lambda event: about())

#отобразить окно
root.mainloop()
