import numpy as np
import random
import time


class Maze:
    def __init__(self,filename):
      self.data = np.loadtxt(filename,dtype=int)
      self.penalties=0
      self.start = (0,0)
      self.finish = (self.data.shape[0]-1,self.data.shape[1]-1)
      self.current = self.start
      print(self.data)
    def moveUp(self):
        if self.current[0]-1 >=0:
          nextStep = (self.current[0]-1,self.current[1])
          self.moveandupdate(nextStep)

    def moveDown(self):
        if self.current[0]+1 <= self.finish[1]:
          nextStep = (self.current[0]+1,self.current[1])
          self.moveandupdate(nextStep)

    def moveLeft(self):
        if self.current[1]-1 >= 0:
          nextStep = (self.current[0],self.current[1]-1)
          self.moveandupdate(nextStep)

    def moveRight(self):
        if self.current[1]+1 <= self.finish[0]:
          nextStep = (self.current[0],self.current[1]+1)
          self.moveandupdate(nextStep)

    def moveandupdate(self,newPosition):
        if self.isWall(newPosition):
            self.penalties = self.penalties+1

        if self.isFinish(newPosition) or self.isWay(newPosition):
            self.data[self.current] = 0
            self.data[newPosition] = 10
            self.current = newPosition

    def isWall(self,position):
        return self.data[position] == 1

    def isWay(self,position):
        return self.data[position] == 0

    def isFinish(self,position):
        return position == self.finish

    def resetMaze(self):
        self.data[self.current] = 0
        self.current = self.start
        self.penalties = 0

class GA:
#     move_limit = 100
#     population_size = 100
#     mutation_chance = 0.5
#     loop = 0
#     #population = np.random.randint(1,5,(population_size,move_limit))
#     population = np.random.choice(5, (population_size,move_limit), p=[0, 0.2, 0.3, 0.2, 0.3])
    def __init__(self,filename):
      self.maze = Maze(filename)
      self.move_limit = 100
      self.population_size = 100
      self.mutation_chance = 0.5
      self.loop = 0
      self.population = np.random.choice(5, (self.population_size,self.move_limit), p=[0, 0.2, 0.3, 0.2, 0.3])
    def fitness(self,chromosome):
        for c in chromosome:
            if c == 1 :
                self.maze.moveUp()
            elif c == 2 :
                self.maze.moveDown()
            elif c == 3 :
                self.maze.moveLeft()
            elif c == 4 :
                self.maze.moveRight()
        score = abs(self.maze.finish[0] - self.maze.current[0]) + abs(self.maze.finish[1] - self.maze.current[1]) + self.maze.penalties
#         if score < 5:
#           print("loop : ", GA.loop , " Score : ",score)
        self.maze.resetMaze()
        return score

    def fittestScore(self,population):
        fitness = [self.fitness(c) for c in population]
        sortedFitness = sorted(fitness)
        return sortedFitness[0]

    def crossOver(self,population):
        newPopulation = np.empty([self.population_size,self.move_limit])
        for i in range(0,self.population_size):
            firstParent = population[np.random.randint(0,self.population_size)]
            secondParent = population[np.random.randint(0,self.population_size)]
            crossOverPoint = np.random.randint(0,self.move_limit)
            newPopulation[i,0:crossOverPoint] = firstParent[0:crossOverPoint]
            newPopulation[i,crossOverPoint:] = self.mutate(secondParent[crossOverPoint:])
        return newPopulation
    
    def mutate(self,chromosome):
        if self.mutation_chance > random.random():
            if chromosome.shape[0] is not 0:
                chromosome[np.random.randint(0,len(chromosome))] = np.random.choice(5, 1, p=[0, 0.2, 0.3, 0.2, 0.3])[0]
        return chromosome

    def searchOptimalMovesHelper(self,population,mostFitScore):
        if(mostFitScore <=2):
            return population
        else :
            self.loop = self.loop+1
            fitness = [self.fitness(c) for c in population]
            # fitness,population = zip(*sorted(zip(fitness, population)))
            fitness_arr = np.array(fitness)
            sorted_fitness = fitness_arr.argsort()
            sorted_population = population[sorted_fitness]
            halfMostFit = sorted_population[0:int(len(population)/2)]
            merge = np.concatenate((halfMostFit,halfMostFit), axis=0)
            newPopulation = self.crossOver(merge)
            return self.searchOptimalMovesHelper(newPopulation,self.fittestScore(newPopulation))
    
    def searchOptimalMoves(self,population):
        return self.searchOptimalMovesHelper(population,999)

print("Maze 1 ")
start_time = time.time()

ga1 = GA("1.txt")
best_path = ga1.searchOptimalMoves(ga1.population)
fitness = [ga1.fitness(c) for c in best_path]
fitness_arr = np.array(fitness)
sorted_fitness = fitness_arr.argsort()
fitness_sorted = fitness_arr[sorted_fitness]
sorted_best_path = best_path[sorted_fitness]
# fitness,best_path = zip(*sorted(zip(fitness, best_path)))
print("Loop : ",ga1.loop," Top Score : ",fitness_sorted[0]," Top Path : " , sorted_best_path[0])

print("--- %s seconds ---" % (time.time() - start_time))

print("Maze 2 ")
start_time = time.time()
ga2 = GA("2.txt")
best_path = ga2.searchOptimalMoves(ga2.population)
fitness = [ga2.fitness(c) for c in best_path]
fitness_arr = np.array(fitness)
sorted_fitness = fitness_arr.argsort()
fitness_sorted = fitness_arr[sorted_fitness]
sorted_best_path = best_path[sorted_fitness]
# fitness,best_path = zip(*sorted(zip(fitness, best_path)))
print("Loop : ",ga2.loop," Top Score : ",fitness_sorted[0]," Top Path : " , sorted_best_path[0])
print("--- %s seconds ---" % (time.time() - start_time))

print("Maze 3")
start_time = time.time()
ga3 = GA("3.txt")
best_path = ga3.searchOptimalMoves(ga3.population)
fitness = [ga3.fitness(c) for c in best_path]
fitness_arr = np.array(fitness)
sorted_fitness = fitness_arr.argsort()
fitness_sorted = fitness_arr[sorted_fitness]
sorted_best_path = best_path[sorted_fitness]
# fitness,best_path = zip(*sorted(zip(fitness, best_path)))
print("Loop : ",ga3.loop," Top Score : ",fitness_sorted[0]," Top Path : " , sorted_best_path[0])
print("--- %s seconds ---" % (time.time() - start_time))

print("Maze 4")
start_time = time.time()
ga4 = GA("4.txt")
best_path = ga4.searchOptimalMoves(ga4.population)
fitness = [ga4.fitness(c) for c in best_path]
fitness_arr = np.array(fitness)
sorted_fitness = fitness_arr.argsort()
fitness_sorted = fitness_arr[sorted_fitness]
sorted_best_path = best_path[sorted_fitness]
# fitness,best_path = zip(*sorted(zip(fitness, best_path)))
print("Loop : ",ga4.loop," Top Score : ",fitness_sorted[0]," Top Path : " , sorted_best_path[0])
print("--- %s seconds ---" % (time.time() - start_time))

print("Maze 5")
start_time = time.time()
ga5 = GA("5.txt")
best_path = ga5.searchOptimalMoves(ga5.population)
fitness = [ga5.fitness(c) for c in best_path]
fitness_arr = np.array(fitness)
sorted_fitness = fitness_arr.argsort()
fitness_sorted = fitness_arr[sorted_fitness]
sorted_best_path = best_path[sorted_fitness]
# fitness,best_path = zip(*sorted(zip(fitness, best_path)))
print("Loop : ",ga5.loop," Top Score : ",fitness_sorted[0]," Top Path : " , sorted_best_path[0])
print("--- %s seconds ---" % (time.time() - start_time))