from template import EditableSpinbox, EditableCombobox, WidgetTemp


def Swarm_Window(frame_swarm):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_swarm, main_title="SWARM ALGORITHM", img_title="Изображение",
                       table_title="Таблица поколений", algorithm="swarm_algorithm")

    # ~Ввод целочисленных данных
    EditableSpinbox(text="Введите количество особей для роя:", initial_value="10", check_index=0,
                    from_=2, to=999, increment=1, frame=WTemp.frame_input, name='sizeSwarm').pack()
    EditableSpinbox(text="Введите количество поколений:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='numberGeneration').pack()
    EditableSpinbox(text="Введите общий масштабирующий коэффициент для скорости:", initial_value="1", check_index=2,
                    from_=0.01, to=1.0, increment=0.01, frame=WTemp.frame_input, name='currentVelocityRatio').pack()
    EditableSpinbox(text="Введите коэффициент влияния лучшей точки особи на скорость:",
                    initial_value="1", check_index=2,
                    from_=0.01, to=1.0, increment=0.01, frame=WTemp.frame_input, name='localVelocityRatio').pack()
    EditableSpinbox(text="Введите коэффициент влияния лучшей точки по всем особям на скорость:",
                    initial_value="5", check_index=0,
                    from_=0.01, to=1.0, increment=0.01, frame=WTemp.frame_input, name='globalVelocityRatio').pack()
    EditableSpinbox(text="Введите начало диапазона поиска:", initial_value="-5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='start').pack()
    EditableSpinbox(text="Введите конец диапазона поиска:", initial_value="5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='end').pack()
    # ~Ввод выдвигающегося списка
    EditableCombobox(WTemp.frame_input, text="Выберете какую функцию хотите исследовать:", name='func').pack()

    WTemp.pack(padx=5, pady=5)
