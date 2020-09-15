from random import random, gauss


def constrain(x, b1, b2):
    return min(b2, max(b1, x))


class ConnectionGene:

    def __init__(self, from_node, to_node, w, inno):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = w
        self.innovation_no = inno
        self.enabled = True

    def mutate_weight(self):
        rand2 = random()
        if rand2 < 0.1:
            self.weight = 2*random()-1
        else:
            self.weight += constrain(gauss(0, 1) / 50, -1, 1)

    def clone(self, from_node, to_node):
        clone = ConnectionGene(from_node, to_node, self.weight, self.innovation_no)
        clone.enabled = self.enabled
        return clone
