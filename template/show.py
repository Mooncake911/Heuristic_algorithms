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
    def buttons_state(self, state) -> None:
        self.btn_del_all.configure(state=state)
        self.btn_del_one.configure(state=state)

    def __init__(self, frame_btn, frame_scroll, frame_input):
        """ Основной класс в котором прописана логика визуализации графа """
        self.points = []
        self.graphPaths = []
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

        # Кнопки для взаимодействия пользователя с программой
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<B1-Motion>", self.on_button_motion)
        self.point_size = 15

        # Кнопки для удаления вершин
        self.btn_del_all = ttk.Button(self.frame_btn, text="Удалить всё", command=self.clear_points, state=NORMAL)
        self.btn_del_all.pack()
        self.btn_del_one = ttk.Button(self.frame_btn, text="Удалить последнюю", command=self.clear_point, state=NORMAL)
        self.btn_del_one.pack()

    def draw_lines(self) -> None:
        """ Рисует полный граф """
        # Очищаем старые значения из таблицы
        self.canvas.delete("all")
        for row in self.edge_table.get_children():
            self.edge_table.delete(row)
        # Добавляем новые
        for p1 in self.points:
            p1_index = self.points.index(p1) + 1
            for p2 in self.points[p1_index:]:
                p2_index = self.points.index(p2) + 1
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="gray", capstyle=ROUND)
                edge_length = int(math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2))
                self.edge_table.insert("", "end", values=(p1_index, p2_index, edge_length))
            self.canvas.create_oval(p1[0] - self.point_size, p1[1] - self.point_size,
                                    p1[0] + self.point_size, p1[1] + self.point_size, fill='red')
            self.canvas.create_text(p1[0], p1[1], text=p1_index, fill='black')

    def draw_cycle(self, route) -> None:
        """ Рисует цикл """
        # Очищаем старые значения из таблицы
        for row in self.cycle_table.get_children():
            self.cycle_table.delete(row)
        # Добавляем новые
        for i in range(len(route) - 1):
            from_ = min(route[i], route[i + 1])
            to_ = max(route[i], route[i + 1])
            p1 = self.points[from_]
            p2 = self.points[to_]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="red", width=2)
            p1_index = self.points.index(p1) + 1
            p2_index = self.points.index(p2) + 1
            self.cycle_table.insert("", "end", values=(p1_index, p2_index, self.graphPaths[from_][to_ - from_ - 1]))

    def add_point(self, event) -> None:
        """ Добавляет 1 точку """
        x, y = event.x, event.y
        try:
            item = self.canvas.find_closest(x, y)[0]
            start_x, start_y = self.canvas.coords(item)[:2]
            if max(abs(start_x - x), abs(start_y - y)) > self.point_size * 2:
                self.points.append([x, y])
        except IndexError:
            self.points.append([x, y])
            self.buttons_state(NORMAL)
        self.draw_lines()

    def on_button_motion(self, event) -> None:
        item = self.canvas.find_closest(event.x, event.y)[0]
        coords = min(self.points, key=lambda p: int(math.sqrt((p[0] - event.x) ** 2 + (p[1] - event.y) ** 2)))
        # coords = self.canvas.coords(item)[:2]
        # Перемещаем объект на новые координаты
        p_index = self.points.index(coords)
        self.canvas.move(item, event.x - coords[0], event.y - coords[1])
        self.points[p_index] = [event.x, event.y]
        self.draw_lines()

    def clear_points(self) -> None:
        """ Удаляет все точки """
        self.points = []
        self.canvas.delete("all")
        self.draw_lines()
        self.buttons_state(DISABLED)

    def clear_point(self) -> None:
        """ Удаляет 1 точку """
        del self.points[-1]
        self.canvas.delete("all")
        self.draw_lines()
        if not self.points:
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
        print(self.graphPaths)
# endregion
