from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from Function import MCMC

# topologic order D (0), I (1), G (2), S (3), L (4)

model = BayesianModel([('0', '2'), ('1', '2'), ('2', '4'), ('1', '3')])

cpd_d = TabularCPD(variable='0', variable_card=2, values=[[0.6, 0.4]])
cpd_i = TabularCPD(variable='1', variable_card=2, values=[[0.7, 0.3]])
cpd_g = TabularCPD(variable='2', variable_card=3, 
                   values=[[0.3, 0.05, 0.9,  0.5],
                           [0.4, 0.25, 0.08, 0.3],
                           [0.3, 0.7,  0.02, 0.2]],
                  evidence=['1', '0'],
                  evidence_card=[2, 2])

cpd_l = TabularCPD(variable='4', variable_card=2, 
                   values=[[0.1, 0.4, 0.99],
                           [0.9, 0.6, 0.01]],
                   evidence=['2'],
                   evidence_card=[3])

cpd_s = TabularCPD(variable='3', variable_card=2,
                   values=[[0.95, 0.2],
                           [0.05, 0.8]],
                   evidence=['1'],
                   evidence_card=[2])

model.add_cpds(cpd_d, cpd_i, cpd_g, cpd_l, cpd_s)


query = 0
evidence = {'1' : 1, '4': 1}

MCMC(model, evidence, query, 4000)