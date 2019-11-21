import random

populationSize = 100
numberOfGenerations = 100
repeater = 'CGG'
standardRepetitions = 30

file=open("finalCSV.csv","w+")

#FMR1 30 CGG
#ATXN1 33 CAG
#RUNX2 22 CAG + 14 GCG

population=[]
tracker=[]

def repetitions(gene):
    repetitions=0
    current=0
    while(gene[current:current+3]==repeater):
        repetitions+=1
        current+=3
    return repetitions

def generation(population,tracker):
    for i in range(len(population)):
        changeReps=random.random()
        if(changeReps<0.05):
            population[i]=population[i]+repeater
        elif(changeReps<0.1):
            population[i]=population[i][:-len(repeater)]
        tracker[i].append(repetitions(population[i]))
    return population,tracker

for i in range(populationSize):
    gene=''
    for i in range(standardRepetitions):
        gene=gene+repeater
    population.append(gene)
    tracker.append([])
    
for i in range(numberOfGenerations):
    population,tracker=generation(population,tracker)

for i in population:
    print(repetitions(i))

for i in tracker:
    for j in i:
        file.write(str(j)+',')
    file.write("\n")
    
file.close()
