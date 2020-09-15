import numpy as np
from helpers import sigmoid


class NeuralBrain:

    """ Neural network and genetic algorithm hybrid """

    def __init__(self, inputs_func, num_inputs, num_layers=1, nodes_per_hl=3, num_output_nodes=3, generate=True):
        self.inputs_func = inputs_func
        self.num_inputs = num_inputs  # the number of values return by inputs_func
        self.num_layers = num_layers  # number of hidden layers
        self.nodes_per_hl = 3  # does not include biases
        self.num_output_nodes = num_output_nodes

        if generate: self.generate_layers()

    @classmethod
    def from_agent_and_layers(cls, brain, agent, layers):
        new_brain = cls(agent.get_inputs, brain.num_inputs, brain.num_layers, brain.nodes_per_hl, brain.num_output_nodes, False)
        new_brain.layers = layers
        return new_brain

    def generate_layers(self):
        """ Generate the hidden and output layers of the network """
        self.layers = []
        self.layers.append(Layer(self.nodes_per_hl, num_inputs=self.num_inputs))
        for i in range(1, self.num_layers+1):
            self.layers.append(Layer(self.nodes_per_hl, self.layers[i-1], is_output=i==self.num_layers))

    def think(self):
        """ Get the brain's prediction """
        return self.layers[-1].calculate_outputs(self.inputs_func())

    def generate_child_layers(self, brain, mutation_chance=1/20, mutation_mag=0.2):
        """ Cross over with another brain and mutate in order to produce another one """
        new_layers = []
        for i in range(len(self.layers)):
            new_layers.append(self.layers[i].crossover(brain.layers[i], mutation_chance, mutation_mag))
        return new_layers
    

class Layer:

    """ A layer of a neural network (hidden or output) """

    def __init__(self, num_nodes, input_layer=None, is_output=False, num_inputs=None, generate=True):
        self.num_nodes = num_nodes + 1 * (not is_output)  # to include bias
        self.input_layer = input_layer
        self.is_output = is_output
        self.num_inputs = num_inputs

        if generate: self.generate_weights()

    @classmethod
    def from_weights(cls, layer, weights):
        new_layer = cls(layer.num_nodes - 1 * (not layer.is_output), layer.input_layer, layer.is_output, layer.num_inputs, False)
        new_layer.weights = weights
        return new_layer

    def generate_weights(self):
        """ Generate the weights for each connection of each node in the layer """
        if self.input_layer is None:
            if self.num_inputs is None: raise Exception("First hidden layer must provide num_inputs")
            self.weights = np.random.rand(self.num_nodes, self.num_inputs)
        else:
            self.weights = np.random.rand(self.num_nodes, self.input_layer.num_nodes)

    def calculate_outputs(self, inputs):
        """ Calculate the outputs of this layer """
        if self.input_layer is None:
            return np.dot(self.weights, inputs)
        if self.is_output:
            return np.tanh(np.dot(self.weights, self.input_layer.calculate_outputs(inputs)))
        return sigmoid(np.dot(self.weights, self.input_layer.calculate_outputs(inputs)))

    def crossover(self, layer, mutation_chance=1/20, mutation_mag=0.2):
        """ cross over with another layer, mutate with chance mutation_chance, with maximum mutation mutation_mag """
        new_weights = np.zeros_like(self.weights)
        for i in range(new_weights.shape[0]):
            for j in range(new_weights.shape[1]):
                new_weights[i,j] = 0.5 * (self.weights[i,j] + layer.weights[i,j])
                if np.random.random() <= mutation_chance:
                    if np.random.random() <= 0.5:
                        new_weights[i,j] *= 1 + mutation_mag
                    else:
                        new_weights[i,j] *= 1 - mutation_mag
        return Layer.from_weights(self, new_weights)
