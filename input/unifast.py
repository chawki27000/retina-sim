import time
import random
import math


class Unifast:
    def __init__(self, nb_task, nb_proc, u):
        self.nb_task = nb_task
        self.nb_proc = nb_proc
        self.u = u

    def generate_utilization(self):
        util = []
        discard = True

        while discard or not self.utilization_is_valid(util):
            sumU = self.u
            discard = False

            for i in range(self.nb_task - 1):
                rndm = random.randint(int(round(time.time() * 1000)))
                nextSumU = sumU * math.pow(rndm, 1 / (self.nb_task - (i + 1)))
                util.append(sumU - nextSumU)
                sumU = nextSumU

            util[self.nb_task - 1] = sumU
            if util[self.nb_task - 1] > 1:
                discard = True

        return util

    def utilization_is_valid(self, util):
        sum = 0
        for u in util:
            sum += u

        return sum <= self.nb_proc
