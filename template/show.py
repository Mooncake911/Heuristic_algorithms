from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import math
from template.widgets import EditableTreeview


# region: /////-- ~Приложение выводящее результат в виде изображения~ --\\\\\ #
class ShowResult:
    def __init__(self, data, max_i, frame_btn, frame_scroll, snapshot_name):
        # Фреймы
        self.frame_btn = frame_btn
        self.frame_scroll = frame_scroll
        self.clean_old_results()
        # Счётчик для изображений
        self.i = 1
        self.max_i = max_i
        self.snapshot_name = snapshot_name
        # Рамка для наших изображений
        self.photo = None
        self.canvas = Canvas(self.frame_btn, width=420, height=345, background="#B3E5FC", highlightthickness=0)
        self.canvas.grid(column=0, row=0, columnspan=2)
        self.show_img()
        # Создаем виджет таблицы
        self.data = data
        self.treeview = ttk.Treeview(self.frame_scroll, columns=list(self.data.columns), show='headings')
        self.treeview.pack(side=LEFT, fill=BOTH, expand=True)
        self.show_table()
        # Кнопки для перелистывания изображений
        self.button_next = ttk.Button(self.frame_btn, text="Следующее", command=self.next_img, state=NORMAL)
        self.button_next.grid(row=1, column=0)
        self.button_back = ttk.Button(self.frame_btn, text="Предыдущее", command=self.previous_img, state=DISABLED)
        self.button_back.grid(row=1, column=1)

    def next_img(self) -> None:
        if self.i == self.max_i:
            self.button_next.configure(state=DISABLED)
        else:
            self.i += 1
            self.button_back.configure(state=NORMAL)
            self.show_img()

    def previous_img(self) -> None:
        if self.i == 1:
            self.button_back['state'] = DISABLED
        else:
            self.i -= 1
            self.button_next['state'] = NORMAL
            self.show_img()

    def show_img(self) -> None:
        try:
            self.photo = ImageTk.PhotoImage(Image.open("{0}/{1}{2}.png".format(self.snapshot_name,
                                                                               self.snapshot_name, self.i)))
            self.canvas.create_image(3, 3, anchor='nw', image=self.photo)
        except FileNotFoundError:
            pass

    def show_table(self) -> None:
        # Добавляем колонки в таблицу
        for col in self.data.columns:
            self.treeview.heading(col, text=col)
        # Добавляем строки в таблицу и заполняем значения ячеек данными из дата-фрейма
        for i, row in self.data.iterrows():
            self.treeview.insert('', END, values=list(row))
        # Создаем scrollbar widget и добавляем его в таблицу
        scrollbar = ttk.Scrollbar(self.frame_scroll, orient=VERTICAL, command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def clean_old_results(self) -> None:
        for widget in self.frame_btn.winfo_children():
            widget.destroy()
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()


# endregion


# region: /////-- ~Приложение выводящее результат в виде графа~ --\\\\\ #
class ShowGraph:
    class Point:
        """ Внутренний класс определяющий параметры точки для отображения в canvas"""

        def __init__(self, x, y, index, frame):
            self.x = x
            self.y = y
            self.index = index
            self.label = Label(frame, text="{}".format(self.index), font=('Helvetica bold', 7), bg="red")
            self.label.place(x=x, y=y, anchor="center")

        def delete_point(self) -> None:
            self.label.destroy()

    def buttons_state(self, state) -> None:
        self.btn_del_all.configure(state=state)
        self.btn_del_one.configure(state=state)

    def __init__(self, frame_btn, frame_scroll, frame_input):
        """ Основной класс в котором прописана логика визуализации графа """
        self.points = []
        self.graphPaths = []
        self.index = 0
        # Объявляем фреймы
        self.frame_btn = frame_btn
        self.frame_scroll = frame_scroll
        self.frame_input = frame_input

        # Создаём рабочее пространство пользователя
        self.canvas = Canvas(self.frame_btn, width=500, height=310, background="#B3E5FC", highlightthickness=0)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        # Создаём таблицу для координат и для рёбер
        self.cycle_table = EditableTreeview(self.frame_input, columns=("P1", "P2", "Ребро"), show="headings")
        self.cycle_table.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.cycle_table.column("# 1", anchor=CENTER, stretch=NO, width=100)
        self.cycle_table.column("# 2", anchor=CENTER, stretch=NO, width=100)
        self.cycle_table.column("# 3", anchor=CENTER, stretch=NO)
        self.cycle_table.configure(height=5)
        self.edge_table = EditableTreeview(self.frame_scroll, columns=("P1", "P2", "Ребро"), show='headings',
                                           editable_columns=["#3"])
        self.edge_table.pack(side=LEFT, fill=BOTH, expand=True)

        # Кнопки для отрисовки и удаления точек
        self.canvas.bind("<Button-1>", self.add_point)
        self.btn_del_all = ttk.Button(self.frame_btn, text="Удалить всё", command=self.clear_points, state=NORMAL)
        self.btn_del_all.pack()
        self.btn_del_one = ttk.Button(self.frame_btn, text="Удалить последнюю", command=self.clear_point, state=NORMAL)
        self.btn_del_one.pack()

    def draw_points(self, rout=None) -> None:
        """ Рисует точки """
        self.canvas.delete("all")
        # Рисуем точки
        for p in self.points:
            self.canvas.create_oval(p.x - 15, p.y - 15, p.x + 15, p.y + 15, fill="red")
        # Две вариации отображения рёбер (полный граф и Гамильтонов цикл)
        if rout is None:
            # Очищаем старые рёбра
            for row in self.edge_table.get_children():
                self.edge_table.delete(row)
            # Рисуем новые
            self.draw_lines()
        else:
            # Очищаем старые рёбра
            for row in self.cycle_table.get_children():
                self.cycle_table.delete(row)
            # Рисуем новые
            self.draw_cycle(rout)

    def draw_lines(self) -> None:
        """ Рисует полный граф """
        for p1 in self.points:
            for p2 in self.points[p1.index:]:
                self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="black")
                edge_length = int(math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2))
                self.edge_table.insert("", "end", values=(p1.index, p2.index, edge_length))

    def draw_cycle(self, route) -> None:
        """ Рисует цикл """
        for i in range(len(route) - 1):
            from_ = min(route[i], route[i + 1])
            to_ = max(route[i], route[i + 1])
            p1 = self.points[from_]
            p2 = self.points[to_]
            self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="red")
            self.cycle_table.insert("", "end", values=(p1.index, p2.index, self.graphPaths[from_][to_ - from_ - 1]))

    def add_point(self, event) -> None:
        """ Добавляет 1 точку """
        self.index += 1
        x = event.x
        y = event.y
        self.points.append(self.Point(x, y, self.index, self.canvas))
        self.draw_points()
        self.buttons_state(NORMAL)

    def clear_points(self) -> None:
        """ Удаляет все точки """
        self.index = 0
        for p in self.points:
            p.delete_point()
        self.points = []
        self.draw_points()
        self.buttons_state(DISABLED)

    def clear_point(self) -> None:
        """ Удаляет 1 точку """
        self.index -= 1
        self.points[-1].delete_point()
        self.points = self.points[:-1]
        self.draw_points()
        if self.index == 0:
            self.buttons_state(DISABLED)

    def prepare_graphPaths(self) -> None:
        """ Представляем список путей в удобном формате"""
        self.graphPaths = []
        values = []
        amount_edges = len(self.points) - 1
        for row in self.edge_table.get_children():
            if len(values) < amount_edges:
                values.append(self.edge_table.item(row)["values"][2])
            else:
                self.graphPaths.append(values)
                amount_edges -= 1
                values = [self.edge_table.item(row)["values"][2]]
        self.graphPaths.append(values)
# endregion
