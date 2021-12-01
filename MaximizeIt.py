# Enter your code here. Read input from STDIN. Print output to STDOUT
'''
    Cian Allen Hackerank "Maximize It!" Practice Problem
    
    For this solution I implemented an evolutionary algorithm to find the optimal solution: 
        -100 epochs
        -0.8 crossover rate
        -0.7 mutation rate.
'''

'''imports'''
import sys
import random

'''F(x)'''
def f(x):
    return int(x)**2

'''preprocess our input list'''
def preprocess():
    #convert stdin to a list
    k_lists=[]
    k=0
    m=0
    for idx, line in enumerate(sys.stdin):
        lis=line.split(" ")     
        
        '''remove new line characters'''
        if "\n" in lis[-1]:
            lis[-1] = lis[-1][:-1] 
            
        '''convert elements to a list'''
        ints = [int(item) for item in lis]
        
        '''if first line, extract k and m, else get the list from the line'''
        if idx == 0:
            k, m = lis
        else:    
            new_list = [item for item in lis[1:]]
            k_lists.append(new_list)
    
    return (k, m, k_lists)

    
''' candidate solution class''' 
class candidate():
    
    '''initialize'''
    def __init__(self, k_lists, m):
        
        self.solution=[]
        self.m = int(m)
        
        '''generate a random solution at initialization'''
        for lis in k_lists:
            self.solution.append(random.choice(lis))
        
        '''get candidates current fitness'''
        self.fitness = self.get_fitness()

    '''fitness (essentially just maximize our desired function)'''
    def get_fitness(self):
        list_sum = 0
        for elem in self.solution:
            list_sum += f(elem)
        return list_sum % self.m
    
        
'''population of candidate solutions class'''
class population():
    
    '''Initalize our population'''
    def __init__(self, pop_size, lis_info, cross_rate, mutate_rate):
        
        self.cr = cross_rate
        self.mutate_rate = mutate_rate
        self.p_size = pop_size
        self.pop = {}
        self.k, self.m, self.k_lists = lis_info
        
        for i in range (0, pop_size):
            self.pop[i] = candidate(self.k_lists, self.m)
        
    '''recombination'''
    def recombination(self):

        '''only recombine if random number is less than cross rate (80% percent of the time)'''
        if random.uniform(0,1) < self.cr:
            
            '''one elem for each list alternating'''
            p1 = self.pop[self.p1[0]]
            p2 = self.pop[self.p2[0]]
            
            '''create new solution by flipping between parent one elements and parent two elements'''
            new_sol1 = []
            new_sol2 = []
            if random.uniform(0,1) < 0.5:
                flip=True
            else:
                flip=False
            for p1_elem, p2_elem in zip(p1.solution, p2.solution):
                if flip == True:
                    new_sol1.append(p1_elem)
                    new_sol2.append(p2_elem)
                    flip=False
                else:
                    new_sol1.append(p2_elem)
                    new_sol2.append(p1_elem)
                    flip=True
            
            '''Create new offspring 1'''
            self.off1 = candidate(self.k_lists, self.m)
            self.off1.solution = new_sol1
            self.off1.fitness = self.off1.get_fitness()
            
            '''Create new offspring 2'''        
            self.off2 = candidate(self.k_lists, self.m)
            self.off2.solution = new_sol2
            self.off2.fitness = self.off2.get_fitness()
        else:
            
            '''We didn't crossover, just pass parents through to next round'''
            self.off1 = self.pop[self.p1[0]]
            self.off2 = self.pop[self.p2[0]]          
        
    
    '''mutation'''
    def mutation(self):
        rand_choice = random.uniform(0,1)
        
        '''if we'd like to mutate according to our mutation rate'''
        if rand_choice < self.mutate_rate:
            ind_to_mutate=random.randint(0, int(self.k)-1)
            
            '''mutate random element of offspring 1'''
            if random.uniform(0,1) < 0.5:
                elem_avoid = self.off1.solution[ind_to_mutate]
                copy_lis = [x for i,x in enumerate(self.k_lists[ind_to_mutate]) if x!=elem_avoid] 
                self.off1.solution[ind_to_mutate] = random.choice(copy_lis)
                    
                '''mutate random element of offspring 2'''
            else: 
                elem_avoid = self.off2.solution[ind_to_mutate]
                copy_lis = [x for i,x in enumerate(self.k_lists[ind_to_mutate]) if x!=elem_avoid] 
                self.off2.solution[ind_to_mutate] = random.choice(copy_lis)
               
            
    '''Parent Selection'''
    def best_parents(self):
        p1 = (-1, -1)
        p2 = (-1, -1)
        
        for idx, candidate in self.pop.items():
            fit = candidate.fitness
            
            if fit > p1[1] and fit > p2[1]:
                p1=(idx, fit)
            elif fit <= p1[1] and fit >= p2[1]:
                p2=(idx, fit)
                
        self.p1 = p1
        self.p2 = p2

    '''find worst parents in the population'''
    def worst_parents(self):
        r1 = (-1, float("inf"))
        r2 = (-1, float("inf"))
        
        for idx, candidate in self.pop.items():
            fit = candidate.fitness
            
            if fit < r1[1] and fit < r2[1]:
                r1=(idx, fit)
            elif fit >= r1[1] and fit <= r2[1]:
                r2=(idx, fit)
                
        self.replace1 = r1
        self.replace2 = r2
        
    
    '''select parents, recombine them and mutate them'''
    def parent_sel(self):
        
        '''retrieve 2 best parents of population'''
        self.best_parents()
        
        '''recombine the 2 parents using custom recombination'''
        self.recombination()
        
        '''mutate one of the offspring randomly'''
        self.mutation()
        
    '''survivor selection -select worst survivors of population and replace with our offspring'''
    def survivor_sel(self):
        
        '''replace two worst candidates of the population with our new offspring'''
        self.worst_parents()
        
        replace_ind1 = self.replace1[0]
        replace_ind2 = self.replace2[0]
        
        self.pop[replace_ind1] = self.off1
        self.pop[replace_ind2] = self.off2
        
    '''get best individuals of epoch'''
    def epoch_results(self):
        p1 = (-1, -1)
        
        '''get best candidate'''
        for idx, candidate in self.pop.items():
            fit = candidate.fitness
            
            if fit >= p1[1]:
                p1=(idx, fit)
        
        best = self.pop[p1[0]]
        
        '''Uncomment these if you'd like to see the best solution for each epoch'''
        #print('Best solution of epoch: ' + str(best.solution))
        #print('Best fitness of epoch: ' + str(best.fitness) + "\n")
        return best
                
            
        
    '''train the population'''
    def train(self, epoch_limit):
        
        for epoch in range (0, epoch_limit):
            
            #select parents and create offspring with crossover and mutation
            self.parent_sel()
            
            #replace worst individuals
            self.survivor_sel()
        
            best = self.epoch_results()
        
        self.best_fitness = best.fitness
        self.best_solution = best.solution
            
if __name__ == "__main__":

    #prepocess input data
    lis_info = preprocess()
    
    #initialize and train our population
    pop = population(1000, lis_info, 0.8, 0.7)
    pop.train(100)
    
    #get best candidate solution from the population
    answer = pop.best_fitness
    solution = pop.best_solution
    print(answer)
    #print(solution)a
    
