from ga.myga import myga
import random
from operator import attrgetter
from entity.MA import MA
from entity import CONSTANT
from entity.Rule import Rule


class myga4train(myga):

    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):

        myga.__init__(self,
                      seed_data=seed_data,
                      population_size=population_size,
                      generations=generations,
                      crossover_probability=crossover_probability,
                      mutation_probability=mutation_probability,
                      elitism=elitism,
                      maximise_fitness=maximise_fitness)

        self.seed_data = seed_data
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness

        self.current_generation = []


        self.fitness_function = None
