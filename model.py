import sys, os, random
import matplotlib.pyplot as plt

pop_size = 10000
gen_num = 1000
point_mutation = 1.1 * 10 ** (-7)
"""
This function simuates reproduction with mutation and tandem repeats
"""
def repetition(dna, repeater):
    last_pos = 0
    pos = 2
    #find last position 
    while(pos < len(dna)):
        if(dna[pos] != repeater[2]):
            last_pos = pos #update last position
            #point mutation 
            if(random.random() < point_mutation):
                chance = random.random()
                if(chance < 0.25):
                    dna = list(dna)
                    dna[pos] = 'A'
                    dna = "".join(dna)
                elif(chance < 0.5):
                    dna = list(dna)
                    dna[pos] = 'T'
                    dna = "".join(dna)
                elif(chance < 0.75):
                    dna = list(dna)
                    dna[pos] = 'C'
                    dna = "".join(dna)
                else:
                    dna = list(dna)
                    dna[pos] = 'G'
                    dna = "".join(dna)
        pos = pos + 3
    #tandem repetitions
    k = (len(dna) - 1 - last_pos) / 3
    chance = random.random()
    if(chance < (k - 1) * 10 ** (-3)):
        chance = random.random()
        if(chance < 0.5):
            dna = dna + repeater
        else:
            dna = dna[:-3]

    return dna

"""
This function simulates selection
It returns whether an individual will survive
Conditions come from the given file
"""
def selection(dna, condition):
    survive = True
    for i in range(len(condition)):
        lower, upper, prob = condition[i].split(" ")
        lower = int(lower)
        upper = int(upper)
        prob = float(prob)
        num_rep = len(dna) / 3
        if(num_rep > lower and num_rep < upper):
            chance = random.random()
            if(chance <= prob):
                survive = False
    return survive

def main(argv):
    if(len(argv) < 2 ):
        print("Usage: python3 model.py genes.txt")
        return
    
    file = open(argv[1], "r") 

    for line in file:
        if(line[0] == ">"): #only process DNA name start with ">"
            dna_name, repeater, dna = line.split(" ") #get gene name, repeater, and dna sequence 
            dna_name = dna_name[1:] 
            dna = dna[:-1]
            #print(dna_name)
            #print(repeater)
            #print(dna)
            num_selection = int(file.readline())
            condition = []
            #get selection conditions 
            for i in range(num_selection):
                condition.append(file.readline()[:-1]) #remove newline character
            #initialize population 
            population = []       
            for i in range(pop_size):
                population.append(dna)
            #iterate generations
            for i in range(gen_num):
                for j in range(len(population)):
                    if(j < len(population)):
                        population[j] = repetition(population[j], repeater)
                        #print(len(population[j])/3)
                        if not selection(population[j], condition):
                            print("num of repeat ",len(population[j]) / 3, "individual ", j,  " die out")
                            del population[j] #die out. 
                            print("Delete individal",j, "generation size", len(population))
            total = 0
            tracker = []
            for i in range(len(population)):
                tracker.append(len(population[i]) / 3)
                total = total + len(population[i])/3
            print(gen_num,"generation", len(population), " population avg repeat", total/len(population))
            plt.hist(tracker, bins=40)
            plt.xlabel('Number of repeats', fontsize = 12)
            plt.ylabel("Frequency", fontsize = 12)
            plt.title("Tandem Repeat for Gene " + dna_name)
            txt = "The frequency distribution for gene " + dna_name + " after " + str(gen_num) + " generations. "
            txt = txt + str(len(population)) + " out of " + str(pop_size) + " survived."  
            plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
            plt.show()


if __name__ == "__main__":
    main(sys.argv)
