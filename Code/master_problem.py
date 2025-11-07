from pyscipopt import Model, quicksum
from parameters import *

def master_model(columns, params=params):
    '''
    parameters

    :columns:       Patterns to choose from
    :params:  Instance parameters 
    :integer: Force integer variables (and thus branch and price) or not 
    '''

    demand = params["demand"]
    T_prime = params["T_prime"]
    linear_relaxation = params["linear_relaxation"]
    n_groups = len(params["machines_per_group"])

    model = Model("Master Problem")

    #### Variable Declaration
    var_lambda = {}
    for subprob in range(n_groups): # This is the number of subproblems
        for i in range(len(columns[subprob])): # the columns in each subproblem
            if linear_relaxation:
                var_lambda[subprob,i] = model.addVar("lambda[%i,%i]"%(subprob,i), lb=0.0, vtype="C") 
            else:
                var_lambda[subprob,i] = model.addVar("lambda[%i,%i]"%(subprob,i), lb=0.0, vtype="I") 

    y = model.addVar(ub=0, lb=0) # dummy variable to get duals of bound constraints
    model.data = {}
    model.data["aux_var"] = y

    #### Objective    
    total_cost = 0
    for subprob in range(n_groups):
        for i in range(len(columns[subprob])):
            total_cost += var_lambda[subprob,i]*columns[subprob][i]["total_cost"]
    model.setObjective(total_cost, "minimize")
    model.setObjIntegral()

    # Convexity constraints  
    convexity_cons = []
    for subprob in range(n_groups): 
        convexity_cons.append(model.addCons(quicksum(y + var_lambda[subprob,i] for i in range(len(columns[subprob]))) <= params["machines_per_group"][subprob], modifiable=True, name="O_convexity_%i"%subprob))

    # Demand constraints 
    demand_cons = []
    for t in T_prime:
        total_production = 0
        for subprob in range(n_groups):
            for i in range(len(columns[subprob])):
                total_production += var_lambda[subprob,i]*columns[subprob][i]["y[%i]"%t] 
        demand_cons.append(model.addCons(y + total_production >= demand[t], modifiable=True, name="O_demand_%i"%t))

    return model, convexity_cons, demand_cons