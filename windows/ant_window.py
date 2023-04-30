from template import EditableSpinbox, WidgetTemp


def Ant_Window(frame_ant):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_ant, main_title="ANT COLONY OPTIMIZATION", img_title="Граф",
                       table_title="Таблица рёбер", algorithm="ant_algorithm")

    # ~Создам атрибуты ввода
    EditableSpinbox(text="Введите размер популяции для одного поколения поколении:", initial_value="10", check_index=0,
                    from_=2, to=999, increment=1, frame=WTemp.frame_input, name='size_pop').pack()
    EditableSpinbox(text="Введите количество поколений:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='numberGeneration').pack()
    EditableSpinbox(text="Введите коэффициент важности феромонов:", initial_value="1", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='alpha').pack()
    EditableSpinbox(text="Введите коэффициент значимости расстояния:", initial_value="1", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='beta').pack()
    EditableSpinbox(text="Введите скорость испарения феромонов:", initial_value="0.1", check_index=2,
                    from_=0.01, to=1.00, increment=1, frame=WTemp.frame_input, name='rho').pack()

    WTemp.pack(padx=5, pady=5)
