import pygame, sys
from pygame.locals import *
import numpy as np
import random 

import time


MUTATION_RATE = 0.01

class Chromosome:
    def __init__(self, genes=None):
        self.genes = [random.randint(1, 8) for _ in range(63)] if genes is None else genes

    def crossover(self, partner):
        crossover_point = random.randint(0, len(self.genes) - 1)
        child_genes1 = self.genes[:crossover_point] + partner.genes[crossover_point:]
        child_genes2 = partner.genes[:crossover_point] + self.genes[crossover_point:]
        
        return Chromosome(child_genes1), Chromosome(child_genes2)

    def mutation(self):
        for i in range(len(self.genes)):
            if random.random() < MUTATION_RATE:
                self.genes[i] = random.randint(1, 8)


class Knight:
    def __init__(self, chromosome=None):
        self.position = (0, 0)
        self.chromosome = Chromosome() if chromosome is None else chromosome
        self.path = [self.position]
        self.fitness = 0

    def move_forward(self, direction):
        moves = [[1, -2], [2, -1], [2, 1], [1, 2],  [-1, 2], [-2, 1], [-2, -1],  [-1, -2]]
        x, y = self.path[-1]
        dx, dy = moves[direction - 1] 
        x, y = self.position
        new_position = (x + dx, y + dy)
        self.position = new_position

    def move_backward(self, direction):
        moves = [[1, -2], [2, -1], [2, 1], [1, 2],  [-1, 2], [-2, 1], [-2, -1],  [-1, -2]]
        x, y = self.path[-1]
        dx, dy = moves[direction - 1] 
        x, y = self.position
        new_position = (x - dx, y - dy)
        self.position = new_position

    def check_moves(self):
        step = random.choice([-1, 1])
        
        for direction in self.chromosome.genes:
            self.move_forward(direction)
            if self.is_valid_move(self.position, self.path):
                self.path.append(self.position)
            else:
                self.move_backward(direction)
                new_direction = direction % 8 + 1 if step == 1 else (direction - 2) % 8 + 1
                self.move_forward(new_direction)

                while not self.is_valid_move(self.position, self.path) and (new_direction != direction):
                    self.move_backward(new_direction)
                    new_direction = new_direction % 8 + 1 if step == 1 else (new_direction - 2) % 8 + 1
                    self.move_forward(new_direction)

                self.path.append(self.position)

    def is_valid_move(self, position, path):
        x, y = position
        return 0 <= x < 8 and 0 <= y < 8 and position not in path

    def evaluate_fitness(self):
        path = []
        for position in self.path:
            if not self.is_valid_move(position, path):
                break
            path.append(position)
        self.fitness = len(path)


class Population:
	def __init__(self, population_size):
		self.population_size = population_size
		self.generation = 1
		self.knights = [Knight() for _ in range(self.population_size)]


	def check_population(self):
		for knight in self.knights:
			knight.check_moves()

	def evaluate(self):
		for knight in self.knights:
			knight.evaluate_fitness()
			
		best_knight = max(self.knights, key=lambda knight: knight.fitness)
		return best_knight.fitness, best_knight

	def tournament_selection(self, size=3):
		tournament_sample = random.sample(self.knights, size)
		winner1 = max(tournament_sample, key=lambda knight: knight.fitness)
		tournament_sample.remove(winner1)
		winner2 = max(tournament_sample, key=lambda knight: knight.fitness)
		return winner1, winner2

	def create_new_generation(self):
		new_generation = []
		for _ in range(self.population_size // 2):
			parent1, parent2 = self.tournament_selection()
			offspring1, offspring2  = parent1.chromosome.crossover(parent2.chromosome)

			offspring1.mutation()
			offspring2.mutation()

			knight1 = Knight(chromosome=offspring1)
			knight2 = Knight(chromosome=offspring2)

			new_generation.extend([knight1, knight2])
			
		self.knights = new_generation
		self.generation += 1






class Population:
	def __init__(self, population_size):
		self.population_size = population_size
		self.generation = 1
		self.knights = [Knight() for _ in range(self.population_size)]


	def check_population(self):
		for knight in self.knights:
			knight.check_moves()

	def evaluate(self):
		for knight in self.knights:
			knight.evaluate_fitness()
			
		best_knight = max(self.knights, key=lambda knight: knight.fitness)
		return best_knight.fitness, best_knight

	def tournament_selection(self, size=3):
		tournament_sample = random.sample(self.knights, size)
		winner1 = max(tournament_sample, key=lambda knight: knight.fitness)
		tournament_sample.remove(winner1)
		winner2 = max(tournament_sample, key=lambda knight: knight.fitness)
		return winner1, winner2

	def create_new_generation(self):
		new_generation = []
		for _ in range(self.population_size // 2):
			parent1, parent2 = self.tournament_selection()
			offspring1, offspring2  = parent1.chromosome.crossover(parent2.chromosome)

			offspring1.mutation()
			offspring2.mutation()

			knight1 = Knight(chromosome=offspring1)
			knight2 = Knight(chromosome=offspring2)

			new_generation.extend([knight1, knight2])
			
		self.knights = new_generation
		self.generation += 1
	
def graphicTour(L_coor):
    horse = pygame.image.load("knight.png")

    pygame.init()
    window = pygame.display.set_mode((8 * 48, 8 * 48))
    pygame.display.set_caption("Knight's Tour")
    background = pygame.image.load("chessboard2.png")
    background = pygame.transform.scale(background, (8 * 49, 8 * 49))
    index = 0

    # Text:
    font = pygame.font.SysFont("Ubuntu", 16)
    text = []
    surface = []

    while True:
        window.blit(background, (0, 0))

        # if index < 64:  # Adjusted for an 8x8 chessboard
        if index < len(L_coor):
            square_size = 49
            horse_size = 48
            # Adjust the blit position for the horse to center it within the square
            x, y = L_coor[index][0] * square_size + (square_size - horse_size) // 2, L_coor[index][1] * square_size + (square_size - horse_size) // 2
            window.blit(horse, (x, y))
            text.append(font.render(str(index + 1), True, (2, 48, 32)))
            surface.append(text[index].get_rect())
            surface[index].center = (x + horse_size // 2, y + horse_size // 2)
            index += 1
        else:
            x, y = L_coor[index - 1][0] * square_size + (square_size - horse_size) // 2, L_coor[index - 1][1] * square_size + (square_size - horse_size) // 2
            window.blit(horse, (x, y))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    pygame.quit()
                    sys.exit()

        for i in range(index):
            window.blit(text[i], surface[i])
            time.sleep(0.0005)
        pygame.display.update()






def main():
    population_size = 50
    # Create the initial population
    population = Population(population_size)
    while True:
        # Check the validity of the current population
        population.check_population()
        # Evaluate the current generation and get the best knight with its fitness value
        maxFit, best_solution = population.evaluate()
        
        print(f"Gen : {population.generation}, Fitness : {maxFit}")
        if maxFit == 64:
            break
        population.create_new_generation()
    graphicTour(best_solution.path)   

      
if __name__ == '__main__':
	main()