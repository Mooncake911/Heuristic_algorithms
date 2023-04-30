from template import EditableSpinbox, WidgetTemp


def Annealing_Window(frame_annealing):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_annealing, main_title="SIMULATED ANNEALING ALGORITHM", img_title="Граф",
                       table_title="Таблица рёбер", algorithm="annealing_algorithm")

    # ~Создам атрибуты ввода
    EditableSpinbox(text="Введите начальную температуру:", initial_value="10", check_index=0,
                    from_=2, to=999, increment=1, frame=WTemp.frame_input, name='start_T').pack()
    EditableSpinbox(text="Введите конечную температуру:", initial_value="1", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='stop_T').pack()
    EditableSpinbox(text="Введите коэффициент охлаждения:", initial_value="0.7", check_index=2,
                    from_=0.1, to=1, increment=1, frame=WTemp.frame_input, name='coolingRatio').pack()
    EditableSpinbox(text="Введите количество поколений:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='numberGeneration').pack()

    WTemp.pack(padx=5, pady=5)
