import math
import random
import copy


class SimulatedAnn:
    """ Класс реализующий метод отжига """
    def __init__(self, graphPaths, start_T, stop_T, coolingRatio, numberGeneration):
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(graphPaths) + 1  # кол-во вершин
        self.coolingRatio = coolingRatio  # коэффициент охлаждения
        self.start_T = start_T  # начальная температура
        self.stop_T = stop_T  # конечная температура
        self.numberGeneration = numberGeneration  # количество попыток отыскать новый маршрут
        # задаём начальные значения
        self.best_path = [x for x in range(self.vertexes)]
        random.shuffle(self.best_path)
        self.best_score = self.count_length(copy.deepcopy(self.best_path))

    def count_length(self, path) -> int:
        """ Находим длину пути """
        path.append(path[0])
        score = 0
        # Потом добавляем остальные маршруты
        for i in range(self.vertexes):
            from_ = min(path[i], path[i + 1])
            to_ = max(path[i], path[i + 1]) - from_ - 1
            score += self.graphPaths[from_][to_]
        return score

    def find_best_way(self) -> None:
        """ Находим лучший путь с наименьшей длиной """
        while self.start_T > self.stop_T:
            # Даём сделать несколько попыток найти лучшую траекторию без понижения температуры
            previous_path = copy.deepcopy(self.best_path)
            for _ in range(self.numberGeneration):
                # пробуем найти лучший путь меняя 2 позиции
                new_path = copy.deepcopy(previous_path)
                pos1 = random.randrange(self.vertexes)
                pos2 = random.randrange(self.vertexes)
                while pos1 == pos2:
                    pos2 = random.randrange(self.vertexes)
                new_path[pos1], new_path[pos2] = new_path[pos2], new_path[pos1]
                # находим длину нового пути
                new_path_score = self.count_length(copy.deepcopy(new_path))
                # считаем вероятность перейти к следующему шагу
                h = math.exp(-(new_path_score - self.best_score) / self.start_T)
                if random.random() < h:
                    self.best_path = new_path
                    self.best_score = new_path_score
            # понижаем вероятность перейти к следующему шагу
            self.start_T = self.start_T * self.coolingRatio
        self.best_path.append(self.best_path[0])


def annealing_algorithm(start_T, stop_T, coolingRatio, numberGeneration, graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = SimulatedAnn(numberGeneration=int(numberGeneration),
                         coolingRatio=float(coolingRatio),
                         start_T=max(int(start_T), int(stop_T)), stop_T=min(int(start_T), int(stop_T)),
                         graphPaths=graphPaths)
        a.find_best_way()
        return a.best_path, a.best_score


'''# Запускаем метод имитации отжига
print(annealing_algorithm(100, 1, 0.7, 10, [[226, 282, 117], [133, 219], [213]]))
'''