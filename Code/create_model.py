from pyscipopt import Model, quicksum
from parameters import *
from copy import copy

def create_model(params, pi=[], gamma=[], subprob=-1, farkas=False, pricing_formulation=-2, branching_decisions=[]):
    """
    Different formulations of the production-maintenance scheduling problem. For now, all machines start with optimal condition.
    
    parameters:
                params:              Instance parameters
                pricing:             Bool indicating whether we are solving a pricing problem (OUTDATED)
                pi:                  Dual (or Farkas') values of the current iteration of the RMP
                gamma:               Dual values for the current branching constraints. 
                subprob:             Int indicating which subproblem we are solving (-1: None)
                farkas:              Bool indicating whether we are solving Farkas' pricing
                pricing_formulation: Which pricing problem to solve (-2: None, -1: original)
                branching_decisions: Restrictions on master variables at current node. Pricing only.
    """

    demand = params["demand"]
    T = params["T"]
    linear_relaxation = params["linear_relaxation"]
    
    # Creating the machines with their components   
    N = []
    if pricing_formulation >= -1:
        machines_per_group = [1]
        cur_machine = copy(params[subprob])
        cur_machine.id = 0
        N.append(cur_machine)
    else:
        machines_per_group = params["machines_per_group"]
        for index,n in enumerate(machines_per_group):
            for _ in range(n):            
                cur_machine = copy(params[index])
                cur_machine.id = len(N)
                N.append(cur_machine)
    
    model = Model() 
    model.setParam("limits/time", params["time_limit"])

    #### Variable Declaration
    y = {}
    for n in N:
        for t in T:
            y[n.id,t] = model.addVar("y[%i,%i]"%(n.id,t),ub=n.Q, lb=0) 

    r = {}
    for n in N:
        for t in [0]+T:
            for k in n.components:
                r[n.id,k.name,t] = model.addVar("r[%i,%s,%i]"%(n.id,k.name,t),lb=0,ub=k.Rmax)

    # this is to help with numerical stability
    r_prime = {}
    for n in N:
        for t in [0]+T:
            for k in n.components:
                r_prime[n.id,k.name,t] = model.addVar("r'[%i,%s,%i]"%(n.id,k.name,t),lb=0,ub=1)
                model.addCons(r_prime[n.id,k.name,t] == r[n.id,k.name,t] / k.Rmax)
                
    m = {}
    for n in N:
        for t in T:
            for k in n.components:
                if linear_relaxation:
                    m[n.id,k.name,t] = model.addVar("m[%i,%s,%i]"%(n.id,k.name,t),vtype="C",lb=0,ub=1)
                else:
                    m[n.id,k.name,t] = model.addVar("m[%i,%s,%i]"%(n.id,k.name,t),vtype="B")
                    
    #### Objective
    if pricing_formulation == -2:
        model.setObjective(quicksum(m[n.id,k.name,t]*k.C for n in N for k in n.components for t in T), "minimize")   
    else:
        var_name_to_object = {}
        for v in model.getVars():
            var_name_to_object[v.name] = v

        # branching cuts
        branching_redcost = 0
        for var_subprob, pricing_var_name, _, _ in branching_decisions:
            if subprob == var_subprob: # since components may share the same name
                pricing_var = var_name_to_object[pricing_var_name]
                branching_redcost += pricing_var*gamma[pricing_var.name]

        maintenance_cost = model.addVar("m_cost") 
        total_maintenance = 0
        for k in n.components:
            for t in T:
                total_maintenance += k.C*m[0,k.name,t] 
        model.addCons(maintenance_cost == total_maintenance)

        model.setObjective((1-farkas)*maintenance_cost - quicksum(y[0,t]*pi[t] for t in T) - pi[0] - branching_redcost, "minimize")         
        
    ###############
    # Constraints #
    ###############

    #### Possibility for idle machines
    z = {}
    for n in N:
        z[n.id] = model.addVar("z[%i]"%n.id, vtype="B")
        if pricing_formulation == -2: # compact
            model.addCons(quicksum(y[n.id,t] for t in T) <= len(T)*n.Q*(1-z[n.id]))
        else:
            model.addCons(z[n.id] == 0)

    #### Maintenance Dependencies
    for n in N:
       for k1 in n.components:
           for k2 in k1.maintenance_dependencies:
               for t in T:
                    model.addCons(m[n.id,k2.name,t] <= m[n.id,k1.name,t]) 

    #### Downtime Constraints 
    
    # Imposing duration in maintenance
    for n in N:
        for k in n.components:
            for t in T[1:-k.maintenance_duration+1]:
                model.addCons(quicksum(m[n.id,k.name,i] for i in range(t,t+k.maintenance_duration)) >= k.maintenance_duration*(m[n.id,k.name,t]-m[n.id,k.name,t-1]))

    # This inequality is only valid for the integer case
    if not linear_relaxation:
       for n in N:
           for k in n.components:
               if k.maintenance_duration >= len(T):
                   continue
               for t in T[len(T)-k.maintenance_duration:]: # This is just a valid inequality saying that you can't maintain towards the end of T (because there is no time)
                   model.addCons(m[n.id,k.name,t] <= m[n.id,k.name,len(T)-k.maintenance_duration + 1]) # if maintenance was not scheduled at this time, then the rest cannot be scheduled anymore
    
    # Imposing 0 load during maintenance
    for n in N:
        for t in T:
            for k in n.components:
                model.addCons(y[n.id,t] <= (1-m[n.id,k.name,t])*k.Q) 
                    
    #### r Constraints
    for n in N:
        for k in n.components:
            model.addCons(r[n.id,k.name,0] == k.Rmax)

    for n in N:
        for t in T:
            for k in n.components:
                degradation_dependency = 0
                max_degradation = 0 # smallest big-M possible
                for component, degradation in k.degradation_dependencies: # degradation is a lambda expression
                    degradation_dependency += degradation(2-r_prime[n.id,component.name,t-1]) # maybe this should be 0 whenever there is no production
                    max_degradation += degradation(2) # assuming convexity of degradation function
                
                
                max_degradation += k.production_degradation(1+k.Q) + k.Rmax # - r*k.D # smaller big-M but product of variables
                model.addCons(r[n.id,k.name,t] <= r[n.id,k.name,t-1]*k.D - k.production_degradation(1+y[n.id,t]) - degradation_dependency + max_degradation*(m[n.id,k.name,t] + z[n.id]))#4*k.Rmax*m[n.id,k.name,t])

    #### Load Limitations
    # Limit load by component damage
    for n in N:
        for t in T:
            for k in n.components:
                model.addCons(y[n.id,t] <= k.production_limit(r_prime[n.id,k.name,t]))

    # Demand satisfaction  
    if pricing_formulation == -2:
        for t in T:
            model.addCons(quicksum(y[n.id,t] for n in N) >= demand[t]) # leave >= instead of ==. should increase perfomance - Ambros 
    else:
        for t in T:
            model.addCons(quicksum(y[n.id,t] for n in N) <= demand[t]) # Valid inequality in pricing

    return model