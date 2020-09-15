from Agent import Agent
from random import random


class Species:

    def __init__(self, num_agents=30):
        self.agents = []
        self.generation = 1
        self.num_agents = num_agents

        self.generate_agents()

    def generate_agents(self):
        for i in range(self.num_agents):
            self.add_agent(Agent(i, 0.5, 0.5))

    def next_generation(self, fitness_function, mutation_chance=1/20, mutation_mag=0.2):
        new_agents = self.select_pool(fitness_function)
        kept = len(new_agents)
        print(new_agents)
        
        for i in range(self.num_agents - kept):
            # generate children to fill in the gaps
            parent_agent_1 = new_agents[i%(kept-1)]
            parent_agent_2 = new_agents[i%(kept-1)+1]
            new_agents.append(parent_agent_1.generate_child(self, parent_agent_2, mutation_chance, mutation_mag))
        self.agents = new_agents
        self.generation += 1

    def add_agent(self, agent):
        self.agents.append(agent)

    def find_agent(self, id_):
        for agent in agents:
            if agent.id == id_: return agent

    def next_id(self):
        return max(self.agents, key=lambda a: a.id).id + 1

    def select_pool(self, fitness_function):
        """ Select the fittest agents that will produce the next generation """
        # find min and max fitness, then normalize them to a probability.
        # however many empty spaces there are after killing some agents is the number of
        # new children
        lower, upper = None, None
        for agent in self.agents:
            fitness = fitness_function(agent)
            if (lower is None) or (fitness < lower): lower = fitness
            if (upper is None) or (fitness > upper): upper = fitness
        v_range = upper - lower
        
        pool = []
        for agent in self.agents:
            if (v_range != 0) and (random() < ((fitness_function(agent) - lower) / v_range)):
                pool.append(agent)
        return pool

    def update(self, surface):
        for agent in self.agents:
            agent.update(surface)
