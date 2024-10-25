from pyscipopt import Model, quicksum
from parameters import *


def master_model(X, params=params):
    '''
    parameters

    :X:       Patterns to choose from
    :params:  Instance parameters 
    :integer: Force integer variables (and thus branch and price) or not 
    '''

    demand = params["demand"]
    T = params["T"]
    linear_relaxation = params["linear_relaxation"]
    n_groups = len(params["machines_per_group"])
    
    model = Model("Master Problem")    

    #### Variable Declaration
    var_lambda = {}
    for subprob in range(n_groups): # number of subproblems
        for i in range(len(X[subprob])): # the columns in each subproblem
            if linear_relaxation:
                var_lambda[subprob,i] = model.addVar("lambda[%i,%i]"%(subprob,i), lb=0.0, ub=params["machines_per_group"][subprob], vtype="C") 
            else:
                var_lambda[subprob,i] = model.addVar("lambda[%i,%i]"%(subprob,i), lb=0.0, ub=params["machines_per_group"][subprob], vtype="I") 

    y = model.addVar(ub=0, lb=0) # dummy variable to get duals of bound constraints

    #### Objective    
    total_cost = 0
    for subprob in range(n_groups):
        for i in range(len(X[subprob])):
            total_cost += var_lambda[subprob,i]*X[subprob][i]["total_cost"]
    model.setObjective(total_cost, "minimize")
    
    # Since the costs have a small number of decimal places, the int conversion should work well
    all_int = True
    for n in range(len(params["machines_per_group"])):
        for k in params[n].components:
            if type(k.C) != int:
                all_int = False
                break
        if not all_int:
            break
    
    if all_int:
        model.setObjIntegral() # not always true. Eg. c_1 = 1/pi, c_2 = 1. Can't make the objective function integral

    # Convexity constraints  
    convexity_cons = []
    for subprob in range(n_groups): 
        convexity_cons.append(model.addCons(quicksum(y + var_lambda[subprob,i] for i in range(len(X[subprob]))) <= params["machines_per_group"][subprob], modifiable=True, name="O_convexity_%i"%subprob))

    # Demand constraints 
    demand_cons = []
    for t in T:
        total_production = 0
        for subprob in range(n_groups):
            for i in range(len(X[subprob])):
                total_production += var_lambda[subprob,i]*X[subprob][i]["y[%i]"%t] 
        demand_cons.append(model.addCons(y + total_production >= demand[t], modifiable=True, name="O_demand_%i"%t))
    
    return model, convexity_cons, demand_cons