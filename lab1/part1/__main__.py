from tkinter import *
from decimal import Decimal, getcontext

getcontext().prec = 100  # устанавливаем точность вычислений

def format_decimal(number, decimal_places):
    return f'{number:.{decimal_places}f}'

def on_sum_click():
    try:
        num1 = Decimal(entry_num1.get().replace(',', '.'))
        num2 = Decimal(entry_num2.get().replace(',', '.'))
        result = num1 + num2

        if abs(result) > 1000000000000:
            label_result['text'] = 'Переполнение'
        else:
            label_result['text'] = f'Результат: {format_decimal(result, 25)}'
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

def on_diff_click():
    try:
        if 'e' in entry_num1.get() or 'e' in entry_num2.get():
            raise ValueError
        num1 = Decimal(entry_num1.get().replace(',', '.'))
        num2 = Decimal(entry_num2.get().replace(',', '.'))
        result = num1 - num2

        if abs(result) > 1000000000000:
            label_result['text'] = 'Переполнение'
        else:
            label_result['text'] = f'Результат: {format_decimal(result, 25)}'
    except ValueError:
        label_result['text'] = 'Ошибка ввода'

root = Tk()
root.title('Калькулятор')
root.geometry('800x200')

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

label_result = Label(root, text='Результат:')
label_result.grid(row=3, column=0, columnspan=2)

root.mainloop()

