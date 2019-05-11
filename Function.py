from random import seed
from random import random
from random import randint
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import collections


def sampling(Values):
    seed()
    value = random()
    sorted_dict = dict(sorted(Values.items(), key=lambda x: x[1], reverse=True))
    previus = 0
    # print("Value from normale Sampling: ", value)

    for key in sorted_dict.keys():
        if value <= sorted_dict[key] + previus:
            return int(key)
        previus += sorted_dict[key]

def easySampling(trueValue):
    seed()
    value = random()
    # print("Value from easy Sampling:", value)
    
    if value <= trueValue:
        # return true
        return 1
    else:
        # return false
        return 0

def variableChoice(numberOfVariable):
    seed()
    value = randint(0,numberOfVariable - 1)
    return value


def markovBlanket(choice, sample, network):
    cpTableChoice = network.get_cpds(str(choice)).values
    choiceParents = network.get_parents(str(choice))
    choiceChild = network.get_children(str(choice))
    parentConditional = {}
    sonConditional = 1
    parentKey = ''
    childKey = ''

    for parent in choiceParents:
        parentKey += str(sample[int(parent)])
    # print("Parent Key: ",parentKey)
    if len(parentKey) == 2:
        key1 = int(parentKey[0:1],2)
        key2 = int(parentKey[1:], 2)
        for i in range(0, len(cpTableChoice)):
            parentConditional[str(i)] = cpTableChoice[i][key2][key1]
    elif len(parentKey) == 1:
        for i in range(0, len(cpTableChoice)):
            parentConditional[str(i)] = cpTableChoice[i][int(parentKey)]
    else:
        for i in range(0, len(cpTableChoice)):
            parentConditional[str(i)] = cpTableChoice[i]
    # print("Parent Conditional: ", parentConditional)

    for value in parentConditional.keys():
        for child in choiceChild:
            childParent = network.get_parents(str(child))
            childKey = ''
            sonConditional = 1
            for parent in childParent:
                if int(parent) == choice:
                    childKey += value
                else:
                    childKey += str(sample[int(parent)])
            if len(childKey) == 2:
                # print("Son key: ", childKey)
                key1 = int(childKey[0:1])
                key2 = int(childKey[1:])
                sonConditional *= network.get_cpds(str(child)).values[int(sample[int(child)])][key2][key1]
            else:
                sonConditional *= network.get_cpds(str(child)).values[int(sample[int(child)])][int(childKey)]
            # print("Son value: ", sonConditional)
        parentConditional[value] = parentConditional[value] * sonConditional
    
    # print("Parent conditional: ", parentConditional)
    norma = normalize(parentConditional)
    # print("Normalize: ", norma)
    value = sampling(norma)
    # print("Value: ", value)

    return value

def normalize(probabilities):
    alpha = 0.0

    for key in probabilities.keys():
        alpha += probabilities[key]
    # print("alpha:", 1/alpha)
    
    for key in probabilities.keys():
        probabilities[key] = probabilities[key] * (1/alpha)
    
    return probabilities
    

def MCMC(network, evidence, query, nSamples):

    sample = [None]*len(network)
    parents = list()
    cptTable = list()
    trueValues = {}
    key = ''
    choice = 0
    numerator = [0]*len(network.get_cpds(str(query)).values)

    sampleGenerated = 0
    while sampleGenerated <= nSamples:
        if sampleGenerated == 0:
            for i in range(0, len(sample)):
                key = ''
                trueValues = {}
                if str(i) in evidence.keys():
                    sample[i] = evidence[str(i)]
                else:
                    parents = network.get_parents(str(i))
                    for parent in parents:
                        key += str(sample[int(parent)])
                    cptTable = network.get_cpds(str(i)).values
                    if len(key) == 2:
                        key1 = int(key[0:1],2)
                        key2 = int(key[1:], 2)
                        for i in range(0, len(cptTable)):
                            trueValues[str(i)] = cptTable[i][key1][key2]
                        sample[i] = sampling(trueValues)
                    elif len(key) == 1:
                        sample[i] = easySampling(cptTable[1][int(key)])
                    else:
                        sample[i] = easySampling(cptTable[1])
        else:
            choice = variableChoice(len(network))
            # print("SAMPLE BEFORE: ", sample)
            while str(choice) in evidence.keys():
                choice = variableChoice(len(network))
            # print("variable choice: ", choice)
            sample[choice] = markovBlanket(choice, sample, network)
            # print("SAMPLE AFTER: ", sample)
            # print("")
            numerator[sample[query]] += 1
            
        sampleGenerated += 1
    
    
    print(numerator)
    

    for i in range(0, len(numerator)):
        print("The probabilty of {:>1} is {:>5}".format(str(i), str(round((numerator[i]/nSamples)*100, 3)) + '%'))