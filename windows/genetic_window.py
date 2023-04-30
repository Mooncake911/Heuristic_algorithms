from template import EditableSpinbox, EditableCombobox, WidgetTemp


def Genetic_Window(frame_genetic):
    # Создание скелета окна
    WTemp = WidgetTemp(root=frame_genetic, main_title="GENETIC ALGORITHM", img_title="Изображение",
                       table_title="Таблица поколений", algorithm="genetic_algorithm")

    # ~Ввод целочисленных данных
    EditableSpinbox(text="Введите размер популяции для одного поколения поколении:", initial_value="10", check_index=0,
                    from_=2, to=999, increment=1, frame=WTemp.frame_input, name='numberOfIndividuals').pack()
    EditableSpinbox(text="Введите количество поколений:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='numberGeneration').pack()
    EditableSpinbox(text="Введите количество итераций для мутации:", initial_value="10", check_index=0,
                    from_=1, to=999, increment=1, frame=WTemp.frame_input, name='mutationSteps').pack()
    # ~Ввод данных с точкой
    EditableSpinbox(text="Какая доля популяции должна производить потомство:", initial_value="0.5", check_index=2,
                    from_=0.01, to=1, increment=0.01, frame=WTemp.frame_input, name='crossoverRate').pack()
    EditableSpinbox(text="Введите шанс индивида мутировать:", initial_value="0.5", check_index=2,
                    from_=0.01, to=1, increment=0.01, frame=WTemp.frame_input, name='chanceMutations').pack()
    EditableSpinbox(text="Введите начало диапазона поиска:", initial_value="-5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='start').pack()
    EditableSpinbox(text="Введите конец диапазона поиска:", initial_value="5", check_index=1,
                    from_=-99999, to=99999, increment=1, frame=WTemp.frame_input, name='end').pack()
    # ~Ввод выдвигающегося списка
    EditableCombobox(WTemp.frame_input, text="Выберете какую функцию хотите исследовать:", name='func').pack()

    WTemp.pack(padx=5, pady=5)
