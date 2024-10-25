from parameters import *

from pyscipopt import Model
from create_model import create_model


import math # this is needed in _eval
import scipy.stats
from collections import defaultdict
import numpy as np

np.random.seed(0)

def _generate_production_price(subprob, pi=[], previous_prices=[], incentive="normal", cur_X=[], params=params):
    """
    Simulates values for the dual variables for the initial RMP columns.
    :params:
    previous_prices := The parameters generated for the previous column 
    incentive       := How much should we expect out of this machine (were previous attempts too soft/too harsh?)
    """

    T = params["T"]

    # analyzing the previous columns. Might be expensive. Don't know how I should do this
    if cur_X:
        pass

    production_prices = len(T)*[0]
    for t in T:
        production_prices[t] = 1000

    # for this we need to take into account the other columns. When is production needed? When is it in excess?
    return production_prices

def _generate_production_vector(subprob, pi, params=params, perturbation = 0, seed=37):
    # pi vector is the incentive to produce at a given time
    demand = params["demand"] # to get an upper bound on production
    T = params["T"]
    cur_machine = params[subprob]
    avg_price = np.mean(pi)
    std_price = np.std(pi)
    np.random.seed(seed)

    # Gets the loss of revenue incurred by maintenance downtime
    opportunity_cost = {}
    for k in cur_machine.components:
        opportunity_cost[k.name] = []
        if k.maintenance_duration == 1:
            opportunity_cost[k.name] = pi
        elif k.maintenance_duration == len(pi):
            opportunity_cost[k.name] = [sum(pi)]
        elif k.maintenance_duration > len(pi):
            continue
        else:
            for t in T[:-k.maintenance_duration+1]:
                opportunity_cost[k.name].append(sum(pi[t:t+k.maintenance_duration])) 

    # probability that the price is as high as it is, assuming normal distribution (just to get an idea)
    prob = scipy.stats.norm(avg_price,std_price).cdf(pi[1:])
    if np.isnan(prob[0]):
        raise ValueError

    production = {}
    for t in T:
        if prob[t-1] > 0.5:
            current_production = prob[t-1]*demand[t]/(len(params["N"])) + perturbation*np.random.uniform() # tentative
        else:
            current_production = prob[t-1]*demand[t]/(len(params["N"])) - perturbation*np.random.uniform() 

        current_production = min(current_production, demand[t]) # no need for excess production
        
        production[t] = min(current_production, params[subprob].Q)

    return production


def _eval(const, decimal_places=0):
        """Evaluates PySCIPOPt expression without variables
        :param string const: Constant expression as string"""
        for operation in ["log", "sin", "cos", "exp", "sqrt"]:
            const = const.replace(operation, "math."+operation)
        const = const.replace("prod(", "math.prod([")
        const = const.replace("sum(", "sum([")
        while "))" in const:
            const = const.replace("))", ")])")

        try:
            return eval(const)
        except:
            raise ValueError

def get_column_given_production(subprob, production=[], pi=[], gamma=[], optimal=False, params=params, farkas=False, fixed_maintenance_actions=[], cur_perturbation=0, seed=37, optimize_production=False):
    """
    Given a fixed production, generates a column that satisfies it. 

    :params:
    production := Fixed production to be satisfied 
    optimal    := Should the resulting model be solved to optimality?
    """

    T = params["T"]

    # For now, we can try using either the duals or the farkas duals. 
    if not pi:
        pi = _generate_production_price(subprob=subprob, previous_prices=[], incentive="normal", params=params, seed=seed)

    production = _generate_production_vector(subprob=subprob, pi=pi, params=params)

    # this is only optimal in relation to the production schedule that was fixed
    if optimal:
        model = fixed_production_model(pi=pi,farkas=farkas,subprob=subprob, production=production, params=params)
        
        if params["verbose"] <= 3:
            model.hideOutput()
        model.optimize()


        if model.getNSols() > 0:
            return _optimize_production(vars=model.getVars(), pi=pi, subprob=subprob, farkas=farkas, params=params)
            
        return 1, [] # infeasible production 

    vars = defaultdict(int)
    vars["not_optimal"] = True

    n = params[subprob]

    # Due to maintenance contraction
    for v in fixed_maintenance_actions:
        # debugging to see how often this is called, to assess its usefulness
        # need to make sure that we are not incurring in degradation and whatnot
        vars[v] = 1
        vars["r[0,%s,%i]"%(k_.name,t+i)] = k_.Rmax
        vars["m[0,%s,%i]"%(k_.name,t+i)] = 1
        vars["y[0,%i]"%(t+i)] = 0
        production[t+i] = 0 

    for t in T:
        # should the production schedule be changed here? Maybe if things are going well, we should adapt instead of getting infeasibilities
        vars["y[0,%i]"%t] = production[t]
  
    for k in n.components:
        vars["r[0,%s,0]" % k.name] = k.Rmax
    
    t = 1
    while t <= T[-1]:        
        for k in n.components:

            if vars["m[0,%s,%i]"%(k.name,t)]: # If component is being maintained, we don't want its degradation   
                 continue # continue instead of break because other components might have natural degradation, even though production is 0

            degradation_dependency = 0
            for component, degradation in k.degradation_dependencies: # degradation is a lambda expression
                degradation_dependency += _eval(str(degradation(2-vars["r[0,%s,%i]"%(component.name,t-1)]/component.Rmax)), params["decimal_places"])
            
            vars["r[0,%s,%i]"%(k.name,t)] = vars["r[0,%s,%i]"%(k.name,t-1)]*k.D - degradation_dependency - _eval(str(k.production_degradation(1+vars["y[0,%i]"%t])), params["decimal_places"])      
            vars["r[0,%s,%i]"%(k.name,t)] = vars["r[0,%s,%i]"%(k.name,t)] - 0.001 # to circumvent all the VERY annoying numerics
            
            # Given the opportunity cost, we would be able to decide if maintenance anticipation makes sense
            python_limit = _eval(str(k.production_limit(vars["r[0,%s,%i]"%(k.name,t)]/k.Rmax)))

            production_limit_exceeded = vars["y[0,%i]"%(t)] > python_limit
            
            if production_limit_exceeded or vars["r[0,%s,%i]"%(k.name,t)] < 0.001: # python limit might be extremely lax
                
                # Even with full maintenance it might be infeasible (high natural degradation, high degradation from other components) (needs to be before changing the t below)
                if vars["m[0,%s,%i]"%(k.name,t)] >= 0.5:
                    return [float("inf"), vars]
                
                if t + k.maintenance_duration >= T[-1]: # if maintenance takes 5 periods, you can't start on the penultimate one
                    t = min(t, T[-1]-k.maintenance_duration + 1) 
                
                for i in range(k.maintenance_duration):
                    vars["r[0,%s,%i]"%(k.name,t+i)] = k.Rmax
                    vars["m[0,%s,%i]"%(k.name,t+i)] = 1
                    vars["y[0,%i]"%(t+i)] = 0

                added_maintenance = True
                while added_maintenance:

                    ###########################

                    added_maintenance = False
                    for k_ in n.components:
                        for k__ in k_.maintenance_dependencies:
                            if any([vars["m[0,%s,%i]"%(k__.name,i)] > vars["m[0,%s,%i]"%(k_.name,i)] for i in range(t,min(len(T),t+k__.maintenance_duration))]):

                                added_maintenance = True
                                if t + k_.maintenance_duration >= T[-1]: # if maintenance takes 5 periods, you can't start on the penultimate one
                                    t = min(t, T[-1]-k_.maintenance_duration + 1) # I think it should have +1 here, but more instances fail

                                for i in range(max(k__.maintenance_duration, k_.maintenance_duration)):
                                    vars["r[0,%s,%i]"%(k_.name,t+i)] = k_.Rmax
                                    vars["m[0,%s,%i]"%(k_.name,t+i)] = 1
                                    vars["y[0,%i]"%(t+i)] = 0

                t-=1 # because components previous to k might have taken production damage

                break # break or continue? need to go back and revert the damage to components that were not maintained

        t+=1

    # this might be overkill
    added_maintenance = True
    while added_maintenance:
        added_maintenance = False
        for t in T:
            for k in n.components:
                for k_ in n.components:
                    if k in k_.maintenance_dependencies and vars["m[0,%s,%i]"%(k.name,t)] and not vars["m[0,%s,%i]"%(k_.name,t)]:
                        vars["r[0,%s,%i]"%(k_.name,t)] = k_.Rmax
                        vars["m[0,%s,%i]"%(k_.name,t)] = 1
                        vars["y[0,%i]"%(t+i)] = 0  
                        added_maintenance = True

    total_cost = 0
    branching_redcost = 0
    for k in n.components:
        for t in T:
            #if t%production_granularity == 0:
            if vars["m[0,%s,%i]"%(k.name,t)] == 1:
                total_cost+= k.C 
                if "m[%i,%s,%i]" % (subprob, k.name, t) in gamma:
                    branching_redcost += gamma["m[%i,%s,%i]" % (subprob, k.name, t)]
    vars["total_cost"] = total_cost

    total_revenue = pi[0]
    for t in params["T"]:
        total_revenue += pi[t]*vars["y[0,%i]"%t]
    

    objective = (1-farkas)*total_cost - total_revenue - branching_redcost# redcost

    # to get the most production possible
    if objective >= 0 and optimize_production:
        objective, vars = _optimize_production(vars=vars, pi=pi, gamma=gamma, subprob=subprob, farkas=farkas, params=params)

    return objective, vars

def _optimize_production(vars, subprob, farkas, pi, gamma, params=params):
    heuristic_cons = {}    
    if type(vars) == dict:
        for v in vars:
            if "m[" in v:
                heuristic_cons[v] = vars[v]   
    else:
        for v in vars:
            if "m[" in v.name:
                heuristic_cons[v.name] = v

    model = create_model(heuristic_cons=heuristic_cons, params=params,pricing_formulation=-1,pi=pi,gamma=gamma, subprob=subprob, farkas=farkas)

    if params["verbose"] <= 3:
        model.hideOutput()

    # this is because solving model directly was crashing on some instances (low_20x20x5) (shouldn't be too bad)
    model.writeProblem("model.cip", verbose=False)
    model.readProblem("model.cip")
    model.setObjlimit(0)
    model.setParam('limits/gap', 0.001)

    model.optimize()

    objective = model.getObjVal()
    vars = model.getVarDict()

    return objective, vars

# This model is infeasible whenever maintenance is required and the production is nonzero
def fixed_production_model(subprob, production, params, pi, farkas):
    """
    Generates a column by dividing the demand by the number of machines.
    This gives us an infeasible problem due to downtime.
    """

    # Easy to get the problem like this
    model = create_model(pi=pi,subprob=subprob,params=params,farkas=farkas, pricing_formulation=-1)

    for v in model.getVars():
        if "y" in v.name:
            t = int(v.name.split(",")[1][:-1])
            model.addCons(v <= production[t]) # you can't have equality because the production schedule doesn't know which maintenance actions are required
    
    return model    