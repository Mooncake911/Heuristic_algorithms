from math import *
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import random
import os


class Unit:
    """ Класс ::Пчела """
    def __init__(self, start, end, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, function):
        # область поиска
        self.start = start
        self.end = end
        # коэффициенты для изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # целевая функция
        self.function = function
        # текущая позиция (первый раз определяется случайно на заданном диапазоне)
        self.currentPos = [random.uniform(self.start, self.end), random.uniform(self.start, self.end)]
        self.score = self.function(*self.currentPos)
        # лучшая локальная позиция
        self.localBestPos = self.currentPos[:]
        self.localBestScore = self.score
        # значение глобальной позиции
        self.globalBestPos = []
        # скорость (первый раз задаётся случайно на диапазоне)
        search_range = abs(self.end - self.start)
        self.velocity = [random.uniform(-search_range, search_range), random.uniform(-search_range, search_range)]

    def nextIteration(self) -> None:
        """ Метод для нахождения новой позиции частицы"""
        # случайные данные для изменения скорости
        rndCurrentBestPosition = [random.random(), random.random()]
        rndGlobalBestPosition = [random.random(), random.random()]
        # делаем перерасчет скорости частицы исходя из всех введенных параметров
        velocityRatio = self.localVelocityRatio + self.globalVelocityRatio
        commonVelocityRatio = 2 * self.currentVelocityRatio / abs(
            2 - velocityRatio - sqrt(abs(velocityRatio ** 2 - 4 * velocityRatio)))

        # изменяем x и y
        multLocal = list(map(lambda x: x * commonVelocityRatio * self.localVelocityRatio, rndCurrentBestPosition))
        multGlobal = list(map(lambda x: x * commonVelocityRatio * self.globalVelocityRatio, rndGlobalBestPosition))

        betweenLocalAndCurPos = [self.localBestPos[0] - self.currentPos[0], self.localBestPos[1] - self.currentPos[1]]
        betweenGlobalAndCurPos = [self.globalBestPos[0] - self.currentPos[0],
                                  self.globalBestPos[1] - self.currentPos[1]]

        newVelocity1 = list(map(lambda x: x * commonVelocityRatio, self.velocity))
        newVelocity2 = [coord1 * coord2 for coord1, coord2 in zip(multLocal, betweenLocalAndCurPos)]
        newVelocity3 = [coord1 * coord2 for coord1, coord2 in zip(multGlobal, betweenGlobalAndCurPos)]
        self.velocity = [coord1 + coord2 + coord3 for coord1, coord2, coord3 in
                         zip(newVelocity1, newVelocity2, newVelocity3)]

        # передвигаем частицу и смотрим, какое значение целевой функции получается
        self.currentPos = [coord1 + coord2 for coord1, coord2 in zip(self.currentPos, self.velocity)]
        self.score = self.function(*self.currentPos)
        if self.score < self.localBestScore:
            self.localBestPos = self.currentPos[:]
            self.localBestScore = self.score


class Swarm:
    """ Класс реализующий метод роя """
    def __init__(self,
                 sizeSwarm,  # размер роя (количество особей)
                 currentVelocityRatio,  # общий масштабирующий коэффициент для скорости
                 localVelocityRatio,  # коэффициент, задающий влияние лучшей точки особи
                 globalVelocityRatio,  # коэффициент, задающий влияние лучшей точки, найденной всеми особями
                 numberGeneration,  # количество поколений алгоритма (критерий остановки)
                 function,  # функция для поиска экстремума
                 start, end):  # область поиска

        self.sizeSwarm = sizeSwarm
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        self.numberGeneration = numberGeneration
        self.function = function
        self.start = start
        self.end = end

        # данные о лучшей позиции
        self.globalBestPos = []
        self.globalBestScore = float('inf')
        # рой частиц
        self.swarm = []
        self.createSwarm()
        # Создаём дата-фрейм в который запишем результаты
        self.data = pd.DataFrame()

    def createSwarm(self) -> None:
        """ Метод для создания роя, вызывается 1 раз в начале"""
        pack = [self.start, self.end, self.currentVelocityRatio, self.localVelocityRatio, self.globalVelocityRatio,
                self.function]
        self.swarm = [Unit(*pack) for _ in range(self.sizeSwarm)]
        # выбираем лучшее значение для только что созданного роя
        for unit in self.swarm:
            if unit.localBestScore < self.globalBestScore:
                self.globalBestScore = unit.localBestScore
                self.globalBestPos = unit.localBestPos

    def startSwarm(self) -> None:
        """ Метод для запуска алгоритма"""
        dataForGIF = []
        dataForTable = []
        for _ in range(self.numberGeneration):
            oneDataX = []
            oneDataY = []
            for unit in self.swarm:
                oneDataX.append(unit.currentPos[0])
                oneDataY.append(unit.currentPos[1])
                unit.globalBestPos = self.globalBestPos
                unit.nextIteration()
                if unit.score < self.globalBestScore:
                    self.globalBestScore = unit.score
                    self.globalBestPos = unit.localBestPos
                # Записываем в таблицу лучшие данные
                dataForTable.append([self.globalBestPos[0], self.globalBestPos[1], self.globalBestScore])
            dataForGIF.append([oneDataX, oneDataY])

        # Сохраняем, рисуем gif
        snapshot_arr = []
        i = 0
        for x, y in dataForGIF:
            i += 1
            snapshot_name = f"s/s{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Поколение: {i}")
            fig.patch.set_facecolor("#B3E5FC")
            ax2.set_xlabel("initial field")
            ax2.plot(x, y, 'bo')
            ax2.set_xlim(min(x) - 2, max(x) + 2)
            ax2.set_ylim(min(y) - 2, max(y) + 2)
            ax1.set_xlabel("dynamic field")
            ax1.plot(x, y, 'bo')
            plt.savefig(snapshot_name, dpi=70, bbox_inches='tight')
            plt.close()
            snapshot_arr.append(snapshot_name)

        with imageio.get_writer('s/swarm.gif', mode='I') as writer:
            for filename in snapshot_arr:
                image = imageio.v2.imread(filename)
                writer.append_data(image)

        # Сохраняем таблицу
        self.data = pd.DataFrame(dataForTable)
        self.data.columns = ['X', 'Y', 'BestScore_F(x,y)']


def swarm_algorithm(sizeSwarm, numberGeneration, currentVelocityRatio, localVelocityRatio, globalVelocityRatio,
                    start, end, function) -> [[float, float], float, pd.DataFrame]:
    if not os.path.isdir('s'):
        os.mkdir('s')
    a = Swarm(sizeSwarm=int(sizeSwarm),
              numberGeneration=int(numberGeneration),
              currentVelocityRatio=float(currentVelocityRatio),
              localVelocityRatio=float(localVelocityRatio),
              globalVelocityRatio=float(globalVelocityRatio),
              function=function,
              start=min(int(start), int(end)),
              end=max(int(start), int(end)))
    a.startSwarm()
    return a.globalBestPos, a.globalBestScore, a.data
