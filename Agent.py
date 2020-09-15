import pygame
import numpy as np
from NeuralBrain import NeuralBrain
from helpers import rotate_in_place, pointlist_midpoint, random_color, sigmoid, constrain
from math import sin, cos, pi



class Agent:

    """ Navigating AI agent """

    def __init__(self, id_, x, y, size=25, decision_threshold=0.5, generate=True):
        self.id = id_
        self.original = x, y
        self.x, self.y = x, y
        self.angle = 0
        self.speed = 1/100
        self.half_size = size / 2
        self.angular_speed = 0.02
        self.dcolor = random_color()
        self.dcolor = (255, self.dcolor[1], self.dcolor[2])
        self.decision_threshold = decision_threshold

        if generate: self.brain = NeuralBrain(self.get_inputs, 3, 2)

    def get_inputs(self):
        """ get the inputs to the agent's brain """
        return np.array([2*self.x-1, 2*self.y-1, (self.angle-pi)/pi])

    def generate_child(self, species, agent, mutation_chance=1/20, mutation_mag=0.2):
        """ Combine with another agent, produce another one for the next generation """
        new_agent = Agent(species.next_id(), self.original[0], self.original[1], self.half_size*2, self.decision_threshold)
        new_agent.brain = NeuralBrain.from_agent_and_layers(self.brain, new_agent,
                                                            self.brain.generate_child_layers(agent.brain, mutation_chance, mutation_mag))
        return new_agent

    def drive(self):
        self.x = constrain(self.x + self.speed * cos(self.angle), 0, 1)
        self.y = constrain(self.y + self.speed * sin(self.angle), 0, 1)

    def rotate_ccw(self):
        self.angle += self.angular_speed

    def rotate_cw(self):
        self.angle -= self.angular_speed

    def draw(self, surface):
        """ Draw the agent to the pygame.Surface surface """
        pygame.draw.polygon(surface, self.dcolor, self.vertices)
        pygame.draw.polygon(surface, (0, 0, 0), self.vertices, 1)
        pygame.draw.polygon(surface, (0, 0, 0), [self.midpoint, self.vertices[2], self.vertices[3]])

    def move(self):
        """ Make the moves the agent's brain thinks is best """
        outputs = self.brain.think()
        #print(outputs)
        if outputs[0] > self.decision_threshold: self.drive()
        if outputs[1] > self.decision_threshold: self.rotate_ccw()
        if outputs[2] > self.decision_threshold: self.rotate_cw()

    def update(self, surface):
        x, y = self.x * surface.get_width(), self.y * surface.get_height()
        self.vertices = rotate_in_place([
            (x - self.half_size, y - self.half_size),
            (x - self.half_size, y + self.half_size),
            (x + self.half_size, y + self.half_size),
            (x + self.half_size, y - self.half_size)
        ], self.angle);
        self.midpoint = pointlist_midpoint(self.vertices)
        
        self.move()
        self.draw(surface)
