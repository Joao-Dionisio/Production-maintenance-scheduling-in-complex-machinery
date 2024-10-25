from pyscipopt import Pricer, SCIP_RESULT, SCIP_PARAMSETTING
from parameters import *

# Master
from master_problem import master_model
from create_model import create_model # Pricing comes from here as well

# Pricing
#import cython_pricing
from generate_initial_pricing_columns import get_column_given_production
#from pricing_problem_heuristics import *

# Branching
from pricing_branching import PricingBranching, PricingEventHdlr

# ObjLimHdlr
from ObjlimHdlr import ObjLimHdlr

# Misc
from time import time
from math import ceil
from statistics import fmean # dual stabilization

class CutPricer(Pricer):

    def __init__(self):
        
        super().__init__()
        self.optimal_cols   = 0
        self.heuristic_cols = 0
        self.optimal_time   = 0
        self.heuristic_time = 0

        self.master_start_time  = time()
        self.master_time        = 0
        self.heur1_time         = 0
        self.exact_pricing_time = 0

        self.farkas = False
        self.seen_duals = []        
    

    # The initialisation function for the variable pricer to retrieve the transformed constraints of the problem
    def pricerinit(self):
        self.redcost_iteration = 1
        self.farkas_iteration = 1
        
        self.duals = {'convexity': {}, 'production': {}, 'branching': {0:[]}}
        for con_type in ["convexity_cons", "demand_cons"]:
            for i, c in enumerate(self.data[con_type]):
                self.data[con_type][i] = self.model.getTransformedCons(c)

        cur_node_number = 1
        self.data['branching_cons'][cur_node_number] = {}
        for i, c in enumerate(self.data["branching_cons"][cur_node_number]): # should be empty
            self.data['branching_cons'][cur_node_number][i] = self.model.getTransformedCons(c)

        # not needed (visualization)
        self.duals = {}
        for c in self.data["cons"]:
            self.duals[c] = []

    # Farkas pricing to fix infeasibilities and get initial columns
    def pricerfarkas(self):
        self.farkas_iteration += 1
        return self.pricer_code(farkas=True)

    # The reduced cost function for the variable pricer
    def pricerredcost(self):
        self.redcost_iteration += 1
        return self.pricer_code(farkas=False)
    
    # Code for farkas pricing and redcost pricing
    def pricer_code(self,farkas=False):
        start = time()

        dualSolutions = {}
        for con_type in ["convexity_cons", "demand_cons"]:
            dualSolutions[con_type] = []
            if farkas:
                for c in self.data[con_type]:
                    dualSolutions[con_type].append(self.model.getDualfarkasLinear(c))
            else:
                for c in self.data[con_type]:
                    # trying out dual stabilization
                    #dualSolutions[con_type][c].append(self.model.getDualSolVal(c))
                    dualSolutions[con_type].append(self.model.getDualSolVal(c))

        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()
        last_present_parent = cur_node
        last_present_parent_number = last_present_parent.getNumber()
        while last_present_parent_number not in self.data["branching_cons"]:
            last_present_parent = last_present_parent.getParent()
            last_present_parent_number = last_present_parent.getNumber()

        self.data["branching_decisions"][cur_node_number] = self.data["branching_decisions"][last_present_parent_number]
        self.data["branching_cons"][cur_node_number] = self.data["branching_cons"][last_present_parent_number]

        dualSolutions["branching_cons"] = {}
        dualSolutions["branching_cons"][cur_node_number] = {}
        if farkas:
            for branching_var in self.data["branching_cons"][cur_node_number]:
                c = self.data["branching_cons"][cur_node_number][branching_var]
                dualSolutions["branching_cons"][cur_node_number][branching_var] = self.model.getDualfarkasLinear(c)
        else:
            for branching_var in self.data["branching_cons"][cur_node_number]:
                c = self.data["branching_cons"][cur_node_number][branching_var]
                dualSolutions["branching_cons"][cur_node_number][branching_var] = self.model.getDualSolVal(c)

        found_negative_redcost = False
        sum_reduced_cost = self.model.getPrimalbound()
        farley_bound = self.model.getPrimalbound() # optimal solution of RMP
        
        self.master_time += time() - self.master_start_time
        
        # If there are negative reduced cost heuristics, great. Otherwise sort the subproblems by heuristic result and then solve them.
        heuristic_results = [] 
        best_heur_result  = float("inf")
        n_subprobs = len(self.data["params"]["machines_per_group"])

        # not using heuristic ATM
        # parallelize this when doing alternative master
        for subprob in range(n_subprobs):
            
            # no need to order subproblems if there is only 1
            if self.data["params"]["heuristic"] == 1 and n_subprobs == 1:
                break

            if self.data["model"] == 0: # original
                result = self.solve_pricing(subprob, heuristic=2, dualSolutions=dualSolutions, farkas=farkas, found=found_negative_redcost, farley_bound=farley_bound, sum_reduced_cost=sum_reduced_cost)
            elif self.data["model"] == 2: # alternative
                result = self.solve_pricing(dualSolutions=dualSolutions, subprob=subprob, sum_reduced_cost=sum_reduced_cost, farley_bound=farley_bound, found=found_negative_redcost, pricing_formulation=0,farkas=farkas, heuristic=1) # args missing TODO

            if "result" in result: # no negative reduced cost
                if result["result"] == SCIP_RESULT.DIDNOTRUN: # timeout (unlikely - heuristic is fast.)
                    print("Pricing timeout.")
                    return {'result': SCIP_RESULT.DIDNOTRUN}
                else:
                    continue
            
            pricing_model    = result["pricing_model"]
            objval           = result["objval"]
            
            # if column is good and we want heuristic columns (if not, we still use the result for subproblem sorting)
            if self.model.isLT(pricing_model.getPrimalbound(),0) and self.data["params"]["heuristic"] > 1: 
                vars                   = result["vars"]
                maintenance_cost       = result["maintenance_cost"]
                found_negative_redcost = True
                self.add_column_to_RMP(objval, vars, subprob, maintenance_cost) 

            heuristic_results.append((objval[0], subprob)) # because we may want to order subprobs by their objval (heuristic only gets 1 sol, hence objval[0])
            best_heur_result = min(best_heur_result, objval[0])

        if found_negative_redcost:
            return {'result': SCIP_RESULT.SUCCESS}
        
        # If heuristic redcost are all positive
        if heuristic_results:
            if self.model.isGE(best_heur_result, 0) or self.data["params"]["heuristic"] == 1:
                heuristic_results.sort() # heuristically getting more promissing subproblems

                ordered_subprobs = [heuristic_results[i][1] for i in range(len(heuristic_results))] # heuristic tells us which subprob to go for
            else:
                ordered_subprobs = [] # heuristics found at least one good column. No need for exact pricing
        else:
            ordered_subprobs = [i for i in range(n_subprobs)] # heuristics found zero solutions
        
        # Getting past redcosts of subproblems to decide order
        if n_subprobs > 1 and self.redcost_iteration >= 10:
            ordered_subprobs = sorted([i for i in range(n_subprobs)], key = lambda subprob: sum(self.data["previous_redcosts"][subprob][-5:]))
            if self.data["straight_subprobs"][1] >= 10 and self.data["straight_subprobs"][0] == ordered_subprobs[0]:
                self.data["straight_subprobs"] = [ordered_subprobs[0], 0] # resetting the count
                ordered_subprobs.append(ordered_subprobs.pop(0)) # moving the subprob to the end 

        found_negative_redcost = False
        for subprob in ordered_subprobs:

            if self.data["model"] == 0:
                # heuristic = 1 is exact pricing. If heuristic gets here, it didn't find negative redcost
                result = self.solve_pricing(subprob, heuristic=1, dualSolutions=dualSolutions, farkas=farkas, found=found_negative_redcost, farley_bound=0, sum_reduced_cost=0, pricing_formulation=-1)
            elif self.data["model"] == 2:
                result = self.solve_pricing(subprob, pricing_formulation=0) # missing args

            # resetting the last time since subprob was solved
            self.data["iterations_since_last"][subprob] = 0

            # no negative redcost
            if "result" in result: 
                if result["result"] == SCIP_RESULT.DIDNOTRUN: # timeout in the middle of pricing
                    return {'result': SCIP_RESULT.DIDNOTRUN}
                elif result["result"] == SCIP_RESULT.INFEASIBLE:
                    return {'result': SCIP_RESULT.INFEASIBLE} # subproblem is infeasible, thus node is infeasible # not true if subproblem is infeasible bc of setObjlimit
                else: # no negative reduced cost
                    self.data["previous_redcosts"][subprob].append(10)
                    continue
            
            pricing_model = result["pricing_model"]
            if self.model.isGE(pricing_model.getPrimalbound(),0):
                if self.data["model"] == 2: # alternative
                   result = self.solve_pricing(pricing_formulation=1)
                   if self.model.isGE(pricing_model.getPrimalbound(),0):
                       result = self.solve_pricing(pricing_formulation=2) # full pricing
                       if self.model.isGE(pricing_model.getPrimalbound(),0):
                           continue
                else:
                    continue

            objval                 = result["objval"]
            vars                   = result["vars"]
            pricing_model          = result["pricing_model"]
            maintenance_cost       = result["maintenance_cost"]
            found_negative_redcost = True
            farley_bound           = result["farley_bound"]
            
            self.add_column_to_RMP(objval, vars, subprob, maintenance_cost, pricing_formulation = result["pricing_formulation"]) 
            self.data["previous_redcosts"][subprob].append(pricing_model.getPrimalbound())

            # to avoid exploring the same subproblem too much
            # capping number of straight iterations in this subprob
            if subprob == self.data["straight_subprobs"][0]:
                self.data["straight_subprobs"][1] += 1 
            else:
                self.data["straight_subprobs"] = [subprob, 1]

            # breaking is broken?
            dont_break = False
            if not farkas:
                if n_subprobs > 1:
                    for i in self.data["iterations_since_last"]:
                        if i != subprob:
                            self.data["iterations_since_last"][i]+=1

                    for i in self.data["iterations_since_last"]:
                        if self.data["iterations_since_last"][i] > (n_subprobs-1)*10: # arbitrary
                            dont_break = True
                            break
                
                if not dont_break:
                    break # breaking straight away to get updated duals
            
        self.master_start_time = time()
        scip_dict = {}

        # if found_negative_redcost and not farkas and optimal_solve: # we are not using this at all.
        #     if self.data["params"]["linear_relaxation"]:
        #         #scip_dict = {"lowerbound": sum_reduced_cost}
        #         scip_dict["lowerbound"] = farley_bound#/(1-pricing_model.getPrimalbound())
        #     else:
        #         #scip_dict = {"lowerbound": ceil(sum_reduced_cost)}
        #         scip_dict["lowerbound"] = ceil(farley_bound)#/(1-pricing_model.getObVal()))+1

        if not found_negative_redcost:
            if farkas:
                return {'result': SCIP_RESULT.SUCCESS} # If farkas can't fix infeasiblity, problem is infeasible

            scip_dict['result'] = SCIP_RESULT.SUCCESS
            #scip_dict['stopearly'] = False
            return scip_dict
                  
        self.optimal_time += (time() - start)
        self.time = time()

        scip_dict['result'] = SCIP_RESULT.SUCCESS 

        return scip_dict

    # Solves pricing problem and prepares to add column to RMP
    def solve_pricing(self, subprob, dualSolutions, sum_reduced_cost, farley_bound=0, heuristic=1, found=False, farkas=False, pricing_formulation=-1):
        """
        Solves the various pricing problems of the different formulations
        parameters:
                    :subprob: subproblem number
                    :dualSolutions: values for the dual variables of the current iteration of the RMP
                    :sum_reduced_cost: shared variable between subproblems for MP lower bound (sum of redcost)
                    :farley_bound: shared variable between subproblem for MP lower bound 
                    :heuristic: combination of heuristics to be used (1 for exact pricing)
                    :found: boolean indicating whether negative redcost column was found
                    :farkas: boolean indicating whether we are doing farkas' pricing
                    :formulation: which pricing problem should we solve? (-1 for original, 0 for production, 1 for maintenance, 2 for full)  
        """

        # Dual Stabilization
        # for c in dualSolutions["production_duals"]:
        #     dualSolutions["production_duals"][c] = fmean(c[-5:])

        cur_node_number = self.model.getCurrentNode().getNumber()
        cur_dualSolutions = {'convexity_duals': dualSolutions["convexity_cons"][subprob], 'production_duals': dualSolutions["demand_cons"], 'branching_duals': dualSolutions["branching_cons"][cur_node_number]}
        pi = [cur_dualSolutions["convexity_duals"]] + cur_dualSolutions["production_duals"]
        gamma = cur_dualSolutions["branching_duals"]
        cur_branching_decisions = self.model.data["pricer"].data["branching_decisions"][cur_node_number]

        #cur_dualSolutions = [dualSolutions[subprob]] + dualSolutions[len(self.data["params"]["machines_per_group"]):]
        heuristic_result = float("inf")
        heuristic_vars = {}
        cur_farley_bound = True
        heuristic_found_sol = False
        
        if heuristic % 2 == 0 and any(pi):
            # trying the heuristic first

            heur1_start_time = time()
            cur_perturbation = -0.1
            cur_tries = 0

            while not heuristic_found_sol and cur_tries < 10: # should be a parameter
                cur_tries += 1
                cur_perturbation += 0.01 # this randomizes the duals a little bit 
                seed = self.data["params"]["global_seed"] + cur_tries

                # cython pricing might be useful later for squeezing in more heuristic rounds
                #heuristic_result, vars = cython_pricing.get_column_given_production(optimal=False,params=self.data["params"],subprob=cur_subprob, pi=cur_dualSolutions, farkas=farkas)
                heuristic_result, vars = get_column_given_production(optimal=False, seed=seed, optimize_production=False, params=self.data["params"],subprob=subprob, pi=pi, gamma=gamma, farkas=farkas, cur_perturbation=cur_perturbation)

                # We have the option of trying to get the optimal maintenance given a fixed production
                if False:#heuristic_result > 0:
                    heuristic_result, vars = get_column_given_production(optimal=True,params=self.data["params"],subprob=cur_subprob, pi=cur_dualSolutions, farkas=farkas)

                self.data["heuristics"]["total"] += 1

                # # we need to remove this when testing. run it once with this just to make sure nothing bad's happening, but it slows
                # # down the heuristic considerably. (also exact pricing since heuristic is used for subprob order)
                # if self.model.isLT(heuristic_result,0):
                #     self.data["heuristics"]["success"] += 1
                #     heuristic_found_sol = True
                #     vars = dict(vars)

                #     # for verifying feasibility, just to be safe. 
                #     if False:                    
                    
                #         pricing_model = create_model(pricing_formulation=pricing_formulation, branching_decisions=cur_branching_decisions, pi=pi, gamma=gamma, subprob=subprob, params=self.data["params"], farkas=farkas)

                #         for v in pricing_model.getVars():
                #             if v.name in vars:                            
                #                 pricing_model.addCons(v - vars[v.name] == 0)

                #         #pricing_model.writeProblem("inf.cip")

                #         if self.data["params"]["verbose"] <= 4:
                #             pricing_model.hideOutput()         
                #         else:
                #             print("Starting heuristic verification")  

                #         pricing_model.optimize()

                #         cur_farley_bound = False
                        
                #         self.heur1_time += time() - heur1_start_time
                #         self.data["heuristic_calls"] += 1

                #         if pricing_model.getNSols() > 0:
                #             heuristic_vars = pricing_model.getVarDict()
                #             heuristic_result = pricing_model.getPrimalbound()
                #             if self.model.isLT(heuristic_result,0) and self.data["params"]["verbose"] >= 3:
                #                 print("Heuristic found sol after %i tries. res: %.2f" % (cur_tries, heuristic_result))
                #             break
                #         else:
                #             # just to ensure that the column added by the heuristic is feasible
                #             raise ValueError("Pricing model should be feasible")
                        

            if not heuristic_found_sol and self.data["params"]["verbose"] >= 2:# and self.data["params"]["heuristic"] > 1:
                if self.data["params"]["heuristic"] == 2:
                    print("Heuristic did not find sol.")
                if heuristic == 2:
                    return {"result": None}

        if heuristic == 1 or not heuristic_found_sol or self.model.isGE(heuristic_result,0) or heuristic_vars in self.data["patterns"][subprob].values():
            exact_pricing_start_time = time()

            # we need to be careful about passing the right duals
            pricing_model = create_model(pi=pi, gamma=gamma, branching_decisions=cur_branching_decisions, subprob=subprob, params=self.data["params"], farkas=farkas, pricing_formulation=pricing_formulation)
            pricing_model.data = {}
            pricing_model.data["objLim_stop"] = False
            # check whether this actually speeds things up
            #objLimHdlr = ObjLimHdlr(pricing_model)
            #pricing_model.includeEventhdlr(objLimHdlr, "Objective limit handler", "Stops solving if dual bound >= 0.")

            # setObjlimit does not work because it marks the model as infeasible (early cutoff)
            # pricing_model.setObjlimit(0) # only interested in these solutions
            
            # check #847. getObjVal has a too strict stage check
            pricing_model.setParam('limits/gap', 0.05) # maybe this is too large. Perhaps it's better to just go for optimality from the get go
            pricing_model.setParam('limits/solutions', 3) # this is not working because sometimes we get a solution that was added in a previous iteration
            
            time_left = self.data["params"]["time_limit"] - (time() - self.data["params"]["start_time"])
            if time_left <= 0:
                return {'result': SCIP_RESULT.DIDNOTRUN}

            pricing_model.setParam("limits/time", time_left)

            if self.data["params"]["verbose"] < 3:
                pricing_model.hideOutput()
            pricing_model.optimize()
            
            # can't use this in conjunction with setObjlimit(0)
            if False and not pricing_model.data["objLim_stop"] and pricing_model.getNSolsFound() == 0:
                return {'result': SCIP_RESULT.INFEASIBLE} 

            if self.model.isGE(pricing_model.getPrimalbound(), 0):
                best_sol = pricing_model.getBestSol()
                pricing_model.freeTransform()
                pricing_model.setParam('limits/gap', 0) # figure out how to recover solution process to avoid starting from scratch
                pricing_model.setParam('limits/solutions',-1)
                #pricing_model.trySol(best_sol)
                pricing_model.optimize()
        
            self.optimal_cols += 1
            self.exact_pricing_time += time() - exact_pricing_start_time
        
        sols = pricing_model.getSols()

        if not farkas and subprob == 1 and sols:
            print(pricing_model.getObjVal())

        if len(sols) == 0: 
            #return {'result': SCIP_RESULT.INFEASIBLE}
            return {'result': SCIP_RESULT.INFEASIBLE}
        
        sols = [s for s in sols if self.model.isLT(pricing_model.getSolObjVal(s),0)]

        # if no negative redcost solution found, return
        if sols == []:
            return {"result": None}

        # trying to get better bounds
        if not farkas and cur_farley_bound and pricing_model.getNSols() > 0:
            sum_reduced_cost += pricing_model.getDualbound() # In case we don't solve the problem to optimality 
            farley_bound += self.data["params"]["machines_per_group"][subprob]*pricing_model.getDualbound()
        
        objval = {}
        vars = {}
        maintenance_cost = {}
        for i, s in enumerate(sols):
            obj = pricing_model.getSolObjVal(s)
            objval[i] = obj

            cur_vars = {}
            for var in pricing_model.getVars():
                cur_vars[var.name] = pricing_model.getSolVal(s, var)
                if "cost" in var.name:
                    maintenance_cost[i] = cur_vars[var.name]
            vars[i] = cur_vars

        best_obj = objval[0]
        if not farkas:
            self.data["red_cost"].append(best_obj)
            if self.data["params"]["verbose"] >= 2:
                print("Subproblem %i iteration %i: %.9f" % (subprob, self.redcost_iteration, best_obj))
        else:
            if self.data["params"]["verbose"] >= 2:
                print("Farkas redcost: %.5f. %i solutions for subprob %i." % (best_obj, len(self.data["patterns"][subprob])+1, subprob))
        
        result = {
            "found":               True,
            "objval":              objval,
            "vars":                vars,
            "pricing_model":       pricing_model, 
            "subprob":             subprob,
            "pricing_formulation": pricing_formulation,
            "maintenance_cost":    maintenance_cost, 
            "sum_reduced_cost":    sum_reduced_cost,
            "farley_bound":        farley_bound
        }

        return result

    def fix_columns_in_ARM(self, subprob, pricing_formulation=-1):
        """
        In here maybe just check or enforce the dominance results
        """
        assert pricing_formulation != 0

    def regroup_columns(self, Delta, Mu):
        """
        In here regroup the columns in order to solve the original pricing problem
        """
        return 

    # Adds column to RMP
    def add_column_to_RMP(self, objval, vars, subprob, maintenance_cost, pricing_formulation=-1):
        
        # for each solution found in subproblem
        for i in range(len(objval)):

            # for verifying feasibility, just to be safe. 
            # pricing_model = create_model(pricing_formulation=pricing_formulation, pi = (1+len(self.data["params"]["T"]))*[0], subprob=subprob, params=self.data["params"])

            # for v in pricing_model.getVars():
            #     if v.name in vars:                            
            #         pricing_model.addCons(v == vars[v.name])
            # pricing_model.hideOutput()
            # pricing_model.optimize()
            # assert pricing_model.getNSols() > 0
            
            # Checking if reduced cost is negative. If column was already visited, discard it.
            # 9.10 - commented out the checking of already visited column
            if self.model.isLT(objval[i],0) and vars[i] not in self.data["patterns"][subprob].values(): # the verification of pattern already added may be costly

                        
                # Adding the new variable to the constraints of the master problem
                currentNumVar = len(self.data['var'][subprob])

                # Creating new var; must set pricedVar to True
                # Variable with asterisk to indicate it was priced.

                # CONSIDER REMOVING THE UPPER BOUND OF THE VARIABLES!!!!! THE CONVEXITY CONSTRAINT IS STRONGER, BUT IF YOU DIDN'T HAVE IT, THEN YOU WOULD NEED THE DUALS FROM THE BOUND CONSTRAINTS
                if self.data["params"]["linear_relaxation"]:
                    vtype="C"
                else:
                    vtype="I"

                # Adding lambda variable
                if pricing_formulation == -1:
                    # newVar = self.model.addVar("lambda[%i,%s]*" % (subprob, currentNumVar), vtype=vtype,
                    #                         lb = 0, ub=self.data["params"]["machines_per_group"][subprob], obj=maintenance_cost[i], pricedVar=True)
                    newVar = self.model.addVar("lambda[%i,%s]*" % (subprob, currentNumVar), vtype=vtype,
                                            lb = 0, obj=maintenance_cost[i], pricedVar=True)
                
                # Adding mu variable
                if pricing_formulation in [0,2]:
                    maintenance_pattern = "a"
                    newVar = self.model.addVar("mu[%i,%i,%s]*" % (subprob, maintenance_pattern, currentNumVar), vtype=vtype,
                                            lb = 0, obj=maintenance_cost[i], pricedVar=True)
                
                # Adding delta variable
                if pricing_formulation in [1,2]:
                    newVar = self.model.addVar("delta[%i,%s]*" % (subprob, currentNumVar), vtype=vtype,
                                            lb = 0, obj=maintenance_cost[i], pricedVar=True)

                # adding the new column to convexity constraint
                if pricing_formulation == -1:
                    self.model.addConsCoeff(self.data["convexity_cons"][subprob], newVar, 1)

                # Adding new column to demand constraints (this will be harder with other formulations)
                if pricing_formulation == -1:                
                    for t, c in enumerate(self.data["demand_cons"]):
                        self.model.addConsCoeff(
                            c, newVar, vars[i]["y[0,%i]" % (t+1)])

                # Storing the new variable in the pricer data.
                self.data['var'][subprob][newVar.name] = newVar
                self.data['patterns'][subprob][newVar.name] = vars[i]
    

def create_pricer(params=params):

    n_subprobs = len(params["machines_per_group"])
    
    # The columns will be stored here
    X = {i: {} for i in range(n_subprobs)}
    

    # master_problem will coordinate the subproblems. 
    if params["model"] == 0:
        master_problem, convexity_cons, demand_cons = master_model(X,params=params)
    elif params["model"] == 1:
        master_problem, maintenance_convexity_cons, production_convexity_cons, demand_cons = master_model(X,params=params)

    master_vars = master_problem.getVars()

    master_problem.setParam("limits/time", params["time_limit"])

    pricer = CutPricer()
    master_problem.includePricer(
        pricer, "Pricer for machine maintenance scheduling", "Pricer to identify patterns for machine scheduling")

    # Setting the pricer data to use in the init and redcost methods
    pricer.data = {}
    pricer_vars = {i: {} for i in range(n_subprobs)}
    for _, var in enumerate(master_vars):  # Getting the relevant variables from the master problem
        var_name = var.name
        if var_name[0] != "l": # don't want the dummy variable
            continue
        cur_subprob = int(var_name.split("[")[1].split(",")[0])
        #pricer_vars[cur_machine].append(var)
        pricer_vars[cur_subprob][var_name] = var

    if params["model"] == 0:
        pricer.data['cons']            = convexity_cons + demand_cons # maybe we should split the constraints
        # like this
        pricer.data["convexity_cons"]  = convexity_cons
        pricer.data["demand_cons"]     = demand_cons
        pricer.data["branching_cons"]  = {}
        
    elif params["model"] == 1:
        pricer.data['cons']                = maintenance_convexity_cons + production_convexity_cons + demand_cons # maybe we should split the constraints
        pricer.data["maintenance_convexity_cons"] = maintenance_convexity_cons
        pricer.data["production_convexity_cons"]  = production_convexity_cons
        pricer.data["demand_cons"]                = demand_cons
        
    pricer.data['var']                     = pricer_vars
    pricer.data['patterns']                = X
    pricer.data['incumbent']               = [float("inf")]
    pricer.data['bound']                   = [-float("inf")]
    pricer.data["params"]                  = params
    pricer.data["red_cost"]                = []
    pricer.data["branching_decisions"]     = {1:[]}
    pricer.data["pseudo_branching"]        = {1:()}
    pricer.data["seen_nodes"]              = {}
    pricer.data["infeasibilities"]         = {}
    pricer.data["added_local_constraints"] = {1: True}
    pricer.data["heuristic_calls"]         = 0
    pricer.data["buggy_heuristic"]         = 0
    pricer.data["model"]                   = params["model"]
    pricer.data["straight_subprobs"]       = [-1,-1]
    pricer.data["heuristics"]              = {"total": 0, "success": 0}
    pricer.data["previous_redcosts"]       = {i:[] for i in range(n_subprobs)}
    pricer.data["iterations_since_last"]   = {i: 0 for i in range(n_subprobs)}
    pricer.data["objLim_stop"]             = False

    for subprob in pricer.data["patterns"]:
        pricer.data["patterns"][subprob][-1] = {} # for initialization purposes in the heuristic

    master_problem.data = {}
    master_problem.data["pricer"] = pricer # Trying this in order to be able to access pricer data from the branching rule 
    
    # Starting the solving process
    # Must disable some settings in order to use duality properly
    master_problem.setPresolve(SCIP_PARAMSETTING.OFF)

    # be careful with this, you're using heuristics in the MP now.
    #master_problem.setHeuristics(SCIP_PARAMSETTING.OFF)
    
    master_problem.disablePropagation()
    pricingBranchingRule = PricingBranching(master_problem)
    master_problem.includeBranchrule(pricingBranchingRule, "Pricing branching", "Branches on pricing variables", 99999999, -1, 1)
    
    # if addConsNode is fixed, this isnt' needed
    pricingEventHdlr = PricingEventHdlr(master_problem)
    master_problem.includeEventhdlr(pricingEventHdlr, "Pricing Event handler", "Enforces branching decisions in master variables")

    return master_problem, pricer
   
    """
    # Printing the results and some statistics
    print(2*"\n")
    print("Objective value ", master_problem.getPrimalbound())

    time_spent = round(time() - start, 3)
    print("Time spent ", time_spent)
    pricing_time = 0
    pricing_time += (pricer.optimal_time)
    print("Total master time: ", round(time_spent - pricing_time, 2))
    print("Total pricing time:", round(pricing_time, 2))
    print()


    # Plotting
    _, axarr = plt.subplots(1,2)

    index = range(len(pricer.data["red_cost"]))
    #plt.plot(index, pricer.data["incumbent"])
    axarr[0].plot(index, pricer.data["red_cost"], label = "Reduced Cost")

    # Plotting the evolution of the dual variables
    max_dual = -1
    for c in pricer.duals:
        axarr[1].plot(pricer.duals[c], label=str(c))
        max_dual = max(max_dual, max(pricer.duals[c]))

    #plt.ylim(-5, 5)
    #plt.legend()
    plt.show()
    """


    """
    _, axarr = plt.subplots(1,2)

    index = range(len(pricer.data["red_cost"]))
    #plt.plot(index, pricer.data["incumbent"])
    axarr[0].plot(index, pricer.data["red_cost"], label = "Reduced Cost")
    #axarr[0].plot(index, pricer.data["bound"], label = "Bound")

    # getting first time that optimal solution is reached
    for i in index:
        if pricer.data["incumbent"][i] == pricer.data["incumbent"][-1]:
            axarr[0].scatter(i,pricer.data["incumbent"][i])
            axarr[0].annotate("Iter " + str(i), (i, pricer.data["incumbent"][i]+0.5))
            break

    axarr[0].set_ylim(-1, pricer.data["incumbent"][1]+1)
    #plt.show()
    # Plotting the evolution of the dual variables
    max_dual = -1
    for c in pricer.duals:
        axarr[1].plot(pricer.duals[c], label=str(c))
        max_dual = max(max_dual, max(pricer.duals[c]))
    axarr[1].set_ylim(-10,20)
    plt.show()
    """