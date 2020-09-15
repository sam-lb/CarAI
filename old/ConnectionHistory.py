
class ConnectionHistory:

    def __init__(self, from_node, to_node, inno, innovation_nos):
        self.from_node = from_node
        self.to_node = to_node
        self.innovation_number = inno
        self.innovation_numbers = innovation_nos[:]

    def matches(self, genome, from_node, to_node):
        if len(genome.genes) == len(self.innovation_numbers):
            if from_node.number == self.from_node and to_node.number == self.to_node:
                for gene in genome.genes:
                    if not (gene.innovation_no in self.innovation_numbers):
                        return False
                return True
        return False
