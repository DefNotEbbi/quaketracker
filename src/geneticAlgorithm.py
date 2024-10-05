# Author: Ebrahim Muneer
# Genetic Algorithm to choose optimum parameters for sta/lta

import random
from obspy import read
import numpy as np
from readWrite import getCatalogTimes
from detectionAlgorithms import recursiveStaLtaMax
import time

class GeneticAlgorithm:

    # Initialize common properties
    def __init__(self, population_size, mutation_rate, num_generations, filenames, catalog, dataDirectory):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.filenames = filenames
        self.catalog = catalog
        self.dataDir = dataDirectory
        self.bestIndividual = None
        self.lowestError = 100
        self.population = self.initialize_population()

    # Bunch individuals into a population
    def initialize_population(self):
        population = []
        for i in range(self.population_size):
            individual = self.create_individual()
            population.append(individual)
        return population

    # Create an individual with random parameters
    def create_individual(self):
        short_window = 114.3457 + random.random() * 10
        long_window = 1772.2823 + random.random() * 10
        on_factor = 0.3188 + random.random() * 0.1
        return [short_window, long_window, on_factor]

    # Testing the fitness of an individual by running it through all the lunar testing files
    # Returns the error as a score
    def fitness(self, individual):
        bad_files = ['xa.s12.00.mhz.1971-10-31HR00_evid00045', 'xa.s12.00.mhz.1970-03-26HR00_evid00004', 'xa.s12.00.mhz.1974-06-25HR00_evid00149', 'xa.s12.00.mhz.1972-07-17HR00_evid00067', 'xa.s12.00.mhz.1970-07-20HR00_evid00011', 'xa.s12.00.mhz.1972-07-17HR00_evid00068', 'xa.s12.00.mhz.1974-04-27HR00_evid00145', 'xa.s12.00.mhz.1970-04-25HR00_evid00006', 'xa.s12.00.mhz.1970-10-24HR00_evid00014', 'xa.s12.00.mhz.1973-07-04HR00_evid00114', 'xa.s12.00.mhz.1974-07-17HR00_evid00153', 'xa.s12.00.mhz.1971-06-12HR00_evid00035', 'xa.s12.00.mhz.1973-06-05HR00_evid00107', 'xa.s12.00.mhz.1974-07-06HR00_evid00151', 'xa.s12.00.mhz.1971-02-09HR00_evid00026', 'xa.s12.00.mhz.1970-07-20HR00_evid00010', 'xa.s12.00.mhz.1971-05-12HR00_evid00031', 'xa.s12.00.mhz.1970-11-12HR00_evid00015', 'xa.s12.00.mhz.1971-04-13HR02_evid00029']
        error_list = []
        for filename in self.filenames:
            if filename in bad_files:
                continue

            st = read(f"{self.dataDir}/{filename}")
            st.filter('bandpass', freqmin=0.90, freqmax=0.91)

            tr = st[0]
            tr_times = tr.times()
            tr_data = tr.data
            tr_samplingRate = tr.stats.sampling_rate

            catalogArrival = getCatalogTimes(self.catalog, filename.replace('.mseed', ''))
            predictedArrival, sta_lta, on_threshold = recursiveStaLtaMax(tr_times, tr_data, tr_samplingRate, short_window=individual[0], long_window=individual[1], on_factor=individual[2])

            if catalogArrival is not None and predictedArrival is not None:
                error = (abs(catalogArrival - predictedArrival) / np.max(tr_times)) * 100
                error_list.append(error)

        avgError = np.mean(error_list)

        if avgError < self.lowestError:
            self.lowestError = avgError
            print("\n NEW BEST INDIVIDUAL:")
        
        print(f"Error: {avgError:.4f}% Short Window: {individual[0]:.4f} Long Window: {individual[1]:.4f} On Factor: {individual[2]:.4f}")
        return -avgError

    # Select the top 40% of the population and returns them
    def selection(self):
        ranked_population = sorted(self.population, key=self.fitness, reverse=True)
        self.bestIndividual = ranked_population[0]
        selected_population = ranked_population[:int(self.population_size * 0.4)]
        return selected_population

    # Crossover the shortwindow property of the individuals to create new children
    def crossover(self, selected_population):
        new_population = []
        for i in range(len(selected_population)):
            for j in range(i+1, len(selected_population)):
                individual1 = selected_population[i]
                individual2 = selected_population[j]

                child1 = individual1[:]
                child2 = individual2[:]

                child1[0] = individual2[0]
                child2[0] = individual1[0]

                new_population.append(child1)
                new_population.append(child2)

        return new_population

    # Mutate all the properties of the individuals by either slightly incrementing or decrementing them
    def mutation(self, population):
        for individual in population:
            if random.random() < self.mutation_rate:
                for i in range(len(individual)):
                    if random.random() < 0.5:
                        individual[i] *= 1.1
                    else:
                        individual[i] *= 0.9

        return population
    
    # Update the terminal with the best individual and save their properties into a text file
    def update(self):
        with open('bestIndividual.txt', 'w') as f:
            f.write(str(self.bestIndividual))
            f.close()
        
        print(f"\nError: {self.lowestError:.4f}% Best Short: {self.bestIndividual[0]:.4f} Best Long: {self.bestIndividual[1]:.4f} Best OnFactor: {self.bestIndividual[2]:.4f}\n")
        time.sleep(1)

    # Main loop
    def run(self):
        for i in range(self.num_generations):
            selected_population = self.selection()
            self.update()
            new_population = self.crossover(selected_population)
            new_population = self.mutation(new_population)
            self.population = new_population
        return self.population