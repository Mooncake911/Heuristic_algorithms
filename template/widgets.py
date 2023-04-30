from tkinter import *
from tkinter import ttk
import re

from template.all_functions import USER_FUN


# region:: Spinbox class
class EditableSpinbox(ttk.Spinbox):
    """ Расширяем виджет Spinbox"""
    def __init__(self, frame, text, check_index, from_, to, increment, initial_value, name):
        # Выбираем check функцию
        check_arr = [self.is_real, self.is_border, self.is_decimals]
        check = (frame.register(check_arr[check_index]), '%P')
        # Текстовые поля tkinter
        self.var = StringVar()  # текст вводимый пользователем
        self.var.set(initial_value)
        self.errmsg = StringVar()  # текст, который выводит ошибку

        super().__init__(frame, validate='key', validatecommand=check, textvariable=self.var,
                         from_=from_, to=to, increment=increment, name=name)

        self.label = Label(frame, text=text, background="#B3E5FC")
        self.warning_label = Label(frame, fg='red', textvariable=self.errmsg, wraplength=250, background="#B3E5FC")

    def pack(self, **kwargs):
        self.label.pack(**kwargs)
        super().pack(**kwargs)
        self.warning_label.pack(**kwargs)

    def is_real(self, val) -> BooleanVar:
        """ Проверка на целое число """
        result = re.match(r"^[0-9]{0,5}$", val) is not None
        if result:
            try:
                if int(val) == 0:
                    self.errmsg.set(":: Переменная не может быть равна 0")
                    self.var.set("")
            except ValueError:
                pass
        elif len(val) > 5:
            self.errmsg.set(":: Число не должно превышать 5 цифры")
        else:
            self.errmsg.set(":: Если не можете ввести данные\n Воспользуйтесь стрелочками")
        return result

    def is_border(self, val) -> BooleanVar:
        """ Проверка на целое число +/- """
        result = re.match(r"^[-+]?\d{0,5}$", val) is not None
        if not result and len(val) > 5:
            self.errmsg.set(":: Введите целое (+/-) число не превышающее 5 цифры")
        elif not result:
            self.errmsg.set(":: Если не можете ввести данные\n Воспользуйтесь стрелочками")
        return result

    def is_decimals(self, val) -> BooleanVar:
        """ Проверка на число с точкой """
        result = re.match(r"^[0-1]?\.?\d{0,2}$", val) is not None
        if result:
            try:
                if float(val) > 1:
                    self.errmsg.set(":: Переменная не может быть больше 1")
                    self.var.set("")
            except ValueError:
                pass
        elif len(val) > 4:
            self.errmsg.set(":: Число должно удовлетворять формату 0.01~1.00")
        else:
            self.errmsg.set(":: Если не можете ввести данные\n Воспользуйтесь стрелочками")
        return result
# endregion


# region:: Combox class
class EditableCombobox(ttk.Combobox):
    """ Расширяем виджет Combobox """
    def __init__(self, frame, text, name, background="#B3E5FC"):
        super().__init__(frame, values=USER_FUN, state='readonly', name=name)
        self.label = Label(frame, text=text, background=background)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)
        super().pack(**kwargs)
# endregion


# region:: Treeview class
class EditableTreeview(ttk.Treeview):
    """ Расширяем виджет treeview """
    class PopupEntry:
        """ Класс, который определяет Entry для таблицы """
        def __init__(self, frame, x, y, width, height, entry_value):
            # Определяем окошко, которое будет накладываться на таблицу
            self.entry_var = StringVar()
            self.entry_var.set(entry_value)
            self.entry = Entry(frame, relief='flat', bg='white', textvariable=self.entry_var, font="sublime",
                               justify='center')
            self.entry.place(x=x, y=y, width=width, height=height)
            # Устанавливаем курсор в конец строки
            self.entry.focus_set()
            self.entry.icursor('end')
            # Кнопки
            self.bind_widget()
            self.entry.wait_window()

        def bind_widget(self):
            self.entry.bind("<Return>", self.rewrite_value)
            self.entry.bind('<FocusOut>', self.rewrite_value)

        def rewrite_value(self, *args):
            value = self.entry_var.get()
            self.entry_var.set(value)
            self.entry.destroy()

    def __init__(self, frame, columns, show, editable_columns=()):
        super().__init__(frame, columns=columns, show=show)
        self.frame = frame
        self.columns_name = columns
        self.editable_columns = editable_columns
        self.bind('<Double Button-1>', self.change_weight)
        self.set_config()

    def set_config(self):
        """ Устанавливаем конфигурацию для таблицы """
        scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        for i in self.columns_name:
            self.heading(column=i, text=i)

    def change_weight(self, event):
        """ Пользователь меняет вес ребра по двойному клику по клетке """
        row = self.focus()
        column = self.identify_column(event.x)
        row_index = self.index(row)
        column_index = int(column.replace("#", '')) - 1

        # Если результат не клетка или колонка не в списке редактируемых колонок, то процесс прерывается
        result = self.identify_region(event.x, event.y)
        if result != 'cell' or not (column in self.editable_columns):
            return None

        # Вызываем поля ввода Entry которое будет накладываться на клетку
        item = self.item(self.get_children()[row_index])
        current_row_values = item["values"]
        entry_var = self.PopupEntry(self.frame, *self.bbox(row, column), current_row_values[column_index]).entry_var

        # Удаляем старую строку и записываем вместо неё новую
        self.delete(row)
        current_row_values[column_index] = entry_var.get()
        self.insert("", row_index, values=current_row_values)
# endregion
