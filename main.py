from tkinter import *
from tkinter import ttk
from windows import *
from template import stop_event
import gc


def on_exit():
    """ Функция, которая завершает threading """
    stop_event.set()
    print("Bye!")
    root.destroy()
    return 0


# Создаётся окно пользователя
root = Tk()
root.title("ALGORITHMS")
root.geometry('1050x670')
root.protocol('WM_DELETE_WINDOW', on_exit)

# Зададим слить для вкладок
style = ttk.Style()
style.theme_use('vista')
style.configure('TNotebook', background='white')
style.configure('TNotebook.Tab', foreground='red',  background="gray")
style.map('TNotebook.Tab', foreground=[('selected', 'green')], background=[('selected', "#B3E5FC")])

# Вкладки
ntb = ttk.Notebook(root, style='TNotebook')
ntb.pack(fill='both', expand=True)

# Генетический алгоритм
frame_genetic = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_genetic, text="Генетический алгоритм")
Genetic_Window(frame_genetic)
# Роевой алгоритм
frame_swarm = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_swarm, text="Алгоритм роя частиц")
Swarm_Window(frame_swarm)
# Метод отжига
frame_annealing = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_annealing, text="Метод отжига")
Annealing_Window(frame_annealing)
# Метод ближайшего соседа
frame_neighbor = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_neighbor, text="Метод ближайшего соседа")
Neighbor_Window(frame_neighbor)
# Муравьиный алгоритм
frame_ant = Frame(ntb, bg="#B3E5FC")
ntb.add(frame_ant, text="Муравьиный алгоритм")
Ant_Window(frame_ant)

root.mainloop()
