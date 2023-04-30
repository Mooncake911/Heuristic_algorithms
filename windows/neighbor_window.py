from template import WidgetTemp


def Neighbor_Window(frame_neighbor):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_neighbor, main_title="NEAREST NEIGHBOR ALGORITHM", img_title="Граф",
                       table_title="Таблица рёбер", algorithm="neighborhood_algorithm")
    WTemp.pack(padx=5, pady=5)
