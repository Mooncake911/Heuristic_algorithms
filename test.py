# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#
#     def __lt__(self, other):
#         if self.x == other.x:
#             return self.y < other.y  # сортировка по y в порядке возрастания
#         return self.x < other.x  # сортировка по x в порядке возрастания
#
#     def __hash__(self):
#         return hash((self.x, self.y))
#
#     def __repr__(self):
#         return "({}, {})".format(self.x, self.y)
#
#
# points_set = {Point(3, 2), Point(1, 5), Point(3, 1), Point(2, 2), Point(1, 1)}
# sorted_points = sorted(points_set)
# print(points_set.__repr__())
