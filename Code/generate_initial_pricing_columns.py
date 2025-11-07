from parameters import *

from pyscipopt import Model
from create_model import create_model


import math # this is needed in _eval
import scipy.stats
from collections import defaultdict
import numpy as np
from copy import copy

def _eval(const, decimal_places=0):
        """Evaluates PySCIPOPt expression without variables
        :param string const: Constant expression as string"""
        for operation in ["log", "sin", "cos", "exp", "sqrt"]:
            const = const.replace(operation, "math."+operation)
        const = const.replace("**", "pow")
        const = const.replace("prod", "_prod")
        const = const.replace("sum", "_sum")

        try:
            return eval(const)
        except:
            raise ValueError("Could not evaluate expression: %s" % const)

def _sum(*args):
    return sum(args)

def _prod(*args):
    out = 1.0
    for a in args:
        out *= a
    return out

class PFHeuristic():
    
    def __init__(self, params, model, subprob, pi, gamma, eta, farkas, optimal, pricing_formulation, optimize_production, cur_perturbation):
        self.params              = params
        self.model               = model
        self.pricer              = model.data["pricer"]   
        self.subprob             = subprob
        self.pi                  = pi
        self.gamma               = gamma
        self.eta                 = eta
        self.farkas              = farkas
        self.optimal             = optimal
        self.pricing_formulation = pricing_formulation
        self.optimize_production = optimize_production # after fixing the maintenance variables, optimizes the resulting NLP
        self.perturbation        = cur_perturbation
        self.fixed_maintenance_actions = []
        np.random.seed(self.pricer.data["heuristics"]["total"])

    def _generate_production_price(self):
        """
        Simulates values for the dual variables for the initial RMP columns.
        :params:
        previous_prices := The parameters generated for the previous column 
        incentive       := How much should we expect out of this machine (were previous attempts too soft/too harsh?)
        """

        demand = params["demand"]
        T_prime = params["T_prime"]

        # analyzing the previous columns. Might be expensive. Don't know how I should do this
        # The idea is to take into account the already added columns. Later saw this mentioned in Lubbecke's book
        if True:
            pass

        production_prices = len(T_prime)*[0]
        for t in self.params["T_prime"]:
            production_prices[t] = 1000

        # for this we need to take into account the other columns. When is production needed? When is it in excess?
        return production_prices

    def _generate_production_vector(self):
        """
        Gets the production vector from the demand duals.

        # Todo: might also want to include the branching duals. Ie, if we're favouring solutions
        # Todo: which maintain at time t1, then the production at t1 should be close to 0.
        """
        # pi vector is the incentive to produce at a given time
        demand = self.params["demand"] # to get an upper bound on production

        avg_price = np.mean(self.pi)
        std_price = np.std(self.pi)

        # disabled for now
        prob_opportunity_cost = {}

        # probability that the price is as high as it is, assuming normal distribution (just to get an idea)
        prob = scipy.stats.norm(loc=avg_price,scale=std_price).cdf(self.pi[1:])
        if np.isnan(prob[0]):
            raise ValueError

        production = {}
        for t in self.params["T_prime"]:
            if prob[t-1] > 0.5:
                current_production = prob[t-1]*demand[t]/(len(self.params["N"])) + self.perturbation*np.random.uniform() # tentative
            else:
                current_production = prob[t-1]*demand[t]/(len(self.params["N"])) - self.perturbation*np.random.uniform() 

            current_production = min(current_production, demand[t]) # no need for excess production
            
            #current_production = truncate(current_production,params["decimal_places"])

            production[t] = min(current_production, self.params[self.subprob].Q)
            if self.model.isZero(self.pi[t]):
                production[t]/=2
            
            production[t] = round(production[t], 3) # to avoid numerical troubles

        return production, prob_opportunity_cost

    def get_column_given_production(self, branching_decisions=[], gamma=[], production=[]):
        """
        Given a fixed production, generates a column that satisfies it. 

        :params:
        production := Fixed production to be satisfied 
        optimal    := Should the resulting model be solved to optimality?
        """

        T_prime = self.params["T_prime"]
        T       = self.params["T"]

        # For now, we can try using either the duals or the farkas duals. 
        if not self.pi:
            self.pi = self._generate_production_price()

        production, prob_opportunity_cost = self._generate_production_vector()

        cur_node_number = self.model.getCurrentNode().getNumber()
        for branching_index in range(len(self.pricer.data["branching_decisions"][cur_node_number][self.subprob])):
            branching_decision = self.pricer.data["branching_decisions"][cur_node_number][self.subprob][branching_index]
            if branching_decision.branching_rule == "disaggregate":
                if self.subprob != branching_decision.branching_var_subprob:
                    continue

                fixed_original_vars = branching_decision.disaggregate_branching_var
                var_val = branching_decision.var_val
                # todo now need to make this proper and make sure that these values aren't changed, they're protected
            else:
                continue

        # this is only optimal in relation to the production schedule that was fixed
        if self.optimal:
            model = self.fixed_production_model()
            
            if params["verbose"] <= 3:
                model.hideOutput()
            model.optimize()


            if model.getNSols() > 0:
                if True:#model.isGE(model.getObjVal(),0) and optimize_production:
                    return self._optimize_production()
                else:
                    objective = model.getObjVal()
                    vars = model.getVarDict()
                    return objective, vars
                
            return 1, [] # infeasible production 

        vars = defaultdict(int)
        vars["not_optimal"] = True

        n = self.params[self.subprob]

        # Due to maintenance contraction
        for v in self.fixed_maintenance_actions:
            # debugging to see how often this is called, to assess its usefulness
            # need to make sure that we are not incurring in degradation and whatnot
            vars[v] = 1
            t = int(v.name.split(",")[1][:-1])
            vars["r[0,%s,%i]"%(k_.name,t)] = k_.Rmax
            vars["m[0,%s,%i]"%(k_.name,t)] = 1
            vars["y[0,%i]"%(t)] = 0
            production[t] = 0 

        for t in self.params["T_prime"]:
            # should the production schedule be changed here? Maybe if things are going well, we should adapt instead of getting infeasibilities

            #vars["y[0,%i]"%t] = truncate(production[t], params["decimal_places"])
            vars["y[0,%i]"%t] = production[t]
   
        for k in n.components.values():
            vars["r[0,%s,0]" % k.name] = k.Rmax
            vars["m[0,%s,0]" % k.name] = 0
        vars["machine_maintenance[0]"] = 0

        t = 1
        while t <= T_prime[-1]:        
            for k in n.components.values():

                if vars["m[0,%s,%i]"%(k.name,t)]: # If component is being maintained, we don't want its degradation   
                    continue # continue instead of break because other components might have natural degradation, even though production is 0

                degradation_dependency = 0
                for component, degradation in k.degradation_dependencies: # degradation is a lambda expression
                    degradation_dependency += _eval(str(degradation(2-vars["r[0,%s,%i]"%(component.name,t-1)]/component.Rmax)), self.params["decimal_places"])
                
                vars["r[0,%s,%i]"%(k.name,t)] = vars["r[0,%s,%i]"%(k.name,t-1)]*k.D - degradation_dependency - _eval(str(k.production_degradation(1+vars["y[0,%i]"%t])), self.params["decimal_places"])      
                vars["r[0,%s,%i]"%(k.name,t)] = vars["r[0,%s,%i]"%(k.name,t)] - 0.00001 # to circumvent all the VERY annoying numerics
                
                # Given the opportunity cost, we would be able to decide if maintenance anticipation makes sense
                python_limit = _eval(str(k.production_limit(vars["r[0,%s,%i]"%(k.name,t)]/k.Rmax)))

                production_limit_exceeded = vars["y[0,%i]"%(t)] > python_limit
                
                if production_limit_exceeded or vars["r[0,%s,%i]"%(k.name,t)] < 0.00001: # python limit might be extremely lax
                    action = 1#vars["m[0,%s,%i]"%(k.name,t//production_granularity)]

                    # Even with full maintenance it might be infeasible (high natural degradation, high degradation from other components) (needs to be before changin the t below)
                    if action > k.n_maintenance_actions:
                        return [float("inf"), vars]
                    
                    if t + k.maintenance_duration[action-1] >= T_prime[-1]: # if maintenance takes 5 periods, you can't start on the penultimate one
                        t = min(t, T_prime[-1]-k.maintenance_duration[action-1] + 1) 
                    
                    for i in range(k.maintenance_duration[action-1]):
                        added_condition = k.Rmax/k.n_maintenance_actions
                        vars["r[0,%s,%i]"%(k.name,t+i)] = min(k.Rmax, vars["r[0,%s,%i]"%(k.name,t+i)] + added_condition)
                        vars["m[0,%s,%i]"%(k.name,t+i)] = action
                        vars["y[0,%i]"%(t+i)] = 0

                    added_maintenance = True
                    while added_maintenance:

                        ###########################
                        added_maintenance = False
                        for k_ in n.components.values():
                            k_maintenance_action = min(action-1, k_.n_maintenance_actions-1) # the big guy might have more maintenance actions
                            for k__ in k_.maintenance_dependencies:
                                # if any period when k__ is being mantained and k_ is not. k__ maintenance might have started earlier, be careful. (maybe we don't need to be careful, we'll never incur in infeasibilities this way, I think)
                                #if vars["m[0,%s,%i]"%(k__.name,t)]: 
                                # even if component A is being maintained because of B, the maintenance of C might imply longer maintenance of A
                                k__maintenance_action = min(k_maintenance_action, k__.n_maintenance_actions-1) # the big guy might have more maintenance actions
                                if any([vars["m[0,%s,%i]"%(k__.name,i)] > vars["m[0,%s,%i]"%(k_.name,i)] for i in range(t,min(len(T),t+k__.maintenance_duration[k__maintenance_action]))]):

                                    added_maintenance = True
                                    if t + k_.maintenance_duration[action-1] >= T[-1]: # if maintenance takes 5 periods, you can't start on the penultimate one
                                        t = min(t, T[-1]-k_.maintenance_duration[action-1] + 1) # I think it should have +1 here, but more instances fail

                                    for i in range(max(k__.maintenance_duration[k__maintenance_action], k_.maintenance_duration[k_maintenance_action])):
                                        vars["m[0,%s,%i]"%(k_.name,t+i)] = min(vars["m[0,%s,%i]"%(k_.name,t+i)] + 1, k_.n_maintenance_actions)
                                        vars["r[0,%s,%i]"%(k_.name,t+i)] = k_.Rmax*vars["m[0,%s,%i]"%(k_.name,t+i)]/ k_.n_maintenance_actions
                                        vars["y[0,%i]"%(t+i)] = 0

                    t-=1 # because components previous to k might have taken production damage
                    break # need to go back and revert the damage to components that were not maintained

            t+=1

        # this might be overkill
        added_maintenance = True
        while added_maintenance:
            added_maintenance = False
            for t in self.params["T"]:
                for k in n.components.values():
                    for k_ in n.components.values():
                        if k in k_.maintenance_dependencies and vars["m[0,%s,%i]"%(k.name,t)] and not vars["m[0,%s,%i]"%(k_.name,t)]:
                            vars["r[0,%s,%i]"%(k_.name,t)] = k_.Rmax
                            vars["m[0,%s,%i]"%(k_.name,t)] = 1
                            vars["y[0,%i]"%(t+i)] = 0  
                            added_maintenance = True

        total_cost = 0
        branching_redcost = 0
        aggregate_index = -1
        for branching_index in range(len(branching_decisions)):
            branching_decision = branching_decisions[branching_index]
            if branching_decision.branching_rule == "aggregatevarbounds":
                aggregate_index += 1

                if self.model.isZero(gamma[aggregate_index]):
                    continue

                # if we branched on sum of all variables, all variables are applicable
                if "all" in branching_decision.branching_thresholds:
                    assert len(branching_decision.branching_thresholds) == 1
                    branching_redcost += gamma[aggregate_index]
                    continue

                # if we branched on sum of variables in subproblem, all variables are applicable
                if "subprob" in branching_decision.branching_thresholds:
                    assert len(branching_decision.branching_thresholds) == 1
                    branching_redcost += gamma[aggregate_index]
                    continue

                branching_thresholds = branching_decision.branching_thresholds
                add_to_branching_cons = True
                for cur_branching_threshold in branching_thresholds:
                    pricing_var, inequality, threshold = cur_branching_threshold

                    if inequality == "<=":
                        if self.model.isGT(vars[pricing_var], threshold):
                            add_to_branching_cons = False
                            break
                    elif inequality == ">=":
                        if self.model.isLT(vars[pricing_var], threshold):
                            add_to_branching_cons = False
                            break
                    else:
                        raise ValueError("Something went wrong with the inequalities.")

                if add_to_branching_cons:
                    branching_redcost += gamma[aggregate_index]
                    
        for k in n.components.values():
            for t in self.params["T"]:
                if vars["m[0,%s,%i]"%(k.name,t)] == 1:
                    total_cost+= k.C 
                        
        vars["total_cost"] = total_cost
        vars["machine_maintenance[0]"] = total_cost
        vars["maintenance_cost"] = total_cost

        total_revenue = 0 # self.pi[0] <- this is being subtracted in add_column_to_rmp
        for t in self.params["T_prime"]:
            total_revenue += self.pi[t]*vars["y[0,%i]"%t]

        objective = (1-self.farkas)*total_cost - total_revenue - branching_redcost # redcost

        # to get the most production possible
        if self.optimize_production:
            objective, vars = self._optimize_production(vars, objective)

        return objective, vars

    def _optimize_production(self, vars, objective):
        orig_vars = copy(vars)
        orig_objective = objective

        heuristic_cons = {}
        if type(vars) == dict or type(vars) == defaultdict:
            for v in vars:
                if "m[" in v:
                    heuristic_cons[v] = vars[v]   
        else:
            for v in vars:
                if "m[" in v.name:
                    heuristic_cons[v.name] = v

        heuristic_cons["total_cost"] = vars["total_cost"]
        pi    = self.pi
        gamma = self.gamma
        cur_node_number = self.model.getCurrentNode().getNumber()
        branching_decisions = self.pricer.get_branching_decision(cur_node_number, self.subprob)
        model = create_model(heuristic_cons=heuristic_cons, branching_decisions=branching_decisions, params=self.params,pricing_formulation=-1,pi=pi,gamma=gamma, subprob=self.subprob, farkas=self.farkas)

        if self.params["verbose"] <= 3:
            model.hideOutput()

        model.setObjlimit(min(orig_objective, 0))
        model.setParam('limits/gap', 0.001)

        time_left = self.pricer.compute_time_left()
        model.setParam('limits/time', min(time_left, self.pricer.data["params"]["time_limit"]/10))
        model.optimize()

        if model.getNSols() == 0:
            #print("Could not optimize production further")
            return orig_objective, orig_vars

        objective = model.getPrimalbound()
        vars = model.getVarDict()
        for v in heuristic_cons:
            vars[v] = heuristic_cons[v]
        vars["maintenance_cost"] = vars["total_cost"]

        #print("heuristic opt time: ", time() - s)
        return objective, vars

    # PF heuristic with local improvement
    def local_search(self):
        """
        Given an heuristic solution, tries to anticipate maintenance actions in an attempt to reduce total cost
        """

        contraction_is_feasible = True
        vars = []#self.initialize_heuristic()
        
        while contraction_is_feasible:
            relevant_vars = {}

            valid_contractions = []
            for k in self.subprob.components:
                # get implications
            
                # if implications is non-empty, then store these
                valid_contractions.append(vars[i])
            
            feasible_contractions = []
            for contraction in valid_contractions:
                local_vars = copy(vars)
                if self.pricer.sol_is_feasible(vars):
                    feasible_contractions.append(contraction)


            for v in vars:
                
                # finding cases where maintenance may be anticipated
                # i.e, look for components B => A, where B is maintenance after A
                if "m" in v:
                    relevant_vars[v] = vars[v]

            objective, vars = self.get_column_given_production()
            
            if not find_contractions:
                break

        return objective, vars

    # This model is infeasible whenever maintenance is required and the production is nonzero
    def fixed_production_model(self):
        """
        Generates a column by dividing the demand by the number of machines.
        This gives us an infeasible problem due to downtime.
        """

        # Easy to get the problem like this
        model = create_model(pi=self.pi,subprob=self.subprob,params=self.params,farkas=self.farkas, pricing_formulation=-1)

        for v in model.getVars():
            if "y" in v.name:
                t = int(v.name.split(",")[1][:-1])
                model.addCons(v <= production[t]) # you can't have equality because the production schedule doesn't know which maintenance actions are required
        
        return model    
