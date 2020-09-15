from math import exp



class Node:

    def __init__(self, number):
        self.number = number
        self.input_sum = 0
        self.output_value = 0
        self.output_connections = []
        self.layer = 0

    def engage(self):
        if layer != 0: self.output_value = self.sigmoid(self.input_sum)

        for connection in self.output_connections:
            if connection.enabled: connection.to_node.input_sum += connection.weight * self.output_value

    def sigmoid(self, x):
        return 1 / (1 + exp(-4.9 * x))

    def is_connected_to(self, node):
        if node.layer == self.layer: return False

        if node.layer < self.layer:
            for connection in node.output_connections:
                if connection.to_node == self: return True
        else:
            for connection in self.output_connections:
                if connection.to_node == node: return True

    def clone(self):
        clone = Node(self.number)
        clone.layer = self.layer
        return clone
