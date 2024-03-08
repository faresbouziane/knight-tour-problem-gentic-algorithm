import pygame, sys
from pygame.locals import *
import numpy as np
import random 

import time

class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes if genes is not None else self.generate_random_genes()

    def generate_random_genes(self):
        return np.random.randint(0,8,64)

    def crossover(self, partner):
        crossover_point = random.randint(1, len(self.genes) - 1)
        new_genes1 = np.concatenate((self.genes[:crossover_point], partner.genes[crossover_point:]))
        new_genes2 = np.concatenate((partner.genes[:crossover_point], self.genes[crossover_point:]))
        return Chromosome(genes=new_genes1),Chromosome(genes=new_genes2)

    def mutation(self, mutation_rate=0.1):
        mutated_genes = self.genes.copy()

        for i in range(len(mutated_genes)):
            if np.random.rand() < mutation_rate:
                mutated_genes[i] = np.random.randint(8)
      


        return Chromosome(genes=mutated_genes)


class Knight:

    def __init__(self, chromosome):
        self.chromosome = chromosome if chromosome is not None else Chromosome(genes=None)
        self.positionx = 0
        self.positiony = 0
        self.fitness = 0
        self.path = [(self.positionx, self.positiony)]
        self.new_position = None  # Add this line to initialize new_position

    def move_forward(self, direction):
        moves = [[1, -2], [2, -1], [2, 1], [1, 2],  [-1, 2], [-2, 1], [-2, -1],  [-1, -2]]
        x, y = self.path[-1]
        dx, dy = moves[direction - 1] 
        self.new_position = (x + dx, y + dy)  # Update new_position
        self.positionx, self.positiony = self.new_position  # Update positionx and positiony
        return self.new_position

    def move_backward(self, direction):
        moves = [[1, -2], [2, -1], [2, 1], [1, 2],  [-1, 2], [-2, 1], [-2, -1],  [-1, -2]]
        x, y = self.path[-1]
        dx, dy = moves[direction - 1] 
        self.new_position = (x - dx, y - dy)  # Update new_position
        self.positionx, self.positiony = self.new_position  # Update positionx and positiony
        return self.new_position
        


    def is_valid_move(self, position):
        x, y = position
        return 0 <= x < 8 and 0 <= y < 8 and position not in self.path

    def is_valid_move2(self, position,i):
        x, y = position
        return 0 <= x < 8 and 0 <= y < 8 and position not in self.path[:i]

  
    def check_moves(self):
     cycle_direction = random.choice([-1, 1])
    
     for direction in self.chromosome.genes:
        self.move_forward(direction)
        print("moved forward")
        x, y = self.positionx, self.positiony  # Use positionx and positiony
        if 0 <= x < 8 and 0 <= y < 8 and (x, y) not in self.path:
            self.path.append((x, y))
            print("path added")
        else:
            self.move_backward(direction)
            print("moved backwards")
            for _ in range(7):
                direction = (direction + cycle_direction - 1) % 8 + 1
                self.move_forward(direction)
                x, y = self.positionx, self.positiony  # Use positionx and positiony
                if 0 <= x < 8 and 0 <= y < 8 and (x, y) not in self.path:
                    self.path.append((x, y))
                    break
                else:
                    self.move_backward(direction)




    def evaluate_fitness(self):
     for pos in self.path:
        x, y = pos
        if 0 <= x < 8 and 0 <= y < 8 and pos not in self.path[:self.path.index(pos)]:
            self.fitness += 1
    # Remove the break statement


class Population:

 def __init__(self,population_size):
     self.population_size = population_size
     self.generation = 1
     self.knights = []

 def initialize_population(self):
       self.knights = [Knight(chromosome=Chromosome(genes=None)) for _ in range(self.population_size)]

 def check_population(self):
        for knight in self.knights:
            knight.check_moves()
            
 def evaluate(self):
        for knight in self.knights:
            knight.evaluate_fitness()
            print(knight.fitness)
        best_knight = max(self.knights, key=lambda knight: knight.fitness)
        best_fitness = best_knight.fitness
        
        return best_knight, best_fitness
#parts belo
 def tournament_selection(self, size=3):
    if len(self.knights) < size:
        return None, None  # Handle the case when there are not enough knights for selection

    selected_knights = random.sample(self.knights, size)

    winner1 = max(selected_knights, key=lambda knight: knight.fitness)
    selected_knights.remove(winner1)

    if len(selected_knights) > 0:
        winner2 = max(selected_knights, key=lambda knight: knight.fitness)
        return winner1, winner2
    else:
        return winner1, None


 def create_new_generation(self):
    new_generation = []

    for _ in range(self.population_size // 2):
        parent1, parent2 = self.tournament_selection()
        offspring1_chromosome , offspring2_chromosome  = parent1.chromosome.crossover(parent2.chromosome)
        
        offspring1_chromosome.mutation()
        offspring2_chromosome.mutation()

        knight1 = Knight(chromosome=offspring1_chromosome)
        knight2 = Knight(chromosome=offspring2_chromosome)

        new_generation.extend([knight1, knight2])

    self.knights = new_generation
    self.generation += 1





def graphicTour(L_coor):
    horse = pygame.image.load("knight.png")

    pygame.init()
    window = pygame.display.set_mode((8 * 48, 8 * 48))
    pygame.display.set_caption("Knight's Tour")
    background = pygame.image.load("board.png")
    background = pygame.transform.scale(background, (8 * 48, 8 * 48))
    index = 0

    # Text:
    font = pygame.font.SysFont("Ubuntu", 16)
    text = []
    surface = []

    while True:
        window.blit(background, (0, 0))
        # if index < 64:  # Adjusted for an 8x8 chessboard
        if index < len(L_coor):
            window.blit(horse, (L_coor[index][0] * 48, L_coor[index][1] * 48))
            text.append(font.render(str(index + 1), True, (0, 0,0)))
            surface.append(text[index].get_rect())
            surface[index].center = (L_coor[index][0] * 48 + 24, L_coor[index][1] * 48 + 24)
            index += 1
        else:
            
            window.blit(horse, (L_coor[index - 1][0] * 48, L_coor[index - 1][1] * 48))
            

        
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
            time.sleep(0.05)
        pygame.display.update()

def main():
    population_size = 50
    # Create the initial population
    population = Population(population_size)
    population.initialize_population()

    while True:
        # Check the validity of the current population
        population.check_population()

        # Evaluate the current generation and get the best knight with its fitness value
        best_solution, max_fit  = population.evaluate()

        if max_fit == 64:
            break

        # Generate the new population
        population.create_new_generation()
        print(len(best_solution.path))
        # Display the solution using Pygame
    graphicTour(best_solution.path)

if __name__ == "__main__":
    main()