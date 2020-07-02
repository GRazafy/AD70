# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 12:33:44 2020

@author: aabbas-t
"""
# Résolution du problème du sac à dos ou KP (Knapsack Problem) à l'aide d'algorithme génétique
# import de la librairie

import numpy as np #utilisation des calculs matriciels
#import pandas as pd #générer les fichiers csv
import random as rd #génération de nombre aléatoire
from random import randint # génération des nombres aléatoires  
import matplotlib.pyplot as plt
import msvcrt as m
import csv
from math import *
    


# Données du problème (générées aléatoirement)
nb_actions=20
ID_objets = np.arange(1,nb_actions+1) #ID des objets à mettre dans le sac de 1 à 10
cout = np.random.randint(50, 350, size = nb_actions) # cout des objets générés aléatoirement
gain_escompte =  cout*np.random.uniform(0, 0.8, size=nb_actions) # gain_escomptes des objets générées aléatoirement
budget = 3000    #Le budget 
print('La liste des objet est la suivante :')
print('ID_objet   Coûts   Gain_escompte')


######################### Q4 ################################
with open("data.csv", 'w',) as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['ID_objet' , 'Couts' , 'Gain_escompte'])
    for i in range(ID_objets.shape[0]):
        print(f'{ID_objets[i]} \t\t {cout[i]} \t\t {gain_escompte[i]}')
        spamwriter.writerow([f'{ID_objets[i]}'] +
                            [f'{cout[i]}'] + [f'{gain_escompte[i]}'])
    print()

# Créer la population initiale
solutions_par_pop = 10 #la taille de la population


######################### Q2 && Q3 ###########################
def generateTab():
    population_initiale = np.empty([solutions_par_pop, nb_actions])
    for i in range (0,solutions_par_pop):
        cout_total = 0
        too_much_actions = False
        seuil_risque = budget*0.25
        
        population_initiale[i] = np.random.randint(seuil_risque/cout, size = nb_actions)
        for j in range (0,nb_actions):
            if (population_initiale[i][j] >= 1):
                cout_total = cout_total + cout[j]*population_initiale[i][j]
                too_much_actions = cout[j]*population_initiale[i][j] > budget*0.25
                
        while (cout_total > budget or too_much_actions):
            cout_total = 0
            population_initiale[i] = np.random.randint(seuil_risque/cout, size = nb_actions)
            for j in range (0,nb_actions):
                if (population_initiale[i][j] >= 1):
                    cout_total = cout_total + cout[j]*population_initiale[i][j] 
                    too_much_actions = cout[j]*population_initiale[i][j] > budget*0.25
    return population_initiale

pop_size = (solutions_par_pop, ID_objets.shape[0])
print('taille de la population = {}'.format(pop_size))
population_initiale = generateTab();   
population_initiale = population_initiale.astype(int)
print('Population Initiale: \n{}'.format(population_initiale))



def cal_fitness(cout, gain_escompte, population, capacite):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * gain_escompte)
        S2 = np.sum(population[i] * cout)
        if S2 <= capacite:
            fitness[i] = S1
        else :
            fitness[i] = 0 
    return fitness.astype(int)  

def selection(fitness, nbr_parents, population):
    fitness = list(fitness)
    parents = np.empty((nbr_parents, population.shape[1]))
    for i in range(nbr_parents):
        indice_max_fitness = np.where(fitness == np.max(fitness))
        parents[i,:] = population[indice_max_fitness[0][0], :]
        fitness[indice_max_fitness[0][0]] = -999999
    return parents

def croisement(parents, nbr_enfants):
    enfants = np.empty((nbr_enfants, parents.shape[1]))
    point_de_croisement = int(parents.shape[1]/2) #croisement au milieu
    taux_de_croisement = 0.8
    i=0
    while (i < nbr_enfants): #parents.shape[0]
        indice_parent1 = i%parents.shape[0]
        indice_parent2 = (i+1)%parents.shape[0]
        x = rd.random()
        if x > taux_de_croisement: # parents stériles
            continue
        indice_parent1 = i%parents.shape[0]
        indice_parent2 = (i+1)%parents.shape[0]
        enfants[i,0:point_de_croisement] = parents[indice_parent1,0:point_de_croisement]
        enfants[i,point_de_croisement:] = parents[indice_parent2,point_de_croisement:]
        i+=1
    return enfants

# La mutation consiste à inverser le bit
def mutation(enfants):
    mutants = np.empty((enfants.shape))
    taux_mutation = 0.5
    for i in range(mutants.shape[0]):
        random_gain_escompte = rd.random()
        mutants[i,:] = enfants[i,:]
        if random_gain_escompte > taux_mutation:
            continue
        int_random_gain_escompte = randint(0,enfants.shape[1]-1) #choisir aléatoirement le bit à inverser   
        if mutants[i,int_random_gain_escompte] == 0 :
            mutants[i,int_random_gain_escompte] = 1
        else :
            mutants[i,int_random_gain_escompte] = 0
    return mutants  

def optimize(cout, gain_escompte, population, pop_size, nbr_generations, capacite):
    sol_opt, historique_fitness = [], []
    nbr_parents = pop_size[0]//2
    nbr_enfants = pop_size[0] - nbr_parents 
    for i in range(nbr_generations):
        fitness = cal_fitness(cout, gain_escompte, population, capacite)
        historique_fitness.append(fitness)
        parents = selection(fitness, nbr_parents, population)
        enfants = croisement(parents, nbr_enfants)
        mutants = mutation(enfants)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants
    print('Voici la dernière génération de la population: \n{}\n'.format(population)) 
    fitness_derniere_generation = cal_fitness(cout, gain_escompte, population, capacite)      
    print('Fitness de la dernière génération: \n{}\n'.format(fitness_derniere_generation))
    max_fitness = np.where(fitness_derniere_generation == np.max(fitness_derniere_generation))
    sol_opt.append(population[max_fitness[0][0],:])
    return sol_opt, historique_fitness



#paramètres de l'algorithme génétique
nbr_generations = 100 # nombre de générations
#lancement de l'algorithme génétique
sol_opt, historique_fitness = optimize(cout, gain_escompte, population_initiale, pop_size, nbr_generations, budget)


#affichage du résultat
print('La solution optimale est: \n{}'.format(sol_opt))
print(np.asarray(historique_fitness).shape)
print('Avec une gain_escompte de : ',np.amax(historique_fitness),'€ et un cout de  : ', np.sum(sol_opt * cout),'euros')
print()
print('\n Nombre d\'actions maximum avant de dépasser le budget :')
objets_selectionnes = ID_objets * sol_opt
for i in range(objets_selectionnes.shape[1]):
  if objets_selectionnes[0][i] != 0:
     print('{}\n'.format(objets_selectionnes[0][i]))

     
historique_fitness_moyenne = [np.mean(fitness) for fitness in historique_fitness]
historique_fitness_max = [np.max(fitness) for fitness in historique_fitness]
plt.plot(list(range(nbr_generations)), historique_fitness_moyenne, label = 'gain_escomptes moyennes')
plt.plot(list(range(nbr_generations)), historique_fitness_max, label = 'gain_escompte maximale')
plt.legend()
plt.title('Evolution de la Fitness à travers les générations')
plt.xlabel('Génerations')
plt.ylabel('Fitness')
plt.show()