from ga.myga import myga
from pyeasyga import pyeasyga


class myga4trade(myga):


    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):
        myga.__init__(self, seed_data,
                               population_size=population_size,
                               generations=generations,
                               crossover_probability=crossover_probability,
                               mutation_probability=mutation_probability,
                               elitism=elitism,
                               maximise_fitness=maximise_fitness)

    def create_initial_population(self):

        indvs = self.seed_data[2]

        initial_population = []
        for indv in indvs:
            initial_population.append(pyeasyga.Chromosome(indv))

        while len(initial_population) < self.population_size:
            genes = self.create_individual(self.seed_data)
            individual = pyeasyga.Chromosome(genes)
            initial_population.append(individual)

        self.current_generation = initial_population
