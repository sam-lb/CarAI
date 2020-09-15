from Node import Node
from ConnectionGene import ConnectionGene
from ConnectionHistory import ConnectionHistory
from math import floor
from random import random


class Genome:

    def __init__(self, inputs, outputs, crossover=False):
        self.inputs, self.outputs = inputs, outputs
        self.genes = []
        self.nodes = []
        self.network = []
        self.layers = 0
        self.next_node = inputs + outputs + 1

        if not crossover:
            for i in range(self.next_node - 1):
                n = Node(i)
                self.nodes.append(n)
                n.layer = int(i > inputs)

            self.nodes.append(Node(next_node))
            self.bias_node = next_node
            self.next_node += 1
            self.nodes[bias_node].layer = 0

    def get_node(self, node_number):
        for node in self.nodes:
            if node.number == node_number: return node
        return None

    def connect_nodes(self):
        for node in self.nodes:
            node.output_connections.clear()

        for gene in self.genes:
            gene.from_node.output_connections.append(gene)

    def feed_forward(self, input_values):
        for i in range(self.inputs):
            self.nodes[i].output_value = input_values[i]

        for node in self.network:
            node.engage()

        outs = []
        for i in range(self.outputs):
            outs.append(self.nodes[inputs + i].output_value)

        for node in self.nodes:
            node.input_sum = 0

        return outs

    def generate_network(self):
        self.connect_nodes()
        self.network = []

        for l in range(self.layers):
            for node in self.nodes:
                if node.layer == l: self.network.add(node)

    def add_node(self, innovation_history):
        if len(self.genes) == 0:
            self.add_connection(innovation_history)
            return
        random_connection = floor(random() * len(self.genes))

        while self.genes[random_connection].from_node == self.nodes[self.bias_node] and len(genes) != 1:
            randomConnection = floor(random() * len(self.genes))
        self.genes[random_connection].enabled = False

        new_node_no = self.next_node
        self.nodes.add(Node(new_node_no))
        self.next_node += 1
        connection_innovation_number = self.get_innovation_number(innovation_history, self.genes[random_connection].from_node, self.get_node(new_node_no))
        self.genes.append(ConnectionGene(self.genes[random_connection].from_node, self.get_node(new_node_no), connection_innovation_number))

        connection_innovation_number = self.get_innovation_number(innovation_history, self.get_node(new_node_no), self.genes.get(random_connection).to_node)
        self.genes.append(ConnectionGene(self.get_node(new_node_no), self.genes[random_connection].to_node, self.genes[random_connection].weight, connection_innovation_number))
        self.get_node(new_node_no).layer = genes[random_connection].from_node.layer + 1

        connection_innovation_number = self.get_innovation_number(innovation_history, self.nodes[self.bias_node], self.get_node(new_node_no))
        self.genes.append(ConnectionGene(self.nodes[self.bias_node], self.get_node(new_node_no), 0, connection_innovation_number))

        if self.get_node(new_node_no).layer == self.genes[random_connection].to_node.layer:
            for node in self.nodes[:-1]:
                if node.layer >= self.get_node(new_node_no).layer: node.layer += 1
            self.layers += 1
        self.connect_nodes()

    def add_connection(self, innovation_history):
        if self.fully_connected():
            print("connection failed")
            return

        random_node_1 = floor(random() * len(self.nodes))
        random_node_2 = floor(random() * len(self.nodes))
        while self.random_connection_nodes_invalid(random_node_1, random_node_2):
            random_node_1 = floor(random() * len(self.nodes))
            random_node_2 = floor(random() * len(self.nodes))
            
        if self.nodes[random_node_1].layer > self.nodes[random_node_2].layer:
            random_node_1, random_node_2 = random_node_2, random_node_1

        connection_innovation_number = self.get_innovation_number(innovation_history, self.nodes[random_node_1], self.nodes[random_node_2])
        self.genes.append(ConnectionGene(self.nodes[random_node_1], self.nodes[random_node_2], 2*random()-1, connection_innovation_number))
        self.connect_nodes()

    def random_connection_nodes_invalid(self, r1, r2):
        if self.nodes[r1].layer == self.nodes[r2].layer: return True
        if self.nodes[r1].is_connected_to(self.nodes[r2]): return True
        return False

    def get_innovation_number(self, innovation_history, from_node, to_node):
        is_new = True
        connection_innovation_number = self.next_connection_no
        for mutation in innovation_history:
            if mutation.matches(this, from_node, to_node):
                is_new = False
                connection_innovation_number = mutation.innovation_number
                break

        if is_new:
            inno_numbers = []
            for gene in self.genes:
                inno_numbers.append(gene.innovation_no)

            innovation_history.append(ConnectionHistory(from_node.number, to_node.number, connection_innovation_number, inno_numbers))
            self.next_connection_number += 1
        return connection_innovation_number

    def fully_connected(self):
        max_connections = 0
        nodes_in_layers = [node.layer for node in self.nodes]

        for i in range(layers-1):
            nodes_in_front = 0
            for j in range(i + 1, layers):
                nodes_in_front += nodes_in_layers[j]
            max_connections += nodes_in_layers[i] * nodes_in_front

        return max_connections == len(self.genes)

    def mutate(self, innovation_history):
        if len(self.genes) == 0: self.add_connection(innovation_history)

        if random() < 0.8:
            for gene in self.genes:
                gene.mutate_weight()
        if random() < 0.08: self.add_connection(innovation_history)
        if random() < 0.02: self.add_node(self.innovation_history)

    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)
        child.genes.clear()
        child.nodes.clear()
        child.layers = self.layers
        child.next_node = self.next_node
        child.bias_node = self.bias_node
        child_genes = []
        is_enabled = []

        for gene in self.genes:
            set_enabled = True

            parent2gene = self.matching_gene(parent2, gene.innovation_no)
            if parent2gene != -1:
                if (not gene.enabled) or (not parent2.genes[parent2gene].enabled):
                    if random() < 0.75: set_enabled = False
            if random() < 0.5:
                child_genes.append(gene)
            else:
                child_genes.append(gene)
                set_enabled = gene.enabled
            is_enabled.add(set_enabled)

        for node in self.nodes:
            child.nodes.append(node.clone())

        for i, cgene in enumerate(child_genes):
            child.genes.append(cgene.clone(cgene.from_node.number), child.get_node(cgene.to_node.number))
            cgene.enabled = is_enabled[i]

        child.connect_nodes()
        return child

    def matching_gene(self, parent2, innovation_number):
        for i, gene in enumerate(parent2.genes):
            if gene.innovation_no == innovation_number: return i
        return -1

    def clone(self):
        clone = Genome(self.inputs, self.outputs, True)
        for node in self.nodes:
            clone.nodes.append(node.clone())

        for gene in genes:
            clone.genes.append(gene.clone(clone.get_node(gene.from_node.number), clone.get_node(gene.to_node.number)))
        clone.layers = self.layers
        clone.next_node = next_node
        clone.bias_node = bias_node
        clone.connect_nodes()

        return clone
