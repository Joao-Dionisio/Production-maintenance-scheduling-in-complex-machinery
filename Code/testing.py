import pyscipopt as scip

# My code
from parameters import Component, Machine, params

from create_model import create_model
from pricer import create_pricer

# Maths and stats
import math
import random
from time import time

# Instances
from importlib import import_module
import os


def pricer_is_feasible(model, params):
    pricer = model.data["pricer"]

    # Checking convexity constraints
    for subprob in range(len(params["machines_per_group"])):
        subproblem_varsum = 0
        for var in pricer.data["var"][subprob].values():
            subproblem_varsum += model.getVal(var)

        # We must ensure every machine is working. Idle machines may still need repairs
        assert model.isLE(subproblem_varsum, params["machines_per_group"][subprob]), "Convexity"

    # Checking demand constraints
    T = params["T"]
    sol_demand = len(T)*[0]
    for subprob in range(len(params["machines_per_group"])):
        for cur_var in pricer.data["var"][subprob].values():
            cur_var_val = model.getVal(cur_var)
            if model.isGT(cur_var_val, 0):
                cur_pattern = pricer.data["patterns"][subprob][cur_var.name]
                for t in T:
                    sol_demand[t-1] += cur_var_val*cur_pattern["y[0,%i]" % t]

    for t in T:
        assert model.isGE(sol_demand[t-1], params["demand"][t]), "Demand. %.9f" % (sol_demand[t-1] - params["demand"][t])
    
    return True

# Instance parameter generation
def get_random_global_parameters(T_prime, n_machines, seed = 1000000000000066600000000000001, linear_relaxation=True, peak_demand=False):

    new_params = {}
    new_params["eps"] = 10**(-9)
    new_params["decimal_places"] = -round(math.log(new_params["eps"],10)) # to use math.round
    new_params["linear_relaxation"] = linear_relaxation
    new_params["T_prime"] = T_prime
    new_params["time_limit"] = 7200
    new_params["global_seed"] = seed

    import random
    random.seed(new_params["global_seed"])


    demand = {}
    if peak_demand:
        # to simulate peaks and valleys of demand. starting out with just one each
        high_demand = [i for i in range(len(T_prime)//2)]
        low_demand  = [i for i in range(len(T_prime)//2, len(T_prime)+1)]
        for t in high_demand:
            demand[t] = round(max(random.random(),0.1)*n_machines*1.3, 3)
        for t in low_demand:
            demand[t] = round(max(random.random(),0.1)*n_machines/4, 3)
    else:
        for t in T_prime:
            demand[t] = round(random.random()*n_machines/2, 3)

    new_params["demand"] = demand

    return new_params

def get_random_machine(complexity="low", seed = 1000000000000066600000000000001, params=params):
    """
    Randomizes every parameter for a group of machines. Needs a seed for randomness
    """
    
    random.seed(seed)

    if complexity == "low":
        n_components = random.randint(1,3)
    elif complexity == "high":
        n_components = random.randint(3,7)

    cur_components = []
    production_granularity = len(params["T_prime"])//len(params["T"])
    degradation_lb = 0.9**(1/production_granularity) # assuming at least 80% capacity at year's end, with no production
    
    # Component creation
    machine_Q = float("inf")
    for cur_component in range(n_components):
        # I'm truncating the random parameters so that the problem can work with the provided tolerances
        # not using params["decimal_places"] to make debugging easier
        component_name         = str(cur_component) 
        Rmax                   = float("{:.2f}".format(random.uniform(20, 100)*production_granularity))
        C                      = float("{:.2f}".format(random.uniform(2, 20)))
        Q                      = float("{:.2f}".format(random.uniform(1, 3)))
        L                      = float("{:.2f}".format(random.uniform(0.5, 2)))
        D                      = float("{:.4f}".format(random.uniform(degradation_lb, 1)))

        maintenance_duration   = random.randint(1, 8) # number of production periods maintenance takes
        cur_components.append(Component(component_name, Rmax, C, Q, L, D, maintenance_duration))
        machine_Q = min(machine_Q, Q)
        
    # Component degradation
    for i,k1 in enumerate(cur_components):

        degradation_type_sample = random.random()
        if degradation_type_sample <= 0.7:
            degradation_type = "linear"
        elif degradation_type_sample <= 0.9:
            degradation_type = "polynomial"
        else:
            degradation_type = "exponential"
        production_degradation = get_component_degradation(degradation_type=degradation_type, source="load", seed=params["global_seed"]+i)
        k1.production_degradation = production_degradation

        limit_type_sample = random.random()
        if limit_type_sample <= 0.7:
            limit_type = "linear"
        elif limit_type_sample <= 0.9:
            limit_type = "polynomial"
        else:
            limit_type = "exponential"
        production_limit = get_production_limit(limit_type=limit_type, seed=2*params["global_seed"]+i)
        k1.production_limit = production_limit

        # Inter-component interaction
        for j, k2 in enumerate(cur_components):
            if k1 == k2:
                continue
            
            if complexity == "low" and random.random() <= 0.1 or complexity == "high" and random.random() <= 0.15:
                k1.maintenance_dependencies.append(k2)

            if complexity == "low" and random.random() <= 0.1 or complexity == "high" and random.random() <= 0.15:                
                degradation_type_sample = random.random()
                if degradation_type_sample <= 0.7:
                    degradation_type = "linear"
                elif degradation_type_sample <= 0.9:
                    degradation_type = "polynomial"
                else:
                    degradation_type = "exponential"
                degradation = get_component_degradation(degradation_type=degradation_type,source="component", seed=params["global_seed"]+j+len(cur_components))
                
                k1.degradation_dependencies.append((k2,degradation))
    
    n = Machine(0, components=cur_components)
    n.Q = machine_Q
    return n

def get_component_degradation(degradation_type, source, seed=1000000000000066600000000000001):
    random.seed(seed)

    # load probably has a bigger impact that any individual component (maybe)
    if source == "load":
        max_slope       = 3
        max_intercept   = 0 # no production implies no production-based degradation
        max_n_exponents = 3
        max_exponents   = 5 # Always concave in the domain that matters
        max_basis       = 3
        max_exponent    = 3
    else:
        max_slope       = 1.5
        max_intercept   = 4
        max_n_exponents = 1
        max_exponents   = 3
        max_basis       = 1.5
        max_exponent    = 2
    
    if degradation_type == "linear":
        slope = float("{:.3f}".format(max_slope*random.random()))
        intercept = float("{:.2f}".format(max_intercept*random.random()))
        degradation = lambda x: slope*x + intercept
    
    elif degradation_type == "polynomial":
        n_exponents = random.randint(1,max_n_exponents)
        exponents = random.sample(range(1,max_exponents), n_exponents)
        coefs     = [float("{:.2f}".format(random.random())) for _ in range(n_exponents)]
        degradation = lambda x: sum([coefs[i]*x**(exponents[i]) for i in range(n_exponents)])
    
    # basis**(x*exponent)
    elif degradation_type == "exponential":
        basis = float("{:.2f}".format(max(max_basis*random.random(), 1))) # min of 1 because we want increasing degradation 
        exponent = float("{:.2f}".format(max_exponent*random.random())) 
        degradation = lambda x: scip.exp(exponent*x)*scip.log(basis)
    
    return degradation

def get_production_limit(limit_type, seed = 1000000000000066600000000000001):
    """
    Gets the limit on the production given the condition of a particular component. The g functions in 
    the formulation.
    """

    random.seed(seed)
    # it's difficult to estimate these. It will depend heavily on the load that they operate on
    min_slope       = 3
    min_intercept   = 10
    max_n_exponents = 3
    max_exponents   = 5
    min_basis       = 3
    min_exponent    = 3

    if limit_type == "linear":
        slope = float("{:.2f}".format(2*(min_slope+random.random())))
        intercept = float("{:.2f}".format(2*(min_intercept+random.random())))
        limit = lambda x: slope*x + intercept
    
    elif limit_type == "polynomial":
        n_exponents = random.randint(1,max_n_exponents)
        exponents = random.sample(range(1,max_exponents), n_exponents)
        coefs     = [float("{:.2f}".format(random.random())) for _ in range(n_exponents)]
        limit = lambda x: sum([coefs[i]*x**(exponents[i]) for i in range(n_exponents)])
    
    elif limit_type == "exponential":
        basis = float("{:.2f}".format(2*(min_basis+random.random())))
        exponent = float("{:.2f}".format(2*(min_exponent+random.random()))) 
        limit = lambda x: scip.exp(exponent*x)*scip.log(basis)
    
    return limit


# Instance set creation

def create_instance_set(set_seed=1, **kwargs):
    """
    Creates a set of instances to the machine-scheduling problem.
    """

    random.seed(set_seed)

    kwargs["T"] = [i for i in range(1,kwargs["T"]+1)]
    kwargs["machines_per_group"] = eval(kwargs["machines_per_group"])


    for i in range(kwargs["n_instances"]):
        if "specific_instance" in kwargs and kwargs["specific_instance"]:
            i = kwargs["specific_instance"]

        filename = "%s_%ix%sx%i.py" % (kwargs["complexity"], len(kwargs["T"]), kwargs["machines_per_group"], i)
        kwargs["seed"] = random.random() # I think this may not be a good way to do this
        params = create_individual_instance(kwargs=kwargs) 

        filename = filename.replace("[", "")
        filename = filename.replace("]", "")
        filename = filename.replace(",", "_")
        filename = filename.replace(" ", "")

        full_path = "Instances/" + filename
        with open(full_path, "w+") as file:
            file.write("import os\n")
            file.write("import sys\n")
            file.write("sys.path.insert(1, os.path.join(sys.path[0], '..'))\n")
            file.write("from testing import get_random_machine\n\n\n")
            file.write("params = " + str(params) + "\n")     
            for index in range(len(params["machines_per_group"])):
                file.write("\nparams[" + str(index) + "] = get_random_machine(seed = " + str(kwargs["seed"] + index) + ",complexity=\"" + kwargs["complexity"] + "\",params=params)\n" )

def create_individual_instance(kwargs):
    """
    Creates an instance to the machine-scheduling problem.
    """

    seed              = kwargs["seed"]
    T_prime           = kwargs["T"]
    n_machines        = sum(kwargs["machines_per_group"])
    peak_demand       = kwargs["peak_demand"]

    params = get_random_global_parameters(T_prime=T_prime, n_machines=n_machines, seed=seed, linear_relaxation=False, peak_demand=peak_demand)

    params["machines_per_group"] = kwargs["machines_per_group"]
    params["n_groups"] = len(params["machines_per_group"])
    params["N"] = [i for i in range(sum(params["machines_per_group"]))]
    params["T"] = kwargs["T"]

    return params

# Testing

def run_instance(filename, model, heuristic=1, verbose=0, linear_relaxation=False, time_limit=7200):
    """
    Runs an individual instance from the created instance set.

    Default heuristic = 1 is exact pricing. Does not affect compact formulation.
    """

    instance = import_module("Instances." + filename, "")

    params = instance.params
    model = int(model)

    params["filename"]          = filename
    params["model"]             = int(model)
    params["heuristic"]         = int(heuristic)
    params["verbose"]           = int(verbose)
    params["linear_relaxation"] = int(linear_relaxation)
    params["time_limit"]        = int(time_limit)

    if model == 1: # compact
        m = create_model(params=params)
    else:
        m = create_pricer(params=params)
        pricer = m[1]
        m = m[0]

    if not verbose:
        m.hideOutput()

    m.setParam('limits/time', params["time_limit"])
    m.setParam("display/freq", 1)
    params["start_time"] = time() # for correctly stopping the pricing problems

    m.optimize()
    
    m.writeSol(m.getBestSol(),"feas.sol", write_zeros=False)

    if not model == 1 and params["heuristic"] == 2:
        print("%i/%i" % (pricer.data["heuristics"]["success"], pricer.data["heuristics"]["total"]))

    if model == 0:
        if m.getNSols() > 0:
            assert pricer_is_feasible(model=m, params=params)

        n_bugs = m.data["pricer"].data["buggy_heuristic"]
        n_heuristic_calls = m.data["pricer"].data["heuristic_calls"]
        if n_bugs > 0:
            with open("./buggy_instances.txt", "a+") as file:
                file.write("%s %i/%i\n" % (filename, n_bugs, n_heuristic_calls))
    return m

def run_instance_set(**kwargs):

    objval = {}
    time = {}
    gap = {}
    dual = {}
    model = {}

    total_instances = 2*2*2*5
    counter = 0

    for complexity in ["low","high"]:
        for n_years in [10,20]:
            for machines_per_group in ["10_10", "20"]:
                for instance_nr in range(5):
                    filename = "%s_%ix%sx%i" % (complexity, n_years, machines_per_group, instance_nr)

                    print("Running instance: ", filename) 

                    m = run_instance(filename=filename, model=kwargs["model"], verbose=kwargs["verbose"], heuristic=kwargs["heuristic"], time_limit=kwargs["time_limit"]) 

                    if kwargs["statistics"]:

                        model[filename] = m
                        
                        if kwargs["model"] == 1:
                            prefix = "./Results/Compact/"
                        elif kwargs["heuristic"] <= 1:
                            prefix = "./Results/DW/"
                        else:
                            prefix = "./Results/DW_PF/"
                        
                        m.writeStatistics(prefix + "Statistics/"+filename+".stats")
                        
                        if kwargs["model"] == 0:
                            n_cols = m.getNVars()
                        else:
                            n_cols = 0

                        result_file = prefix + "x".join(filename.split("x")[:2]) + ".txt"
                        instance_number = filename.split("x")[2]

                        if instance_nr == 0:
                            with open(result_file, "w") as header: 
                                header.write("N | OPT | Gap(%) | Obj | Dual | N Cols | Time(s)\n")
                                header.write(48*"-" + "\n")

                        with open(result_file, "a") as result_file:

                            if m.getNSols() > 0: # found solution (optimal or suboptimal)
                                objval[filename] = m.getObjVal() 
                                time[filename]   = m.getSolvingTime()
                                dual[filename]   = m.getDualbound()
                                gap[filename]    = m.getGap()*100 if (dual[filename] > 0.001 or objval[filename]==dual[filename]) else 100*objval[filename] # percentage
                                result_file.write("%s | %i | %.2f | %.2f | %.2f | %i | %.2f\n" % (instance_number, m.isZero(gap[filename]), gap[filename], objval[filename], dual[filename], n_cols, time[filename]))
                            else:
                                if m.getStage() != 10 or m.isGT(m.getSolvingTime(), kwargs["time_limit"]): # Timeout
                                    objval[filename] = "-"
                                    gap[filename]    = "-"
                                    time[filename]   = "-"
                                    dual[filename]   = "-" if m.isInfinity(abs(m.getDualbound())) else round(m.getDualbound(),2) 
                                    result_file.write("%s | - | - | - | %s | %i | Timeout\n" % (instance_number, str(dual[filename]), n_cols))
                                else: #infeasible
                                    time[filename]   = m.getSolvingTime()
                                    result_file.write("%s | Infeasible | - | - | - | %i | %.2f\n" % (instance_number, n_cols, time[filename]))
                    
                    counter += 1
                    print("Finished instance %i/%i." % (counter, total_instances))

# Stats

def generate_stats_report(**kwargs):
    """
    Gets model statistics (mean gap and stuff like that)

    trivial:    optimality < 10s
    easy:       optimality < 60s
    medium:     optimality < 300s
    hard:       suboptimal solution at time limit
    impossible: found no solution at time limit
    """

    prefix = ""
    if "model" in kwargs:
        if kwargs["model"] == 1:
            prefix = "./Results/Compact/"
        elif kwargs["heuristic"] <= 1:
            prefix = "./Results/DW/"
        else:
            prefix = "./Results/DW_PF/"

    for model in ["Compact", "DW", "DW_PF"]:
        prefix = "./Results/" + model + "/"
        result_file = prefix + model + "_results"

        total_opt        = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_subopt     = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_infeasible = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_timeout    = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_gap        = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_n_cols     = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_time       = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0} 
        total_dual       = {"impossible": 0}

        for complexity in ["low","high"]:
            for n_years in [10,20]:
                for machines_per_group in ["20","10_10"]:

                    opt     = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    subopt  = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    inf     = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    timeout = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    gap     = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    n_cols  = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    time    = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}   

                    cur_instances = "%s_%ix%sx" % (complexity, n_years, machines_per_group) 
                    directory = prefix + "Statistics/" + cur_instances

                    for i in range(5):
                        filename = directory+str(i)+".stats"
                        result = scip.readStatistics(filename)
                        if result.total_time <= 10:
                            instance_type = "trivial"
                        elif result.total_time <= 60:
                            instance_type = "easy"
                        elif result.total_time < 300:
                            instance_type = "medium"
                        else:
                            if result.n_solutions_found > 0:
                                instance_type = "hard"
                            else:
                                instance_type = "impossible"

                        opt[instance_type]     += (result.status == "optimal")
                        inf[instance_type]     += (result.status == "infeasible")
                        timeout[instance_type] += (result.status == "user_interrupt")

                        assert result.status in ["optimal", "infeasible", "user_interrupt"]

                        if result.gap:
                            gap[instance_type]    += result.gap if result.dual_bound > 0 else result.primal_bound
                        
                        if model != "Compact":
                            n_cols[instance_type] += result.n_presolved_vars

                        time[instance_type]   += result.total_time
                    
                    for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
                        total_opt[instance_type] += opt[instance_type]
                        total_subopt[instance_type] += subopt[instance_type]
                        total_infeasible[instance_type] += inf[instance_type]
                        total_timeout[instance_type] += timeout[instance_type]
                        total_gap[instance_type] += gap[instance_type]
                        total_n_cols[instance_type] += n_cols[instance_type]
                        total_time[instance_type] += time[instance_type]
                
        with open(result_file, "w+") as file:
            for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
                file.write(instance_type+"\n")

                file.write("Total optimal: %i\n" % (total_opt[instance_type]))
                file.write("Total suboptimal: %i\n" % (total_subopt[instance_type]))
                file.write("Total timeout: %i\n" % (total_timeout[instance_type]))
                file.write("Total infeasible: %i\n" % total_infeasible[instance_type])
                file.write("Total gap: %.2f%%\n" % total_gap[instance_type])
                if model != "Compact":
                    file.write("Total n_cols: %i\n" % total_n_cols[instance_type])
                file.write("Total time: %.2f\n" % total_time[instance_type])
                file.write("\n")
        
    return

if __name__ == "__main__":
    
    # To create the instances in the Instance folder.
    # n_instances = 5
    # set_creation_seed = 1
    # for T in [10,20]:
    #     for complexity in ["low", "high"]:
    #         for machines_per_group in ["[20]","[10,10]"]:
    #             create_instance_set(T = T, complexity=complexity, machines_per_group=machines_per_group, n_instances=n_instances, set_seed=set_creation_seed, peak_demand=False)
    #             set_creation_seed += 1

    # run instance set and generate result files
    #run_instance_set(model=0, heuristic=2, verbose=1, statistics=True, time_limit = 300)
    generate_stats_report()
    
    # create individual instance
    #create_instance_set(T = 12, complexity="low", machines_per_group = "[60]", n_instances = 1, set_seed=0, peak_demand=False, specific_instance=None)
    
    # run individual instance
    #run_instance("low_20x20x1", model = 0, heuristic=1, verbose=2, linear_relaxation=False, time_limit=300) # useful for problematic instances