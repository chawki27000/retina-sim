import random


class Unifast:
    def __init__(self, nb_task, nb_set, u):
        self.nb_task = nb_task
        self.nb_set = nb_set
        self.u = u

    def UUniFastDiscard(self):
        sets = []
        while len(sets) < self.nb_set:
            # Classic UUniFast algorithm:
            utilizations = []
            sumU = self.u
            for i in range(1, self.nb_task):
                nextSumU = sumU * random.random() ** (1.0 / (self.nb_task - i))
                utilizations.append(sumU - nextSumU)
                sumU = nextSumU
            utilizations.append(sumU)

            # If no task utilization exceeds 1:
            if all(ut <= 1 for ut in utilizations):
                sets.append(utilizations)

        return sets[0]
