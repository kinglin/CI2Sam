from ga.myga import myga
from pyeasyga import pyeasyga


class myga4selection(myga):

    def create_initial_population(self):

        initial_population = []
        # for _ in range(self.population_size):
        #     genes = self.create_individual(self.seed_data)
        #     individual = pyeasyga.Chromosome(genes)
        #     initial_population.append(individual)
        self.current_generation = initial_population