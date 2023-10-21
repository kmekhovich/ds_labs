from tkinter import *
from decimal import Decimal, getcontext
import re

getcontext().prec = 100  # устанавливаем точность вычислений

def is_valid_input(s):
    if s[0] == '+' or s[0] == '-':
        s = s[1:]
    a = s.replace(',', '.').split('.')
    if len(a) > 1:
        if ' ' in a[1]:
            return False
    b = a[0].split(' ')
    if len(b) > 1:
        if len(b[0]) > 3:
            return False
        for bs in b[1:]:
            if len(bs) != 3:
                return False
    return True

def parse_input(input_str):
    try:
        return Decimal(input_str.replace(' ', '').replace(',', '.'))
    except:
        raise ValueError

def format_decimal(number, decimal_places):
    result = f'{number:.{decimal_places}f}'
    int_part, dec_part = result.split('.')
    int_part = '{:,}'.format(int(int_part)).replace(',', ' ')  # Группируем по 3 разряда
    return f'{int_part}.{dec_part}'

def on_sum_click():
    try:
        if is_valid_input(entry_num1.get()) and is_valid_input(entry_num2.get()):
            num1 = parse_input(entry_num1.get())
            num2 = parse_input(entry_num2.get())
            result = num1 + num2

            if abs(result) > 1000000000000:
                label_result['text'] = 'Переполнение'
            else:
                label_result['text'] = f'Результат: {format_decimal(result, 6)}'
        else:
            raise ValueError
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

def on_diff_click():
    try:
        if is_valid_input(entry_num1.get()) and is_valid_input(entry_num2.get()):
            num1 = parse_input(entry_num1.get())
            num2 = parse_input(entry_num2.get())
            result = num1 - num2

            if abs(result) > 1000000000000:
                label_result['text'] = 'Переполнение'
            else:
                label_result['text'] = f'Результат: {format_decimal(result, 6)}'
        else:
            raise ValueError
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

def on_mult_click():
    try:
        if is_valid_input(entry_num1.get()) and is_valid_input(entry_num2.get()):
            num1 = parse_input(entry_num1.get())
            num2 = parse_input(entry_num2.get())
            result = num1 * num2

            if abs(result) > 1000000000000:
                label_result['text'] = 'Переполнение'
            else:
                label_result['text'] = f'Результат: {format_decimal(result, 6)}'
        else:
            raise ValueError
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

def on_div_click():
    try:
        if is_valid_input(entry_num1.get()) and is_valid_input(entry_num2.get()):
            num1 = parse_input(entry_num1.get())
            num2 = parse_input(entry_num2.get())
            if num2 == 0:
                raise ZeroDivisionError
            else:
                result = num1 / num2

            if abs(result) > 1000000000000:
                label_result['text'] = 'Переполнение'
            else:
                label_result['text'] = f'Результат: {format_decimal(result, 6)}'
        else:
            raise ValueError
    except ZeroDivisionError:
        label_result['text'] = 'Деление на ноль'
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

root = Tk()
root.title('Калькулятор')

label_info = Label(root, text='Мехович Константин, 4 группа, 4 курс, 2023')
label_info.grid(row=0, column=0, columnspan=2)

entry_num1 = Entry(root)
entry_num1.grid(row=1, column=0)

entry_num2 = Entry(root)
entry_num2.grid(row=1, column=1)

button_sum = Button(root, text='Сложение', command=on_sum_click)
button_sum.grid(row=2, column=0)

button_diff = Button(root, text='Вычитание', command=on_diff_click)
button_diff.grid(row=2, column=1)

button_mult = Button(root, text='Умножение', command=on_mult_click)
button_mult.grid(row=3, column=0)

button_div = Button(root, text='Деление', command=on_div_click)
button_div.grid(row=3, column=1)

label_result = Label(root, text='Результат:')
label_result.grid(row=4, column=0, columnspan=2)

root.mainloop()

