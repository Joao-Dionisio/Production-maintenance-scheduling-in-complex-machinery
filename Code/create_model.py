# pyright: reportOptionalSubscript=false
# pyright: reportPossiblyUnboundVariable=false
from pyscipopt import Model, quicksum
from parameters import *
from copy import deepcopy

def create_model(params, joint_feasibility_check=False, pi=None, gamma=None, eta="a",\
                subprob=-1, farkas=False, pricing_formulation=-2, branching_thresholds=None,\
                fixed_delta=None, fixed_mu=None, heuristic_cons=None, branching_decisions=[], machine_map=None):
    """
    Different formulations of the production-maintenance scheduling problem. For now, all machines start with optimal condition.

    parameters:
                params:              Instance parameters
                pricing:             Bool indicating whether we are solving a pricing problem (OUTDATED)
                pi:                  Dual (or Farkas') values of the current iteration of the RMP
                gamma:               Dual values for the current branching constraints. 
                subprob:             Int indicating which subproblem we are solving (-1: None)
                farkas:              Bool indicating whether we are solving Farkas' pricing
                pricing_formulation: Which pricing problem to solve (-2: None, -1: original, 0: production, 1: maintenance, 2: full)
                branching_decisions: Restrictions on master variables at current node. Pricing only.
                fixed_delta:         Fixed maintenance values for maintenance pattern delta
                args:                Extra arguments for the model
    """

    demand = params["demand"]
    T = params["T"]
    T_prime = params["T_prime"] # experimental. Represents the number of production periods
    production_granularity = len(T_prime)/len(T) # If T_prime=480, T=20, this is 24
    assert int(production_granularity) == production_granularity, "Something went wrong with instance creation."

    linear_relaxation = params["linear_relaxation"]
            
    # Creating the machines with their components   
    N = []
    if pricing_formulation >= -1:
        machines_per_group = [1]
        cur_machine = deepcopy(params[subprob])
        cur_machine.id = 0
        N.append(cur_machine)
    else:
        machines_per_group = params["machines_per_group"]
        for index,n in enumerate(machines_per_group):
            #cur_components = params[index]["components"]
            #components_list = [cur_components[i] for i in cur_components]
            for _ in range(n):            
                cur_machine = deepcopy(params[index])
                cur_machine.id = len(N)
                N.append(cur_machine)
    
    # Create mapping from individual machine index to (subprob, position within subprob)
    machine_map = {}
    machine_idx = 0
    for subprob, num_machines in enumerate(params["machines_per_group"]):
        for pos in range(num_machines):
            machine_map[machine_idx] = (subprob, pos)
            machine_idx += 1

    # todo: think about this!!! later on you might only need partial columns for feasibility, maybe
    if farkas and pricing_formulation > -1:
        pricing_formulation = -1 # careful

    model = Model()
    model.setParam("limits/time", params["time_limit"])
    model.setParam("nlhdlr/concave/detectsum", True) # from Stefan #3899

    if params["model"] == 1:
        if params["verbose"] >= 3:
            model.setParam("display/verblevel", 5)

    #### Variable Declaration
    y = {}
    for n in N:
        if pricing_formulation == 1:
            for t in T_prime:
                # no need adding a constraint saying the continuous variable is equal to 
                # the value in question, can just say it's a parameter
                    y[n.id, t] = fixed_mu["y[0,%i]"%t]
                    continue
        else:
            if not params["discrete_production"]:
                for t in T_prime:
                    y[n.id,t] = model.addVar("y[%i,%i]"%(n.id,t), ub=n.Q, lb=0)
                    if pricing_formulation == -2:
                        if machine_map:
                            subprob, pos = machine_map[n.id]
                    y[n.id,t].data = {"subprob": subprob}
            else:
                if params["discrete_production"]:
                    discrete_y = {}

                    for t in T_prime:
                        discrete_y[n.id,t] = model.addVar("discrete_y[%i,%i]"%(n.id,t), vtype="I", ub=n.n_production_levels, lb=0)
                        y[n.id,t] = n.Q*discrete_y[n.id,t]/n.n_production_levels

    r = {}
    for n in N:
        for t in [0]+T_prime:
            for k in n.components.values():
                r[n.id,k.name,t] = model.addVar("r[%i,%s,%i]"%(n.id,k.name,t),lb=0,ub=k.Rmax)

    m = {}
    for n in N:
        for t in [0]+T:
            for k in n.components.values():
                if k.artificial:
                    m[n.id,k.name,t] = 0
                    continue

                if pricing_formulation == 0:
                    m[n.id,k.name,t] = fixed_delta["m[%i,%s,%i]"%(n.id,k.name,t)]
                    continue


                if linear_relaxation:
                    m[n.id,k.name,t] = model.addVar("m[%i,%s,%i]"%(n.id,k.name,t),vtype="C",lb=0,ub=k.n_maintenance_actions)
                else:
                    m[n.id,k.name,t] = model.addVar("m[%i,%s,%i]"%(n.id,k.name,t),vtype="I",lb=0,ub=k.n_maintenance_actions)
                    if pricing_formulation == -2:
                        if machine_map:
                            subprob, pos = machine_map[n.id]
                    m[n.id,k.name,t].data = {"subprob": subprob}
    
    # possibility for idle machines
    z = {}
    for n in N:
        if not linear_relaxation and pricing_formulation == -2:
            z[n.id] = model.addVar("z[%i]"%n.id, vtype="B") # this doesn't work for the linear relaxation. Because you have semi-idle machines producing stuff
        else:
            z[n.id] = 0     

    machine_maintenance = {}
    for n in N:
        machine_maintenance[n.id] = model.addVar("machine_maintenance[%i]"%n.id, vtype="C", lb=0)
        model.addCons(machine_maintenance[n.id] == quicksum(m[n.id,k.name,t]*k.C for k in n.components.values() for t in [0]+T)) # to make retrieval easier later

    #### Objective
    if pricing_formulation == -2:
        model.setObjective(quicksum(m[n.id,k.name,t]*k.C for n in N for k in n.components.values() for t in [0]+T) , "minimize")   
    else:
        if not joint_feasibility_check:
            var_name_to_object = {}
            for v in model.getVars():
                var_name_to_object[v.name] = v

            total_maintenance = 0
            for k in n.components.values():
                for t in [0]+T:
                    total_maintenance += k.C*m[0,k.name,t]

            branching_redcost = 0
            
            # For single master variable branching
            aux_single_vars = {}

            # For aggregate subproblem branching
            auxiliary_var = {}
            branching_applicable = {}
            aggregate_index = -1

            for branching_index in range(len(branching_decisions)):
                # if pricing_formulation == 0: # todo: double check if this is needed
                #     break

                branching_decision = branching_decisions[branching_index]

                # Forbidding regeneration of master variable in down branch
                if branching_decision.branching_rule == "single":
                    aux_single_vars[branching_index] = {}
                    master_pattern = branching_decision.master_pattern
                    node_position = branching_decision.node_position
                    if node_position == "<=":
                        all_aux_single_vars = 0
                        for var_name, var_val in master_pattern.items():
                            if var_name[0] in ["m","y"]:
                                aux_single_vars[branching_index][var_name] = [model.addVar(vtype="B", name="single_%s_lb"%var_name)]
                                aux_single_vars[branching_index][var_name].append(model.addVar(vtype="B", name="single_%s_ub"%var_name))
                                model.addConsIndicator(var_name_to_object[var_name] <= var_val - 0.1, aux_single_vars[branching_index][var_name][0])
                                model.addConsIndicator(var_name_to_object[var_name] >= var_val + 0.1, aux_single_vars[branching_index][var_name][1])
                            else:
                                continue
                            
                            all_aux_single_vars += (aux_single_vars[branching_index][var_name][0] + aux_single_vars[branching_index][var_name][1])
                        model.addCons(all_aux_single_vars >= 1) # forcing the pattern that comes out to be different
                    else:
                        # only care about down branch
                        continue

                # Constraints on original variables
                elif branching_decision.branching_rule == "disaggregate":
                    var_to_branch_on_name = branching_decision.disaggregate_branching_var
                    inequality = branching_decision.inequality
                    var_val = branching_decision.var_val
                    if inequality == "<=":
                        model.addCons(var_name_to_object[var_to_branch_on_name] <= var_val)
                    elif inequality == ">=":
                        model.addCons(var_name_to_object[var_to_branch_on_name] >= var_val)

                # Constraints on master variables (indirectly via redcost)
                elif branching_decision.branching_rule == "aggregatevarbounds":

                    aggregate_index += 1
                    if model.isZero(gamma[aggregate_index]):
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
                    auxiliary_var[aggregate_index] = {}
    
                    if pricing_formulation == 0:
                        branching_applicable[aggregate_index] = True

                    n_upper_bounds = 0
                    n_lower_bounds = 0
                    upper_bound_indices = []
                    lower_bound_indices = []
                    # the variables need to use the indices because different branching constraints migth use the same (variable, threshold) pair
                    for threshold_index, cur_threshold in enumerate(branching_thresholds):
                            
                        cur_var_name, threshold_inequality, threshold = cur_threshold
                        auxiliary_var[aggregate_index][threshold_index] = model.addVar(vtype="B", name="branching_%i_threshold_%i"%(aggregate_index, threshold_index))
                        if cur_var_name[:2] == "m[":
                            time = int(cur_var_name.split(",")[2][:-1])
                            name = cur_var_name.split(",")[1]
                            cur_var = m[0, name, time]
                        elif cur_var_name[0] == "d": # separating from maintenance because these thresholds are subproblem independent
                            assert params["discrete_production"], "You're trying to use continuous y variables for thresholds"
                            time = int(cur_var_name.split(",")[1][:-1])
                            cur_var = discrete_y[0, time]
                        else:
                            raise ValueError("Branched on artificial variable")

                        # In continuous formulation, maintenance is fixed, so just need to check if constraints are satisfied
                        if pricing_formulation == 0:
                            if threshold_inequality == "<=":
                                if model.isGT(cur_var, threshold):
                                    branching_applicable[aggregate_index] = False
                                    break
                            elif threshold_inequality == ">=":
                                if model.isLT(cur_var, threshold):
                                    branching_applicable[aggregate_index] = False
                                    break
                            continue

                        # Important: you need the split between the down and up branches, because there will be different incentives from gamma
                        varub = cur_var.getUbOriginal()                  
                        varlb = cur_var.getLbOriginal()

                        threshold = int(threshold)
                        if model.isLT(gamma[aggregate_index], 0):
                            if threshold_inequality == "<=":
                                n_upper_bounds += 1
                                upper_bound_indices.append(threshold_index)
                                model.addCons(auxiliary_var[aggregate_index][threshold_index] >= (threshold+1-cur_var)/(threshold+1-varlb))
                            elif threshold_inequality == ">=":
                                n_lower_bounds += 1
                                lower_bound_indices.append(threshold_index)
                                model.addCons(auxiliary_var[aggregate_index][threshold_index] >= (cur_var-threshold)/(varub-threshold))
                        elif model.isGT(gamma[aggregate_index],0):
                            if threshold_inequality == "<=":
                                n_upper_bounds += 1
                                upper_bound_indices.append(threshold_index)
                                model.addCons(auxiliary_var[aggregate_index][threshold_index] <= (varub - cur_var)/(varub - threshold))
                            elif threshold_inequality == ">=":
                                n_lower_bounds += 1
                                lower_bound_indices.append(threshold_index)
                                model.addCons(auxiliary_var[aggregate_index][threshold_index] <= (cur_var-varlb)/(threshold + 1 - varlb))

                    if pricing_formulation != 0:
                        # branching constraint is applicable if all thresholds are met
                        branching_applicable[aggregate_index] = model.addVar(vtype="B", name="branching_%i"%(aggregate_index))

                        if model.isLT(gamma[aggregate_index], 0): # incentive for branching to be 1
                            ub_sum = quicksum([auxiliary_var[aggregate_index][i] for i in upper_bound_indices])
                            lb_sum = quicksum([auxiliary_var[aggregate_index][i] for i in lower_bound_indices])
                            model.addCons(branching_applicable[aggregate_index] >= 1 + ub_sum + lb_sum - n_upper_bounds - n_lower_bounds)
                        else:
                            for threshold_index in range(len(branching_thresholds)): # incentive for branching to be 0
                                model.addCons(branching_applicable[aggregate_index] <= auxiliary_var[aggregate_index][threshold_index])

                    branching_redcost += branching_applicable[aggregate_index]*gamma[aggregate_index]
                    
                else:
                    raise ValueError("Branching rule not recognized")

            if pricing_formulation == -1:
                #model.setObjective((1-farkas)*total_maintenance - quicksum(y[0,t]*pi[t] for t in T) - pi[0] - branching_redcost, "minimize")
                model.setObjective((1-farkas)*total_maintenance - quicksum(y[0,t]*pi[t] for t in T_prime) - branching_redcost, "minimize")

            elif pricing_formulation == 0:
                model.setObjective(- quicksum(y[0,t]*pi[t] for t in T_prime) - 1*eta, "minimize")

            elif pricing_formulation == 1:
                model.setObjective(total_maintenance - branching_redcost, "minimize")
            
            elif pricing_formulation == 2:
                model.setObjective((1-farkas)*total_maintenance - 2*quicksum(y[0,t]*pi[t] for t in T_prime) - branching_redcost, "minimize")

    #########################
    # Heuristic Constraints #
    #########################

    if heuristic_cons:
        for key_str in heuristic_cons:
            if key_str == "total_cost":
                total_maintenance = heuristic_cons[key_str]
                continue

            inner = key_str[key_str.find('[')+1 : key_str.rfind(']')]
            parts = [x.strip() for x in inner.split(',')]
            tuple_key = (int(parts[0]), parts[1], int(parts[2]))
            if type(m[tuple_key]) is int: #artificial component
                continue

            model.addCons(m[tuple_key] == heuristic_cons[key_str])

    # # Zero duals can't improve solution (seems to have a minor impact on time, but produces worse columns)
    if False and pricing_formulation >= -1:
        for n in N:
            for t in T:
                if pi[t] == 0:
                    pi[t] = model.addCons(y[n.id,t] == 0)

    # these are the f and g constraints
    if not joint_feasibility_check:
        if pricing_formulation != 1: # not applicable to discrete PP

            ###############################################################
            #                   CONTINUOUS CONSTRAINTS                    #
            # The constraints below concern the continuous variables only #
            ###############################################################

            #### Possibility for idle machines
            for n in N:
                model.addCons(quicksum(y[n.id,t] for t in T_prime) <= len(T_prime)*n.Q*(1-z[n.id]))

            # Demand satisfaction
            if pricing_formulation == -2:
                for t in T_prime:
                    model.addCons(quicksum(y[n.id,t] for n in N) >= demand[t])
            else:
                for t in T_prime:
                    model.addCons(quicksum(y[n.id,t] for n in N) <= demand[t]) # Valid inequality in pricing

        if pricing_formulation != 0: # not applicable to continuous PP

            #############################################################
            #                   DISCRETE CONSTRAINTS                    #
            # The constraints below concern the discrete variables only #
            #############################################################

            #### Maintenance Dependencies
            for n in N:
                for k1 in n.components.values():
                    for k2 in k1.maintenance_dependencies:
                        for t in T:
                            model.addCons(m[n.id,k2.name,t] <= m[n.id,k1.name,t]) 

            #### Maintenance duration constraints 

            # Imposing duration in maintenance
            for n in N:
                for k in n.components.values():
                    for action in range(k.n_maintenance_actions):
                        for t in T[1:-k.maintenance_duration[action]+1]:
                            model.addCons(quicksum(m[n.id,k.name,i] for i in range(t,t+k.maintenance_duration[action])) >= k.maintenance_duration[action]*(m[n.id,k.name,t]-m[n.id,k.name,t-1]))

            # This inequality is only valid for the integer case
            if False: # todo look at this in the context of T_prime. not linear_relaxation:
                for n in N:
                    for k in n.components.values():
                        if k.maintenance_duration >= len(T):
                            continue
                        for t in T[len(T)-k.maintenance_duration:]: # This is just a valid inequality saying that you can't maintain towards the end of T (because there is no time)
                            model.addCons(m[n.id,k.name,t] <= m[n.id,k.name,len(T)-k.maintenance_duration + 1]) # if maintenance was not scheduled at this time, then the rest cannot be scheduled anymore

    if True:#todo: look at this. pricing_formulation not in [0,1]: # not applicable to continuous and discrete PPs

        ################################################################################
        #                           JOINT CONSTRAINTS                                  #
        # The constraints below concern both the discrete and the continuous variables #
        ################################################################################

        #### r Constraints
        for n in N:
            for k in n.components.values():
                if k.artificial:
                    continue

                model.addCons(r[n.id,k.name,0] == k.Rmax)

        # Imposing reduced load during maintenance
        for n in N:
            for t in T:
                for k in n.components.values():
                    if k.artificial:
                        break
                    for action in range(k.n_maintenance_actions):
                        model.addCons(y[n.id,t] <= (k.n_maintenance_actions-m[n.id,k.name,t])*k.Q)
  
        for n in N:
            for t in T_prime:
                for k in n.components.values():
                    degradation_dependency = 0
                    max_degradation = 0 # smallest big-M possible
                    # IMPORTANT CHANGE!!! Added 1 to degradation and production degradation!!!!!
                    for component, degradation in k.degradation_dependencies: # degradation is a lambda expression
                        degradation_dependency += degradation(2 - (r[n.id,component.name,t-1] / component.Rmax) ) # maybe this should be 0 whenever there is no production
                        max_degradation += degradation(2) # assuming convexity of degradation function

            
                    # only allowing maintenance at the beginning of the year
                    max_degradation += k.production_degradation(1+k.Q) + k.Rmax # - r*k.D # smaller big-M but product of variables
                    if t%production_granularity == 0:
                        model.addCons(r[n.id,k.name,t] <= r[n.id,k.name,t-1]*k.D - k.production_degradation(1+y[n.id,t]) - degradation_dependency + max_degradation*(m[n.id,k.name,t//production_granularity]/k.n_maintenance_actions + z[n.id]))
                    else:
                        model.addCons(r[n.id,k.name,t] <= r[n.id,k.name,t-1]*k.D - k.production_degradation(1+y[n.id,t]) - degradation_dependency + max_degradation*z[n.id])

        #### Load Limitations
        # Limit load by component damage
        for n in N:
            for t in T_prime:
                for k in n.components.values():
                    if k.artificial:
                        break

                    model.addCons(y[n.id,t] <= n.Q*k.production_limit(r[n.id,k.name,t] / k.Rmax))

    return model
