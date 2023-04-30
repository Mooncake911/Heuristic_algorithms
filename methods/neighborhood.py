class Neighbor:
    """ Метод ближайшего соседа """
    def __init__(self, graphPaths):
        self.graphPaths = graphPaths  # веса путей заданных в графе
        self.vertexes = len(graphPaths) + 1  # кол-во вершин
        self.best_path = []  # лучший маршрут
        self.best_score = float('inf')  # наименьшая длина цикла

    def find_best_way(self) -> None:
        # Начинаем обход по каждой вершине
        for i in range(self.vertexes):
            new_path = [i]
            new_score = 0
            while len(new_path) <= self.vertexes:
                min_rib = float('inf')
                next_top = i
                for j in range(self.vertexes):
                    if j not in new_path:
                        from_ = min(new_path[-1], j)
                        to_ = max(new_path[-1], j) - from_ - 1
                        rib = self.graphPaths[from_][to_]
                        if rib < min_rib:
                            min_rib = rib
                            next_top = j

                if min_rib < float('inf'):
                    new_score += min_rib
                else:
                    from_ = min(new_path[-1], next_top)
                    to_ = max(new_path[-1], next_top) - from_ - 1
                    new_score += self.graphPaths[from_][to_]
                new_path.append(next_top)

            if new_score < self.best_score:
                self.best_path = new_path
                self.best_score = new_score


def neighborhood_algorithm(graphPaths):
    if graphPaths == [] or graphPaths == [[]]:
        return [], None
    else:
        a = Neighbor(graphPaths=graphPaths)
        a.find_best_way()
        return a.best_path, a.best_score


""" Запускаем метод ближайшего соседа
print(neighborhood_algorithm([[226, 282, 117], [133, 219], [213]]))
"""
