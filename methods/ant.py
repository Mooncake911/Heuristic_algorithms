import numpy as np


class Ant:
    def __init__(self, size_pop, numberGeneration, graphPaths, alpha, beta, rho):
        """ Класс реализующий муравьиный алгоритм """
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(self.graphPaths) + 1  # количество вершин
        self.size_pop = size_pop  # популяция муравьёв
        self.numberGeneration = numberGeneration  # количество итераций
        self.alpha = alpha  # коэффициент важности феромонов при выборе пути
        self.beta = beta  # коэффициент значимости расстояния
        self.rho = rho  # скорость испарения феромонов

        # Нормализованное расстояние
        self.prob_matrix_distance = [list(map(lambda x: 1/x, sublist)) for sublist in self.graphPaths]
        # Матрица феромонов, обновляющаяся каждую итерацию
        self.Tau = [list(map(lambda x: 1, sublist)) for sublist in self.graphPaths]

        self.generation_best_path, self.generation_best_score = [], []  # лучшие в своём поколении
        self.best_path, self.best_score = None, None

    def distance(self, path) -> int:
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
        for _ in range(self.numberGeneration):
            # Путь каждого муравья в определённом поколении
            TablePath = np.zeros((self.size_pop, self.vertexes)).astype(int)
            # вероятность перехода без нормализации
            a_alfa = [[x ** self.alpha for x in sublist] for sublist in self.Tau]
            b_beta = [[x ** self.beta for x in sublist] for sublist in self.prob_matrix_distance]
            prob_matrix = [[float(x) * float(y) for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a_alfa, b_beta)]
            for ant in range(self.size_pop):  # для каждого муравья
                TablePath[ant, 0] = 0
                for v in range(self.vertexes - 1):  # каждая вершина, которую проходят муравьи
                    # точка, которая была пройдена и не может быть пройдена повторно
                    allow_list = list(set(range(self.vertexes)) - set(TablePath[ant, :v + 1]))
                    prob = []
                    for i in allow_list:
                        from_ = min(TablePath[ant, v], i)
                        to_ = max(TablePath[ant, v], i) - from_ - 1
                        prob.append(prob_matrix[from_][to_])
                    prob = [p / sum(prob) for p in prob]  # нормализация вероятности
                    next_point = np.random.choice(allow_list, size=1, p=prob)[0]
                    TablePath[ant, v + 1] = next_point

            # рассечёт расстояния
            scores = np.array([self.distance(list(path)) for path in TablePath])
            # фиксация лучшего решения
            index_best = scores.argmin()
            self.generation_best_path.append(TablePath[index_best, :])
            self.generation_best_score.append(scores[index_best])

            # мутация феромона, который будет добавлен к ребрам нового поколения
            self.Tau = [list(map(lambda x: (1 - self.rho) * x, sublist)) for sublist in self.Tau]
            for ant in range(self.size_pop):  # для каждого муравья
                for v in range(self.vertexes - 1):  # для каждой вершины
                    # муравьи перебираются из вершины from_ в вершину to_
                    from_ = min(TablePath[ant, v], TablePath[ant, v+1])
                    to_ = max(TablePath[ant, v], TablePath[ant, v+1]) - from_ - 1
                    self.Tau[from_][to_] += 1 / scores[ant]  # нанесение феромона
                # муравьи ползут от последней вершины обратно к первой
                from_ = min(TablePath[ant, self.vertexes - 1], TablePath[ant, 0])
                to_ = max(TablePath[ant, self.vertexes - 1], TablePath[ant, 0]) - from_ - 1
                self.Tau[from_][to_] += 1 / scores[ant]

        best_generation = np.array(self.generation_best_score).argmin()
        self.best_path = self.generation_best_path[best_generation].tolist()
        self.best_path.append(self.best_path[0])
        self.best_score = self.generation_best_score[best_generation]


def ant_algorithm(size_pop, numberGeneration, alpha, beta, rho, graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = Ant(size_pop=int(size_pop),
                numberGeneration=int(numberGeneration),
                alpha=int(alpha), beta=int(beta), rho=float(rho),
                graphPaths=graphPaths)
        a.find_best_way()
        return a.best_path, a.best_score


"""
# Проверка муравьиного алгоритма
print(ant_algorithm(10, 20, 1, 2, 0.1, [[226, 282, 117], [133, 219], [213]]))
"""
