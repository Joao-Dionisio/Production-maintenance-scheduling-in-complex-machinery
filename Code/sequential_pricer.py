# pyright: reportPossiblyUnboundVariable=false
from pyscipopt import Model, Pricer, SCIP_RESULT, SCIP_PARAMSETTING, SCIP_PARAMEMPHASIS, Variable, Constraint, quicksum
from pyscipopt.recipes.getLocalConss import getLocalConss
from parameters import *

# Master
from master_problem import master_model
from create_model import create_model # Pricing is done here as well

# Pricing
from generate_initial_pricing_columns import PFHeuristic, _eval
from copy import copy

# Branching
from pricing_branching import PricingBranchingAggregateVarbound, PricingBranchingDisaggregate, PricingEventHdlr
from pricing_branching import BranchingDecision

# Misc
from time import time
from statistics import fmean # dual stabilization
from testing import log_error # writting errors to file
from collections import defaultdict
import numpy as np
import ast # to convert dict as string into dict
import math
from typing import Any, Dict, Union, cast, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Magic numbers
MAX_SUBPROB_SIZE_FOR_COMPACT_INITIALIZATION = 20000
COMPACT_MODEL_TIME_LIMIT     = 30
COMPACT_MODEL_RUN_FREQUENCY  = 10000
N_HEURISTIC_TRIES            = 10
AGE_CUTOFF                   = 20 # for cleaning old columns
IRMP_COOLDOWN_DEFAULT        = 3 # minimum number of nodes between IRMP solves (as sometimes it solves too often)
FAILED_IRMP_PENALTY_FACTOR   = 0.3 # ratio of new columns needed before re-atempting Price-and-Branch
MAX_STRAIGHT_0_SUBPROBS      = 50 # to make use of new deltas for column domination
MAX_STRAIGHT_1_SUBPROBS      = 10

# Dual stabilization
INITIAL_ALPHA        = 0.1
MAX_ALPHA            = 0.7
ALPHA_RATE_OF_CHANGE = 1.2

# Print iteration info
COL1_WIDTH  = 15
COL2_WIDTH  = 15
COL3_WIDTH  = 15
COL4_WIDTH  = 15
COL5_WIDTH  = 15
COL6_WIDTH  = 15
COL7_WIDTH  = 15
COL8_WIDTH  = 15
COL9_WIDTH  = 15
COL10_WIDTH = 15
HEADER_FREQUENCY = 20

# From a different project. Here just to ensure the code runs
given_delta = None
given_mu = None

def gini(array):
    """
    Helper function to normalize the huge values of farkas pricing
    """
    array = np.array(array)
    array = array.flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)  # values cannot be negative
    array += 1e-10  # avoid division by zero
    array = np.sort(array)
    n = array.size
    index = np.arange(1, n+1)
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

def round_up(number, decimals=5):
    factor = 10 ** decimals
    return math.ceil(number * factor) / factor

class CutPricer(Pricer):

    data: Dict[str, Any]
    def __init__(self, n_subprobs):        
        super().__init__()
        self.optimal_cols               = 0
        self.heuristic_cols             = 0
        self.optimal_time               = 0
        self.heuristic_time             = 0
        self.prev_node_nvars            = 0
        self.ncols_required_for_imp_opt = 0
        self.n_delta                    = 0
        self.n_mu                       = 0
        self.n_subprobs                 = n_subprobs

        self.min_redcost                = {"delta": [0 for _ in range(n_subprobs)],
                                           "mu": [0 for _ in range(n_subprobs)],
                                           "full_col": [0 for _ in range(n_subprobs)]}

        self.redcosts:               Dict[int, float] = {i: 0 for i in range(n_subprobs)}    
        self.stabilized_duals:       Dict[str, list]  = {}
        self.explored_subproblems:   Dict[int, int]   = {}
        self.data:                   Dict[Any, Any]   = {}
        self.break_early:            Dict[int, Any]   = {}
        self.applied_redcost_fixing: Dict[int, Any]   = {}
        self.seen_duals:             list             = []
        self.alpha:                  float            = INITIAL_ALPHA # dict[int, float] = {i: INITIAL_ALPHA for i in range(n_subprobs)}
        self.irmp_cooldown:          int              = 0
        self.force_negative_redcost: bool             = False

    # The initialisation function for the variable pricer to retrieve the transformed constraints of the problem
    def pricerinit(self):
        try:
            return self._pricerinit()
        except Exception as e:
            log_error("pricerinit", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}
    
    def _pricerinit(self):
        self.redcost_iteration = 0
        self.farkas_iteration = 0
        self.feastol     = self.model.getParam("numerics/feastol") 
        self.dualfeastol = self.model.getParam("numerics/dualfeastol")

        self.duals = {"convexity": {}, "production": {}, "branching": {0:[]}}
        for con_type in ["convexity_cons", "demand_cons"]:
            for i, c in enumerate(self.data[con_type]):
                self.data[con_type][i] = self.model.getTransformedCons(c)

        cur_node_number = 1
        self.data["branching_cons"][cur_node_number] = {i: {} for i in range(self.n_subprobs)}
        for subprob in range(self.n_subprobs):
            for i, c in enumerate(self.data["branching_cons"][cur_node_number][subprob]): # should be empty
                self.data["branching_cons"][cur_node_number][subprob][i] = self.model.getTransformedCons(c)

        if self.data["params"]["debug_mode"]:
            self.duals = {
                "convexity": {i:[] for i in range(self.n_subprobs)},
                "demand": {t:[] for t in self.data["params"]["T_prime"]},
            }

        self.misprice = {i: 0 for i in range(self.n_subprobs)}

    def run_compact(self):
        try:
            return self._run_compact()
        except Exception as e:
            log_error("run_compact", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    def debug_print_dualSolutions(self,
                                  dualSolutions: Dict[str, Any],
                                  *,
                                  decimals: int = 7,
                                  title: Optional[str] = None) -> None:
        """
        Pretty-print the full dualSolutions dictionary (all subproblems and nodes).

        Call this right after retrieving duals, e.g.:
            ds = self.collect_dual_values()
            self.debug_print_dualSolutions(ds)

        Sections printed:
        - convexity_cons: list over subproblems
        - demand_cons: list over time periods
        - compatibility_cons: per subproblem, all entries
        - branching_cons: per node, per subproblem, all entries
        """
        try:
            def fmt(v: float) -> str:
                try:
                    return f"{float(v):.{decimals}f}"
                except Exception:
                    return str(v)

            if not isinstance(dualSolutions, dict) or not dualSolutions:
                print("[debug_print_dualSolutions] No dualSolutions to print.")
                return

            header = title if title else "DualSolutions snapshot"
            print(f"\n==== {header} ====\n")
            node_info = f" | node: {getattr(self, 'cur_node_number', '?')}" if hasattr(self, 'cur_node_number') else ""
            print(f"farkas: {getattr(self, 'farkas', False)}{node_info}")

            # Convexity
            conv = dualSolutions.get("convexity_cons", [])
            if isinstance(conv, (list, tuple)) and conv:
                print("\n[convexity_cons]")
                for i, val in enumerate(conv):
                    print(f"  subprob {i:>3}: {fmt(val)}")

            # Demand
            dem = dualSolutions.get("demand_cons", [])
            if isinstance(dem, (list, tuple)) and dem:
                print("\n[demand_cons]")
                for t, val in enumerate(dem):
                    print(f"  t={t:>3}: {fmt(val)}")

            # Compatibility (ARMP)
            comp = dualSolutions.get("compatibility_cons", {})
            if isinstance(comp, dict) and comp:
                print("\n[compatibility_cons]")
                for sp, items in comp.items():
                    if not items:
                        continue
                    print(f"  subprob {sp}:")
                    # Show sorted by descending |value|
                    try:
                        sorted_items = sorted(items.items(), key=lambda kv: abs(kv[1]), reverse=True)
                    except Exception:
                        sorted_items = list(items.items())
                    for k, v in sorted_items:
                        print(f"    eta[{k}] = {fmt(v)}")

            # Branching
            br = dualSolutions.get("branching_cons", {})
            if isinstance(br, dict) and br:
                print("\n[branching_cons]")
                for node, sub_map in br.items():
                    if not isinstance(sub_map, dict) or not sub_map:
                        continue
                    for sp, entries in sub_map.items():
                        if not entries:
                            continue
                        print(f"  node {node}, subprob {sp}:")
                        for idx, v in entries.items():
                            print(f"    gamma[{idx}] = {fmt(v)}")

            print("\n=======================\n")
        except Exception as e:
            print(f"[debug_print_dualSolutions] Exception while printing dualSolutions: {e}")
    
    def _run_compact(self):
        if not self.data["compact_model"]["model"]:
            self.data["compact_model"]["model"] = create_model(params=self.data["params"], pricing_formulation=-2)
            self.data["compact_model"]["model"].setObjective(0) # only care about feasibility
            self.data["compact_model"]["model"].setParam("limits/solutions", 1)
            if self.data["params"]["verbose"] >= 2:
                print("Starting compact model run")

            if self.data["params"]["verbose"] <= 3:
                self.data["compact_model"]["model"].hideOutput()
            
            self.data["compact_model"]["model"].setEmphasis(SCIP_PARAMEMPHASIS.FEASIBILITY)        

        self.data["compact_model"]["time"] += COMPACT_MODEL_TIME_LIMIT
        self.data["compact_model"]["n_solutions"] += 1
        self.data["compact_model"]["model"].setParam("limits/time", self.data["compact_model"]["time"])
        self.data["compact_model"]["model"].setParam("limits/solutions", self.data["compact_model"]["n_solutions"])

        self.data["compact_model"]["model"].optimize()

        status = self.data["compact_model"]["model"].getStatus()
        if status in ["timelimit", "infeasible", "unbounded"]:
            return {"status": status}

        self.add_columns_from_compact(self.data["compact_model"]["model"])
        return {"status": status}
    
    def add_columns_from_compact(self, compact_model):
        
        self.compact_found_sol = True

        # Initialize data structures with correct nesting
        delta_patterns = {i: [{} for _ in range(self.data["params"]["machines_per_group"][i])] for i in range(self.n_subprobs)}
        mu_patterns    = {i: [{} for _ in range(self.data["params"]["machines_per_group"][i])] for i in range(self.n_subprobs)}
        vars           = {i: [{} for _ in range(self.data["params"]["machines_per_group"][i])] for i in range(self.n_subprobs)}

         # Determine pricing formulation based on model
        if self.data["model"] == 0:
            pricing_formulation = -1
        elif self.data["model"] == 2:
            pricing_formulation = 2
        else:
            raise ValueError("Invalid model")

        # Create mapping from individual machine index to (subprob, position within subprob)
        machine_map = {}
        machine_idx = 0
        for subprob, num_machines in enumerate(self.data["params"]["machines_per_group"]):
            for pos in range(num_machines):
                machine_map[machine_idx] = (subprob, pos)
                machine_idx += 1
        
        # Process all variables from compact model
        for var in compact_model.getVars():
            var_name = var.name

            split_var = var_name.split(",")
            if len(split_var) >= 2:
                # Extract original format: "m[machine_idx,component,period]"
                machine_idx = int(split_var[0].split("[")[1])
                subprob, pos = machine_map[machine_idx]
                var_prefix = var_name.split("[")[0]
                component_period = ",".join(split_var[1:])
                var_name = f"{var_prefix}[0,{component_period}"
            else:
                machine_idx = int(var_name.split("[")[1][:-1])
                subprob, pos = machine_map[machine_idx]
                var_name = var_name.split("[")[0] + "[0]"

            var_val = compact_model.getVal(expr=var)
            if self.data["model"] == 0:
                vars[subprob][pos][var_name] = var_val
            else:
                if var_name.startswith("m["):
                    delta_patterns[subprob][pos][var_name] = var_val
                elif var_name.startswith("y["):
                    mu_patterns[subprob][pos][var_name] = var_val
                else:
                    continue

        var_dict = compact_model.getVarDict()
        for machine_idx in machine_map:
            subprob, pos = machine_map[machine_idx]
            maintenance_cost = var_dict["machine_maintenance[%i]"%machine_idx]
            delta_patterns[subprob][pos]["total_cost"]       = maintenance_cost
            vars[subprob][pos]["total_cost"]                 = maintenance_cost
            delta_patterns[subprob][pos]["maintenance_cost"] = maintenance_cost # todo: standardize this, they're the same
            vars[subprob][pos]["maintenance_cost"]           = maintenance_cost
        
        added_vars = {}
        # Add columns to RMP for each subproblem
        for subprob in range(self.n_subprobs):
            # Create result object with required structure
            result = {
                "objval": [-1]*len(vars[subprob]),  # Force addition of column
                "vars": vars[subprob],
                "mu_patterns": mu_patterns[subprob],
                "delta_patterns": delta_patterns[subprob],
                "maintenance_cost": [delta["maintenance_cost"] for delta in delta_patterns[subprob]],
                "fixed_redcost_contribution": 0,
                "pricing_formulation": pricing_formulation,
                "compact_run": True
            }
            
            self.found_negative_redcost = True

            # Add columns to the RMP
            added_vars[subprob] = self.add_column_to_RMP(result=result, subprob=subprob)
        
        return

    def compact_status_to_scip_result(self, status):
        if status == "infeasible":
            return {"result": SCIP_RESULT.INFEASIBLE}
        elif status == "optimal":
            return {"result": SCIP_RESULT.SUCCESS}
        elif status == "sollimit":
            return {"result": SCIP_RESULT.SUCCESS}
        elif status == "timelimit":
            return {"result": SCIP_RESULT.DIDNOTRUN}
        else:
            raise ValueError("Unknown result from compact model")

    # Farkas pricing to fix infeasibilities and get initial columns
    def pricerfarkas(self):
        try:
            return self._pricerfarkas()
        except Exception as e:
            log_error("pricerfarkas", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}
    
    def _pricerfarkas(self):
        if self.initialize_with_compact and not self.compact_found_sol:
            result = self.run_compact()
            self.initialize_with_compact = False
            if result["status"] != "timelimit":
                return self.compact_status_to_scip_result(result["status"])

        self.farkas = True
        self.farkas_iteration += 1
        self.found_negative_redcost=False
        self.cur_node = self.model.getCurrentNode()
        self.cur_node_number = self.cur_node.getNumber()

        # setting lowerbound of 0, just for better visualization
        self.model.updateNodeLowerbound(self.cur_node, 0)

        return self.pricer_main()

    # The reduced cost function for the variable pricer
    def pricerredcost(self):
        try:
            return self._pricerredcost()
        except Exception as e:
            log_error("pricerredcost", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}
    
    def _pricerredcost(self):

        self.cur_node = self.model.getCurrentNode()
        self.cur_node_number = self.cur_node.getNumber()

        # node should have already been cutoff in branching, but just to be sage.
        if self.model.isGE(self.model.getLPObjVal(), self.best_sol["obj"]):
            self.model.cutoffNode(self.cur_node)
            return {"result": SCIP_RESULT.SUCCESS}
        
        # for some reason, in ARMP, SCIP sometimes continues optimizing after finding the optimal solution
        if not self.model.isInfinity(self.model.getPrimalbound()) and self.model.isGE(self.model.getLPObjVal(), self.model.getPrimalbound()):
            self.model.cutoffNode(self.cur_node)
            return {"result": SCIP_RESULT.SUCCESS}

        self.farkas = False
        self.redcost_iteration += 1
        self.found_negative_redcost=False
        no_sols_found = self.model.getNSols() == 0 and not self.compact_found_sol 
        if no_sols_found and self.redcost_iteration % COMPACT_MODEL_RUN_FREQUENCY == 0:
            if self.data["params"]["verbose"] >= 2:
                print("\n Running compact model in feasibility mode to get initial solution.\n")
            result = self.run_compact()
            if result:
                return self.compact_status_to_scip_result(result["status"])

        self.data["explored_subprobs"] = [0 for _ in range(self.n_subprobs)] # because of lagrangian bound, can only set it whenever we have dual bounds for every subproblem
        if not self.model.isInfinity(-self.model.getLPObjVal()):
            self.lagrangian_bound = self.model.getLPObjVal()
        else:
            self.lagrangian_bound = -float("inf")

        return self.pricer_main()

    # Main pricing function
    def pricer_main(self):
        """
        Main routine for the pricing step in a branch-and-price algorithm.
        This method orchestrates the pricing process for the current node in the branch-and-bound tree.
        It handles several tasks including:
        - Timing and bookkeeping for pricing and master problem solution.
        - Checking if the current node should be closed due to integrality or other criteria.
        - Updating primal bounds and storing best solutions found.
        - Adding columns to the Restricted Master Problem (RMP) based on repaired variables or implicit integer solutions.
        - Collecting dual solutions and applying dual stabilization if required.
        - Sorting subproblems for heuristic pricing and running heuristic routines.
        - Running the exact pricing loop to find columns with negative reduced cost.
        - Cleaning up inactive columns from the RMP.
        - Handling integer RMP runs and updating lower bounds.
        - Applying reduced cost fixing if enabled.
        - Printing iteration information for debugging and verbose output.
        Returns:
            dict: A dictionary containing the result of the pricing step and other relevant information,
                  such as objective value, variables added, and status flags.
        """

        # early branching is often decided after adding variables, so we need to enforce it at the beginning of the next iteration.
        if self.cur_node_number in self.data["early_branch"]:
            self.optimize_integer_master_problem() # because this is not called when early branching (as there are negative redcost cols)

            if self.data["params"]["verbose"] >= 3:
                print("Branch early.")

            return {"result": SCIP_RESULT.DIDNOTRUN}

        start = time()
        # Attribute master (SCIP) time since the end of the last callback up to the start of pricing
        last_end = self.data.get("last_callback_end", self.data.get("master_start_time", start))
        self.data["master_time"] += max(0.0, start - last_end)
        self.data["begin_pricing_time"] = start

        heuristic_time = 0.0
        exact_time = 0.0
        integer_rmp_time = 0.0
        self.data["old_lambdas"] = 0
        self.data["removed_deltas"] = 0
        self.data["removed_mus"] = 0
        self.data["old_deltas"] = 0
        self.data["old_mus"] = 0

        if self.cur_node_number in self.data["closed_nodes"]:
            now = time()
            self.data["end_pricing_time"] = now
            # Update unified callback anchor
            self.data["last_callback_end"] = now
            return {"result": SCIP_RESULT.SUCCESS}

        self.found_negative_redcost = False # just resetting in case no repaired variables

        # collecting dual or farkas dual solutions
        dualSolutions, dualSolsWithNames = self.collect_dual_values()
        self.data["dualSolutions"] = dualSolutions
        self.data["dualSolsWithNames"] = dualSolsWithNames

        if self.data["params"]["dual_stabilization"] and not self.farkas:
            dualSolutions = self.get_stabilized_duals()

        # sorting subproblems by heuristic result
        if self.n_subprobs > 1 or self.data["params"]["heuristic"] > 1:
            if self.data["params"]["heuristic"] == -1 or self.redcost_iteration % 50 == 0:
                self.ordered_subprobs = [i for i in range(self.n_subprobs)]
            else:
                heuristic_start = time()
                if self.data["model"] == 2:
                    # result = self.sort_subproblems(dualSolutions=dualSolutions)
                    result = {} # DEBUG: eval is not working properly, careful!! # self.sort_subproblems(dualSolutions=dualSolutions)
                else:
                    result = self.sort_subproblems(dualSolutions=dualSolutions)
                heuristic_time = time() - heuristic_start
                self.data["heuristic_time"] += heuristic_time

                if "result" in result and result["result"] == SCIP_RESULT.DIDNOTRUN:
                    now = time()
                    self.data["end_pricing_time"] = now
                    self.data["last_callback_end"] = now
                    return result

                # found negative redcost or pricing timeout
                if result and self.data["params"]["heuristic"] == 2:
                    assert 'result' in result and result['result'] in [SCIP_RESULT.SUCCESS, SCIP_RESULT.DIDNOTRUN]

        if self.data["params"]["heuristic"] == 2 and self.found_negative_redcost:
            if self.data["params"]["verbose"] >= 2:
                self.print_iteration_info(result)

            self.data["python_time"] += max(0.0, (time() - start - heuristic_time - exact_time - integer_rmp_time))
            now = time()
            self.data["end_pricing_time"] = now
            self.data["last_callback_end"] = now
            return {"result": SCIP_RESULT.SUCCESS}

        # main (exact) solving loop
        exact_start = time()
        all_results = self.exact_solving_loop(dualSolutions=dualSolutions)
        exact_time = time() - exact_start
        self.data["exact_pricing_time"] += exact_time

        if self.data["params"]["verbose"] >= 2:
            if self.data["params"]["model"] == 0:
                if self.data["old_lambdas"]:
                    print("Removed %i lambda due to inactivity."%(self.data["old_lambdas"]))
            elif self.data["params"]["model"] == 2:
                if self.data["removed_deltas"] or self.data["removed_mus"]:
                    print("Transfered %i mu variables and removed %i delta due to domination."%(self.data["removed_mus"], self.data["removed_deltas"]))
                if self.data["old_deltas"] or self.data["old_mus"]:
                    print("Removed %i delta and %i mu variables due to inactivity."%(self.data["old_deltas"], self.data["old_mus"]))

        integer_rmp_start = time()
        self.ran_integer_rmp = False
        scip_dict = self.get_final_scip_dict(all_results)

        if self.data["model"] == 2:
            scip_dict["pricing_formulation"] = all_results.get(0, {}).get("pricing_formulation")

            if scip_dict["pricing_formulation"] != 2:
                scip_dict["lowerbound"] = 0 # todo: think about lowerbounds in the event of the other pricing problems.

        if self.ran_integer_rmp:
            integer_rmp_time = time() - integer_rmp_start
            self.data["integer_rmp_time"] += integer_rmp_time
        
        if "lowerbound" in scip_dict:
            if self.model.isInfinity(scip_dict["lowerbound"]):
                del scip_dict["lowerbound"]
            elif self.model.isGE(scip_dict["lowerbound"], self.primal_bound): # solutions from integer_rmp are not known to the model after root
                self.model.cutoffNode(self.model.getCurrentNode())

        if self.data["params"]["verbose"] >= 2:
            self.print_iteration_info(scip_dict)

        self.data["python_time"] += max(0.0, (time() - start - exact_time - heuristic_time - integer_rmp_time))
        now = time()
        self.data["end_pricing_time"] = now
        self.data["last_callback_end"] = now

        return scip_dict

    # Getting dual values
    def _collect_dual_values(self):
        try:
            return self.collect_dual_values()
        except Exception as e:
            log_error("collect_dual_values", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    def collect_dual_values(self) -> dict:
        """
        Collects dual values from the Restricted Master Problem (RMP) for various constraint types.
        Constraint types handled:
            - Convexity constraints ("convexity_cons")
            - Demand constraints ("demand_cons")
            - Compatibility constraints ("compatibility_cons", ARMP only)
            - Branching constraints ("branching_cons")
        For each constraint type, retrieves dual values using either Farkas duals or standard duals,
        depending on the `self.farkas` flag. Compatibility and branching constraints are handled
        with additional indexing for subproblems and branching decisions.
        If debug mode is enabled, stores dual values for convexity and demand constraints for further analysis.
        Returns:
            dict: A dictionary containing dual values for each constraint type, structured as follows:
                {
                    "convexity_cons": list of duals,
                    "demand_cons": list of duals,
                    "compatibility_cons": dict of dicts of duals,
                    "branching_cons": dict of dicts of dicts of duals
                }
        """

        dualSolutions = {}
        dualSolsWithNames = {}
        for con_type in ["convexity_cons", "demand_cons"]:
            dualSolutions[con_type] = []
            if self.farkas:
                for c in self.data[con_type]:
                    dualSolutions[con_type].append(self.model.getDualfarkasLinear(c))
                    dualSolsWithNames[c.name] = dualSolutions[con_type][-1]
            else:
                for c in self.data[con_type]:
                    dualSolutions[con_type].append(self.model.getDualSolVal(c))
                    dualSolsWithNames[c.name] = dualSolutions[con_type][-1]

        dualSolutions["compatibility_cons"] = {i:{} for i in range(self.data["params"]["n_groups"])}
        for subprob in self.data["compatibility_cons"]: # ARMP only
            if self.farkas:
                for cur_delta in self.data["compatibility_cons"][subprob]:
                    cur_cons = self.data["compatibility_cons"][subprob][cur_delta]
                    dualSolutions["compatibility_cons"][subprob][cur_delta] = self.model.getDualfarkasLinear(cur_cons)
                    dualSolsWithNames[cur_cons.name] = dualSolutions["compatibility_cons"][subprob][cur_delta]
            else:
                for cur_delta in self.data["compatibility_cons"][subprob]:
                    cur_cons = self.data["compatibility_cons"][subprob][cur_delta]
                    dualSolutions["compatibility_cons"][subprob][cur_delta] = self.model.getDualSolVal(cur_cons)
                    dualSolsWithNames[cur_cons.name] = dualSolutions["compatibility_cons"][subprob][cur_delta]

        # getting branching dual values
        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()

        dualSolutions["branching_cons"] = {}
        dualSolutions["branching_cons"][cur_node_number] = {i: {} for i in range(self.n_subprobs)}
        if self.farkas:
            for subprob in range(self.n_subprobs):
                dualSolutions["branching_cons"][cur_node_number][subprob] = {}
                for branching_index in range(len(self.data["branching_decisions"][cur_node_number][subprob])):
                    c = self.data["branching_decisions"][cur_node_number][subprob][branching_index].branching_con
                    dualSolutions["branching_cons"][cur_node_number][subprob][branching_index] = self.model.getDualfarkasLinear(c)
                    dualSolsWithNames[c.name] = dualSolutions["branching_cons"][cur_node_number][subprob][branching_index]
        else:
            for subprob in range(self.n_subprobs):
                dualSolutions["branching_cons"][cur_node_number][subprob] = {}
                for branching_index in range(len(self.data["branching_decisions"][cur_node_number][subprob])): # todo add check for aggregatemvarbound
                    c = self.data["branching_decisions"][cur_node_number][subprob][branching_index].branching_con
                    dualSolutions["branching_cons"][cur_node_number][subprob][branching_index] = self.model.getDualSolVal(c)
                    dualSolsWithNames[c.name] = dualSolutions["branching_cons"][cur_node_number][subprob][branching_index]

        if self.data["params"]["debug_mode"]:
            if not self.farkas:
                for subprob in range(self.n_subprobs):
                    self.duals["convexity"][subprob].append(dualSolutions["convexity_cons"][subprob])
                for t in self.data["params"]["T_prime"]:
                    self.duals["demand"][t].append(dualSolutions["demand_cons"][t-1])

        if self.data["params"]["debug_mode"] and self.data["params"]["verbose"] >= 4:
            self.debug_print_dualSolutions(dualSolutions, title=f"Collected dualSolutions at node {cur_node_number}")

        return dualSolutions, dualSolsWithNames

    # Sorting subprobs for exact solve
    def sort_subproblems(self, dualSolutions):
        try:
            return self._sort_subproblems(dualSolutions)
        except Exception as e:
            log_error("sort_subproblems", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    # Sorting subprobs for exact solve
    def _sort_subproblems(self, dualSolutions) -> dict:
        """
        Runs fast heuristics on the subproblems to determine the order in which they should be exactly solved

        Note: If params["heuristics"] > 1 negative recost columns will be added, and pricing will finish 
        """

        self.ordered_subprobs = []

        # If there are negative reduced cost heuristics, great. Otherwise sort the subproblems by heuristic result and then solve them.
        heuristic_results = [] 
        best_heur_result  = float("inf")

        given_delta = None # for initialization purposes
        if self.data["model"] == 0:
            pricing_formulation = -1
        elif self.data["model"] == 2:
            if self.farkas:
                pricing_formulation = 2 # maybe don't need to do full pricing every time during farkas
            else:
                pricing_formulation = 0
        else:
            raise ValueError("Invalid model number")

        # parallelize this when doing alternative master
        for subprob in range(self.n_subprobs): 

            # no need to order subproblems if there is only 1
            if self.data["params"]["heuristic"] == 1 and self.n_subprobs == 1:
                break

            if pricing_formulation == 2:
                break
            
            if pricing_formulation != 0:
                fixed_redcost_contribution = dualSolutions["convexity_cons"][subprob]
            else:
                fixed_redcost_contribution = 0

            for given_delta in self.data["Delta"][subprob]: 
                if self.data["model"] == 0: # original
                    result = self.solve_pricing(subprob, reopt=self.data["params"]["reopt"], heuristic=2, pricing_formulation=-1, dualSolutions=dualSolutions, given_delta=None, given_mu=None)
                elif self.data["model"] == 2: # alternative
                    result = self.solve_pricing(dualSolutions=dualSolutions, reopt=self.data["params"]["reopt"], subprob=subprob, pricing_formulation=pricing_formulation, heuristic=1, given_delta=given_delta, given_mu=None)
                else:
                    raise ValueError("Invalid model number")

                if self.model.isGT(self.model.getTotalTime(), self.data["params"]["time_limit"]):
                    return {"result": SCIP_RESULT.DIDNOTRUN}
                elif 'result' in result:
                    if result["result"] == SCIP_RESULT.INFEASIBLE: # if one subproblem is infeasible, whole problem is
                        return result
                    elif result["result"] == SCIP_RESULT.DIDNOTFIND:
                        # heuristic_results.append((result["objval"][0], subprob))
                        best_heur_result = min(best_heur_result, result["objval"][0] - fixed_redcost_contribution)
                        continue

                objval = result["objval"]

                # if column is good and we want heuristic columns (if not, we still use the result for subproblem sorting)
                # preventing optimal solve only if heuristic column is good enough
                if self.data["params"]["heuristic"] > 1 and self.model.isLT(objval[0] - fixed_redcost_contribution, -0.1):
                    self.found_negative_redcost = True

                    self.add_column_to_RMP(result=result, subprob=subprob, given_delta=given_delta, heuristic=True)

                best_heur_result = min(best_heur_result, objval[0] - fixed_redcost_contribution) # heuristic only gets 1 sol, hence objval[0]

            heuristic_results.append((best_heur_result, subprob)) # because we may want to order subprobs by their objval

        # Getting subproblem order because we might still want to exact solve
        if heuristic_results:
            heuristic_results.sort(key=lambda x: x[0] * self.data["params"]["machines_per_group"][x[1]])
            ordered_subprobs = [heuristic_results[i][1] for i in range(len(heuristic_results))] # heuristic tells us which subprob to go for
        else:
            ordered_subprobs = [i for i in range(self.n_subprobs)] # heuristics found zero solutions

        # Getting past redcosts of subproblems to decide order
        if not heuristic_results and self.redcost_iteration >= 10:
            ordered_subprobs = sorted([i for i in range(self.n_subprobs)], key = lambda subprob: sum(self.data["previous_redcosts"][subprob][-5:]))
            if self.data["straight_subprobs"][1] >= 10 and self.data["straight_subprobs"][0] == ordered_subprobs[0]:
                ordered_subprobs.append(ordered_subprobs.pop(0)) # moving the subprob to the end 
                self.data["straight_subprobs"] = [ordered_subprobs[0], 0] # resetting the count

        if not ordered_subprobs and not self.found_negative_redcost:
            self.ordered_subprobs = [i for i in range(self.n_subprobs)]
        else:
            self.ordered_subprobs = ordered_subprobs

        if self.found_negative_redcost and self.data["params"]["heuristic"] == 2:
            return {"result": SCIP_RESULT.SUCCESS, "heuristic": True, "objval": best_heur_result}

        return {}

    # ORIG and ARMP exact solving loop
    def exact_solving_loop(self, dualSolutions):
        try:
            return self._exact_solving_loop(dualSolutions)
        except Exception as e:
            log_error("exact_solving_loop", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    # ORIG and ARMP exact solving loop
    def _exact_solving_loop(self, dualSolutions) -> dict:
        """
        Executes the exact solving loop for all ordered subproblems using the provided dual solutions.

        This method iterates over each subproblem in `self.ordered_subprobs` and solves its pricing problem
        using either the original or alternative master problem formulation. For each subproblem:
        - Calls `solve_pricing` (for model 0) or `ARMP_exact_solving_loop` (for model 2).
        - Stores the result for each subproblem in `all_results`.
        - Updates the iteration count since last solve for each subproblem.
        - Handles special cases:
            - If a subproblem times out (`SCIP_RESULT.DIDNOTRUN`), returns immediately.
            - If a subproblem is infeasible (`SCIP_RESULT.INFEASIBLE`), returns immediately.
            - If no negative reduced cost is found, updates previous redcosts and continues.
        - If a negative reduced cost column is found, adds it to the RMP.
        - Implements logic to avoid exploring the same subproblem too often.
        - May break early if better duals are needed.

        After all subproblems are processed, sets the overall result to `SCIP_RESULT.SUCCESS` and returns `all_results`.

        Args:
            dualSolutions: Dictionary of dual values for the current node.

        Returns:
            dict: A dictionary containing the results for each subproblem and the overall status.
        """
        if self.data["params"]["model"] == 0:
            assert len(self.ordered_subprobs) == self.n_subprobs, "Problem with subprob ordering"
        
        # todo: eventually have all deltas in a priority queue, even across subprobs.
        # elif self.data["params"]["model"] == 2:
        #     assert len(self.ordered_subprobs) == sum([len(self.data["Delta"][subprob]) for subprob in self.ordered_subprobs]), "Problem with subprob ordering"

        all_results = {} # in case of multiple subproblems
        result = {}
        for subprob in self.ordered_subprobs:
            if self.data["model"] == 0:
                result = self.solve_pricing(subprob=subprob, reopt=self.data["params"]["reopt"], heuristic=1, dualSolutions=dualSolutions, pricing_formulation=-1, given_delta=None, given_mu=None)
            else:
                raise ValueError("Invalid model number.")

            all_results[subprob] = result

            # resetting the last time since subprob was solved
            self.data["iterations_since_last"][subprob] = 0
            if "result" in result: 
                if result["result"] == SCIP_RESULT.DIDNOTRUN: # timeout in the middle of pricing
                    return {"result": SCIP_RESULT.DIDNOTRUN}
                elif result["result"] == SCIP_RESULT.INFEASIBLE:
                    return {"result": SCIP_RESULT.INFEASIBLE} # subproblem is infeasible, thus node is infeasible # not true if subproblem is infeasible bc of setObjlimit
                else: # no negative reduced cost
                    self.data["previous_redcosts"][subprob].append(10)
                    continue

            self.data["previous_redcosts"][subprob].append(result["objval"][0])

            # no negative redcost
            if self.force_negative_redcost:
                self.force_negative_redcost = False # in PP1 we sometimes get better deltas that don't yet have decent mu's. might still be worth it to add them
            else:
                if 'result' in result or self.model.isGE(result["objval"][0],0):
                    continue

            self.found_negative_redcost = True
            self.add_column_to_RMP(result=result, subprob=subprob, given_delta=given_delta, heuristic=False) 

            # to avoid exploring the same subproblem too much
            # capping number of straight iterations in this subprob
            if subprob == self.data["straight_subprobs"][0]:
                self.data["straight_subprobs"][1] += 1 
            else:
                self.data["straight_subprobs"] = [subprob, 1]

            # breaking is broken?
            if self.break_for_better_duals(subprob=subprob):
                break

        all_results['result'] = SCIP_RESULT.SUCCESS
        return all_results

    def print_iteration_info(self, result):
        """
        Prints formatted information about the current iteration of the pricing algorithm, including node statistics,
        bounds, gap, reduced cost, and timing. The output adapts to the model type and whether the Farkas pricing is used.

        Args:
            result (dict): Dictionary containing results for the current iteration. Expected keys include:
                - "objval" (float, optional): Reduced cost value.
                - "result" (float, optional): Alternative reduced cost value if "objval" is not present.
                - "dualbound" (float, optional): Local dual bound for the current node.
                - "heuristic" (bool, optional): Indicates if the solution was found by a heuristic.
                - "pricing_formulation" (str, optional): Identifier for the pricing formulation used.

        Prints:
            A formatted table row with the following columns (depending on model type):
                - Current node number
                - Number of open nodes
                - Iteration or formulation|iteration
                - Reduced cost (with heuristic marker if applicable)
                - Gap percentage
                - Primal bound
                - Global dual bound
                - Local dual bound
                - Solving time (seconds)
        """

        # Print header
        if self.farkas and self.farkas_iteration % HEADER_FREQUENCY == 1:
            print()
            if self.data["model"] == 2:
                print(f"{'Time':^{COL1_WIDTH}}{'Cur Node':^{COL2_WIDTH}}{'Open Nodes':^{COL3_WIDTH}}{'Formulation|Iter':^{COL4_WIDTH}}{'Redcost':^{COL5_WIDTH}}{'Local dual':^{COL6_WIDTH}}{'Global dual':^{COL7_WIDTH}}{'Primal bound':^{COL8_WIDTH}}{'Gap':^{COL9_WIDTH}}")
            else:
                print(f"{'Time':^{COL1_WIDTH}}{'Cur Node':^{COL2_WIDTH}}{'Open Nodes':^{COL3_WIDTH}}{'Iteration':^{COL4_WIDTH}}{'Redcost':^{COL5_WIDTH}}{'Local dual':^{COL6_WIDTH}}{'Global dual':^{COL7_WIDTH}}{'Primal bound':^{COL8_WIDTH}}{'Gap':^{COL9_WIDTH}}")
        elif not self.farkas and self.redcost_iteration % HEADER_FREQUENCY == 1:
            print()
            if self.data["model"] == 2:
                print(f"{'Time':^{COL1_WIDTH}}{'Cur Node':^{COL2_WIDTH}}{'Open Nodes':^{COL3_WIDTH}}{'Formulation|Iter':^{COL4_WIDTH}}{'Redcost':^{COL5_WIDTH}}{'Local dual':^{COL6_WIDTH}}{'Global dual':^{COL7_WIDTH}}{'Primal bound':^{COL8_WIDTH}}{'Gap':^{COL9_WIDTH}}")
            else:
                print(f"{'Time':^{COL1_WIDTH}}{'Cur Node':^{COL2_WIDTH}}{'Open Nodes':^{COL3_WIDTH}}{'Iteration':^{COL4_WIDTH}}{'Redcost':^{COL5_WIDTH}}{'Local dual':^{COL6_WIDTH}}{'Global dual':^{COL7_WIDTH}}{'Primal bound':^{COL8_WIDTH}}{'Gap':^{COL9_WIDTH}}")

        cur_node = self.model.getCurrentNode().getNumber()
        open_nodes = self.model.getNTotalNodes()
        iteration = self.farkas_iteration if self.farkas else self.redcost_iteration
        if "objval" in result:
            redcost = result["objval"]
        else:
            redcost = result["result"] # debug: this is misleading, it makes it seem like you're adding positive redcost variables

        primal = round(self.model.getPrimalbound(), 3)
        if hasattr(self, "best_sol"):
            primal = min(primal, round(self.best_sol["obj"], 3))
        global_dual = round(self.model.getDualbound(), 2)
        if not self.model.isZero(global_dual):
            gap = 100 * abs(global_dual - primal) / global_dual if not self.model.isInfinity(primal) else float("inf")
            if gap != float("inf"):
                gap = f"{gap:.2f}%"
        else:
            if not self.model.isInfinity(primal):
                gap = abs(primal)
            else:
                gap = float("inf")


        if "dualbound" in result:
            local_dual = result["dualbound"]
        else:
            local_dual = self.model.getCurrentNode().getLowerbound()
        local_dual = round(local_dual, 2)

        time = self.model.getSolvingTime()

        if "heuristic" in result and result["heuristic"]:
            heur = "*"
        else:
            heur = ""

        farkas = "F" if self.farkas else ""
        formulation = str(result.get("pricing_formulation", ""))

        # Print data
        iteration = f"{formulation} | {iteration}"
        redcost = f"{redcost:.2e}"
        print(f"{round(time):^{COL1_WIDTH}}{cur_node:^{COL2_WIDTH}}{open_nodes:^{COL3_WIDTH}}{farkas + iteration:^{COL4_WIDTH}}{redcost + heur:^{COL5_WIDTH}}{local_dual:^{COL6_WIDTH}}{global_dual:^{COL7_WIDTH}}{primal:^{COL8_WIDTH}}{gap:^{COL9_WIDTH}}")

    # Get result dict for SCIP
    def get_final_scip_dict(self, all_results):
        """
        Processes the results from SCIP optimization and returns a summary dictionary containing the final status, bounds, and relevant information.
        This method analyzes the results of the column generation or pricing step, determines the appropriate SCIP result status, computes lower bounds, and optionally triggers early branching or node cutoff based on solution properties.
        Args:
            all_results (dict): A dictionary containing results from subproblems or pricing steps. Each entry may include keys such as "result", "objval", and "pricing_formulation".
        Returns:
            dict: A dictionary summarizing the final SCIP status, including keys such as:
                - "result": The final SCIP result status (e.g., SUCCESS, DIDNOTRUN).
                - "lowerbound": The computed lower bound for the current node.
                - "objval": The minimum objective value found among subproblems.
                - "branchearly": (optional) Indicates if early branching is triggered.
        """

        if "result" in all_results and all_results["result"] in [SCIP_RESULT.DIDNOTRUN, SCIP_RESULT.INFEASIBLE]:
            return {"result": SCIP_RESULT.DIDNOTRUN}

        if not self.found_negative_redcost:
            self.data["optimal_duals"][self.cur_node_number] = self.data["dualSolsWithNames"] # for redcost fixing later

            self.data["lpsol"] = {}

            if not self.farkas and self.data["params"]["price_and_branch"]:
                result = self.optimize_integer_master_problem()
                if result["optimal"]:
                    return {"result": SCIP_RESULT.SUCCESS}

                if result["result"] == SCIP_RESULT.DIDNOTRUN: # timeout
                    return result

            self.data["local_dual_bounds"][self.cur_node_number] = self.model.getLPObjVal()
            
            # if solution is locally optimal, we don't care about other lower bounds, since no columns will improve the solution
            if not self.model.isInfinity(self.model.getLPObjVal()):
                return {"result": SCIP_RESULT.SUCCESS, "lowerbound": self.model.feasCeil(self.model.getLPObjVal())}
            else:
                return {"result": SCIP_RESULT.SUCCESS} # should it be infeasible? think

        if self.farkas:
            scip_dict = {"lowerbound": self.model.feasCeil(self.model.getDualbound())}
        else:
            scip_dict = {"lowerbound": min(self.model.getDualbound(), self.model.feasCeil(self.model.getLPObjVal()))}

        # all_results is a dict of dicts, each may have "objval"
        objvals = []
        for i in range(self.n_subprobs):
            result = all_results[i]
            if "objval" in result:
                objvals.append(result["objval"][0])
        
        if objvals:
            scip_dict["objval"] = min(objvals)
        else:
            scip_dict["objval"] = float("inf")

        if "result" not in all_results or all_results["result"] != SCIP_RESULT.SUCCESS:
            return all_results

        if not self.farkas and all(self.explored_subproblems.values()):
            # lagrangian bound

            if self.model.isGT(self.lagrangian_bound, scip_dict["lowerbound"]):
                best_bound = "Lagrangian bound"
                scip_dict["lowerbound"] = self.model.feasCeil(self.lagrangian_bound)

            if self.n_subprobs == 1:
                other_constant = 0
                for t in self.data["params"]["T_prime"]:
                    other_constant += self.data["dualSolutions"]["demand_cons"][t-1]*self.data["params"]["demand"][t]

                # farley bound
                min_lambda_price = float("inf")
                for mvar in self.model.getVars(transformed=True):
                    if mvar.name.startswith("t"):
                        continue

                    numerator = mvar.getObj()
                    denominator = 0
                    for t in self.data["params"]["T_prime"]:
                        cur_dual = self.data["dualSolutions"]["demand_cons"][t-1]
                        denominator += self.data["continuous_patterns"][mvar.name]["y[0,%i]"%t]*cur_dual

                    if self.model.isLE(denominator, 0):
                        continue

                    cur_lambda_price = numerator/denominator
                    min_lambda_price = min(min_lambda_price, cur_lambda_price)

                farley_bound = self.model.feasCeil(min_lambda_price*other_constant)
                if farley_bound > scip_dict["lowerbound"]:
                    best_bound = "Farley bound"
                    scip_dict["lowerbound"] = farley_bound

            if self.data["params"]["verbose"] >= 2:
                pass #print(45*" " + "%s found: %.3f" % (best_bound, scip_dict["lowerbound"]))

        scip_dict["result"] = SCIP_RESULT.SUCCESS

        # if the lowerbound and RMP solution respectively round up to the same integer, the bound is as tight as possible 
        can_branch_early = False
        if self.model.isEQ(self.model.feasCeil(self.model.getLPObjVal()), scip_dict["lowerbound"]): 
            can_branch_early = True
            self.data["local_dual_bounds"][self.cur_node_number] = str(scip_dict["lowerbound"])+"*"

        # early branching in case redcost is too small or solution is integer-optimal
        if not self.farkas and can_branch_early and (self.data["model"] == 0 or (self.data["model"] == 2 and all_results[0]["pricing_formulation"] == 2)):  # or (small_negative_redcost and shallow_node):
            scip_dict["branchearly"] = True
            self.data["early_branch"][self.cur_node_number] = True

            # need to check if suboptimal lp solution is integer feasible, because then we can't branch
            integer_feasible = True
            for mvar in self.model.getVars(transformed=True)[1:]:
                if not self.model.isFeasIntegral(self.model.getSolVal(sol=None, expr=mvar)):
                    integer_feasible = False
                    break

            if integer_feasible:
                scip_dict["result"] = SCIP_RESULT.SUCCESS
            else:
                scip_dict["result"] = SCIP_RESULT.DIDNOTRUN

            return scip_dict

        if self.model.isGE(scip_dict["lowerbound"], self.best_sol["obj"]):
            scip_dict["lowerbound"] = 10**10
            self.model.cutoffNode(self.model.getCurrentNode())
            # scip_dict["result"] = SCIP_RESULT.CUTOFF # pricer doesn't really accept cutoff
        else:
            scip_dict["result"] = SCIP_RESULT.SUCCESS

        return scip_dict

    # Get better dualbound for ORIG
    def compute_lagrangian_dualbound(self):
        if self.found_negative_redcost and not self.farkas:
            if self.data["params"]["linear_relaxation"]:
                lowerbound = self.lagrangian_bound
            else:
                lowerbound = self.model.feasCeil(self.lagrangian_bound)
            return lowerbound
        else:
            return

    # Error safe add_column_to_RMP
    def add_column_to_RMP(self, result, subprob, given_delta=-1, heuristic=False):
        try:
            return self._add_column_to_RMP(result=result, subprob=subprob, given_delta=given_delta, heuristic=heuristic)
        except Exception as e:
            log_error("add_column_to_RMP", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}
    
    # Checks if current columns can be added to RMP and does it, along with master constraint manipulation
    def _add_column_to_RMP(self, result, subprob, given_delta=-1, heuristic=False) -> list[Variable]:
        """
        Adds a new column (variable) to the Restricted Master Problem (RMP) based on the solution of a subproblem.
        This method handles multiple pricing formulations and manages the addition of lambda, mu, and delta variables,
        as well as their associated constraints. It also updates internal data structures for pattern encoding, branching,
        and compatibility constraints. Duplicate columns are detected and handled by updating variable bounds.
        Parameters
        ----------
        result : dict
            Dictionary containing the solution of the subproblem, including objective value, variable assignments,
            patterns, maintenance costs, and other relevant data.
        subprob : int
            Index of the subproblem for which the column is being added.
        given_delta : int or dict, optional
            The delta pattern to be used for the new column. Its type and usage depend on the pricing formulation.
            Default is -1.
        heuristic : bool, optional
            Indicates whether the column was generated heuristically. Default is False.
        Returns
        -------
        list[Variable]
            A list of newly added variables to the RMP. The type and content of the list depend on the pricing formulation:
            - Formulation -1: List of lambda variables.
            - Formulation 0: List of mu variables.
            - Formulation 1: List of delta variables.
            - Formulation 2: List of (mu, delta) variable pairs.
        Raises
        ------
        AssertionError
            If required patterns or variables are missing, or if infeasible columns are detected.
        ValueError
            If an unexpected pricing formulation is encountered or if inequalities are misconfigured.
        Notes
        -----
        - Handles duplicate columns by updating upper bounds instead of adding new variables.
        - Updates branching and compatibility constraints for newly added variables.
        - Manages internal encodings for patterns to facilitate branching and lookup.
        - Supports multiple pricing formulations, each with specific logic for variable and constraint management.
        """

        assert self.found_negative_redcost == True

        added_vars:             list[Variable]       = []
        added_mus:              list[Variable]       = []
        added_deltas:           list[Variable]       = []
        newVar:                 Optional[Variable]   = None
        new_mu:                 Optional[Variable]   = None
        new_delta:              Optional[Variable]   = None
        identical:              bool                 = False
        currentNumVar:          int                  = -1
        new_compatibility_cons: Optional[Constraint] = None
        old_delta:              str                  = ""
        current_mu_index:       int                  = -1
        given_mu:               int                  = -1
        converted_mus:         dict                  = {}

        objval                     = result["objval"]
        fixed_redcost_contribution = result["fixed_redcost_contribution"]
        vars                       = result["vars"]
        mu_patterns                = result["mu_patterns"]
        delta_patterns             = result["delta_patterns"]
        pricing_formulation        = result["pricing_formulation"]
        maintenance_cost           = result["maintenance_cost"]

        if pricing_formulation == 1:
            old_delta          = result["old_delta"] # need this because we want to remove mu from this old delta
            converted_mus      = result["converted_mus"] # need this because we want to access the variables that will be transfered to the new delta

        self.data["previous_redcosts"][subprob].append(objval[0])

        if pricing_formulation == 0:
            given_delta        = result["given_delta"]
        else:
            given_delta        = {i: None for i in range(len(objval))}

        if pricing_formulation == 0:
            assert mu_patterns
            assert given_delta[0] != None, "PP 0 needs to be given a discrete pattern!"

        have_new_col = False
        # for each solution found in subproblem
        for i in range(len(objval)):
            if pricing_formulation == -1:
                decision_vars = vars[i]
                cur_mu = None
                cur_delta = None
                # actual_decision_vars = {var: val for var, val in vars[i].items() if var.startswith('y') or var.startswith("m")}
            else:
                cur_mu = None
                cur_delta = None
                if pricing_formulation == 0:
                    cur_mu = mu_patterns[i]
                elif pricing_formulation == 1:
                    cur_delta = delta_patterns[i]

                decision_vars = {}

            if self.data["params"]["debug_mode"] and pricing_formulation != 1:
                # Checking if reduced cost is negative. If column was already visited, discard it. # debug why are identical columns regenerated?
                new_col = self.col_is_new(pricing_formulation=pricing_formulation, subprob=subprob, mu_patterns=cur_mu,\
                                        vars=decision_vars, given_delta=given_delta[i], delta_patterns=cur_delta)
                
                if not new_col: # this must be because the variable was deactivated due to old age, or redcost_fixed
                    if pricing_formulation == -1:
                        pattern_key = ''.join(str(decision_vars))
                        var_name = self.data["pattern_encoding"][subprob][pattern_key]
                        existing_var = self.data["var"][subprob][var_name]
                        target_ub = self.data["params"]["machines_per_group"][subprob]

                    elif pricing_formulation == 0:
                        mu_var = None
                        for mu_name, mu_pat in self.data["Mu_patterns"][subprob][given_delta[i]].items():
                            if mu_pat == cur_mu:
                                mu_var = self.data["Mu"][subprob][given_delta[i]][mu_name]
                                break
                        assert mu_var is not None, "Could not locate existing mu pattern."
                        delta_var = self.data["Delta"][subprob][given_delta[i]]
                        existing_var = mu_var
                        target_ub = delta_var.getUbLocal()

                    elif pricing_formulation in (2,):
                        # Could be delta or mu; first try delta by hashed key
                        existing_var = None
                        if cur_delta:
                            delta_key = self._ARMP_get_delta_key_for_hashing(subprob=subprob,
                                                                        delta_pattern=cur_delta)
                            if delta_key in self.data["delta_encoding"][subprob]:
                                existing_delta_name = self.data["delta_encoding"][subprob][delta_key][0]
                                existing_var = self.data["Delta"][subprob][existing_delta_name]
                        if existing_var is None and cur_mu:
                            # fallback to mu pattern exact match
                            for dname in self.data["Mu_patterns"][subprob]:
                                for mu_name, mu_pat in self.data["Mu_patterns"][subprob][dname].items():
                                    if mu_pat == cur_mu:
                                        existing_var = self.data["Mu"][subprob][dname][mu_name]
                                        break
                                if existing_var: break
                        assert existing_var is not None, "Existing pattern (formulation 2) not found."
                        target_ub = self.data["params"]["machines_per_group"][subprob]
                    else:
                        raise ValueError("Unexpected pricing formulation for duplicate handling.")

                    old_var = existing_var.data.get("old", False)
                    if not old_var:
                        redcost_fixed_var = self.data["redcost_fixed_vars"][self.cur_node_number].get(existing_var.name, False)

                    # some SCIP bug is making it so multiple identical solutions are reported from the same pricing problem. not very problematic
                    # assert old_var or redcost_fixed_var, "Expected existing variable to be marked old."

                    # Increase (or reset) its upper bound as specified
                    self.model.chgVarUb(existing_var, target_ub)
                    continue

                # checking if new column satisfies the constraints of the pricing problem (for heuristic)
                if self.data["params"]["model"] == 0:
                    pass#column_feasible = self.check_column_feasibility(subprob=subprob, vars=vars[i])
                    # assert column_feasible, "Column is infeasible for subproblem %i" % subprob
            else:
                new_col = True

            if new_col:
                have_new_col = True

            # we try to always improve the deltas
            if new_col and (self.model.isLE(objval[i] - fixed_redcost_contribution, -self.dualfeastol) or pricing_formulation == 1):

                if heuristic:
                    self.heuristic_cols += 1
                else:
                    self.optimal_cols += 1

                if self.data["params"]["linear_relaxation"]:
                    vtype="C"
                else:
                    vtype="I"

                # Adding lambda variable (no need for UB, convexity constraint does it)
                if pricing_formulation == -1:
                    currentNumVar = len(self.data["var"][subprob])
                    newVar = self.model.addVar("lambda[%i,%s]*" % (subprob, currentNumVar), vtype=vtype,
                                            lb = 0, obj=maintenance_cost[i], pricedVar=True)
                    newVar.data = {
                                    'subprob': subprob,
                                    'age':0,
                                    'old': False
                                    }
                    added_vars.append(newVar)

                # Adding mu variable
                current_delta_index = self.n_delta # modified when adding delta. needs to be here for managing mu's

                if pricing_formulation in [0,2]:
                    if current_delta_index == -1:
                        assert self.farkas
                        given_delta_index = 0

                    if given_delta[i] == None:
                        assert pricing_formulation == 2
                        given_delta_index = current_delta_index
                    else:
                        given_delta_index = int(given_delta[i].split(",")[1][:-2])

                    current_mu_index = self.n_mu
                    if "mu_name" in result:
                        mu_name = "transfer_" + result["mu_name"]
                    else:
                        mu_name = "mu[%i,%i,%s]*" % (subprob, given_delta_index, current_mu_index)

                    new_mu = self.model.addVar(mu_name, vtype="C", lb = 0, obj=0, pricedVar=True, deletable=True)
                    self.n_mu += 1
                    # del_mu = self.model.addVar(name="del_mu[%i,%i,%s]*" % (subprob, given_delta_index, current_mu_index), vtype="C",
                                            # lb = 0, obj=0, pricedVar=True)
                    # self.model.addCons(del_mu == new_mu, name="del_cons_mu[%i,%i,%s]*" % (subprob, given_delta_index, current_mu_index))

                    # new_mu.data = {'subprob': subprob, 'was_deleted': False, "del_var": del_mu} # was_deleted to not duplicate deletions later
                    new_mu.data = {"subprob": subprob, "is_optimal": False, "old": False}
                    added_mus.append(new_mu)

                # Adding delta variable
                if pricing_formulation in [1,2]:
                    identical = False
                    key = self._ARMP_get_delta_key_for_hashing(delta_pattern=delta_patterns[i], subprob=subprob)
                    self.data["delta_encoding_rev"][subprob][key] = given_delta[i]
                    if key in self.data["delta_encoding"][subprob]:
                        identical = True
                        delta_name = self.data["delta_encoding"][subprob][key][0]
                        new_delta = self.data["Delta"][subprob][delta_name]
                        given_delta[i] = new_delta.name

                    if not identical:
                        new_delta = self.model.addVar("delta[%i,%s]*" % (subprob, current_delta_index), vtype=vtype,
                                                lb = 0, obj=maintenance_cost[i], pricedVar=True, deletable=True)
                        self.n_delta+=1
                        new_delta.data = {'subprob': subprob, 'old': False}
                        if given_delta[i] == None:
                            given_delta[i] = new_delta.name
                        added_deltas.append(new_delta)

                # adding the new column to convexity constraint
                if pricing_formulation == -1: 
                    self.model.addConsCoeff(self.data["convexity_cons"][subprob], newVar, 1)

                # adding new delta to convexity constraints
                if pricing_formulation in [1,2] and not identical:
                    self.model.addConsCoeff(self.data["convexity_cons"][subprob], new_delta, 1)

                # adding new mu to compatibility constraints
                if pricing_formulation == 0:
                    self.model.addConsCoeff(self.data["compatibility_cons"][subprob][given_delta[i]], new_mu, 1)

                # Adding new row
                if pricing_formulation in [1,2]:
                    if pricing_formulation == 2:
                        given_mu = new_mu
                        if identical:
                            self.model.addConsCoeff(self.data["compatibility_cons"][subprob][given_delta[i]], new_mu, 1)
                        else:
                            new_compatibility_cons = self.model.addCons(given_mu <= new_delta, modifiable=True, name="A_compatibility_%s" % (new_delta))
                            self.data["compatibility_cons"][subprob][new_delta.name] = new_compatibility_cons
                    elif pricing_formulation == 1: # added later
                        given_mu = converted_mus[i]

                # Adding new column to demand constraints (this will be harder with other formulations)
                if pricing_formulation == -1:                
                    for t, c in enumerate(self.data["demand_cons"]):
                        self.model.addConsCoeff(c, newVar, round_up(vars[i]["y[0,%i]" % (t+1)], 5))

                elif pricing_formulation in [0,2]:
                    for t, c in enumerate(self.data["demand_cons"]):
                        self.model.addConsCoeff(c, new_mu, mu_patterns[i]["y[0,%i]" % (t+1)])

                # Debug: VERY IMPORTANT!!! because variables are added globally, you also need to add them to all branching constraints
                # Adding new column to branching constraints
                if pricing_formulation in [-1,1,2]:
                    for cur_node_number in self.data["branching_decisions"]: # Fix here you are iterating over old nodes as well. Slower, but you can't just go over the leaves, because they don't have branching constraints yet.
                        # Todo: add a marker to the node or somewhere else that says whether the guy can be safely ignored

                        all_branching_decisions = self.get_branching_decision(cur_node_number, subprob)
                        for branching_index in all_branching_decisions:
                            branching_decision = all_branching_decisions[branching_index]
                            if branching_decision.branching_rule == "disaggregate":
                                assert self.data["params"]["machines_per_group"][subprob] == 1

                            if branching_decision.branching_rule != "aggregatevarbounds":
                                continue                        

                            branching_thresholds = branching_decision.branching_thresholds
                            add_to_branching_cons = self.mvar_should_be_added_to_branching_cons(branching_thresholds, vars[i] if pricing_formulation == -1 else delta_patterns[i])

                            if add_to_branching_cons:
                                self.add_mvar_to_branching_cons(mvar=newVar if pricing_formulation==-1 else delta_patterns[i], branching_decision=branching_decision, cur_node_number=cur_node_number, pricing_formulation=pricing_formulation)

                            branching_index += 1

                # Storing the new variable in the pricer data.
                if pricing_formulation == -1:
                    self.data["var"][subprob][newVar.name] = newVar
                    self.data["patterns"][subprob][newVar.name] = decision_vars

                    # todo this was buggy, take another look. you're not using it in branching
                    # # to avoid rechecking during branching
                    # for k, v in actual_decision_vars.items():
                    #     if not self.model.isZero(v):
                    #         self.data["filtered_mvars"][subprob][k].append(v)

                    # integer patterns play a fundamentally different role
                    cur_integer_pattern = {k: self.model.feasFloor(v) for k, v in decision_vars.items() if k.startswith("m")} # need feasFloor because sometimes we get 0.9999999999, which is the same for SCIP but not for Python
                    cur_integer_pattern["total_cost"] = self.model.feasFloor(decision_vars["total_cost"])
                    self.data["integer_patterns"][newVar.name] = cur_integer_pattern
                    cur_integer_encoding = str(sorted(list(cur_integer_pattern.items())))

                    # to make lookup easier when branching
                    if cur_integer_encoding in self.data["integer_encoding"][subprob]:
                        self.data["integer_encoding"][subprob][cur_integer_encoding].append(newVar.name)
                    else:
                        self.data["integer_encoding"][subprob][cur_integer_encoding] = [newVar.name]

                    # but it's still nice to have continuous encoding
                    cur_continuous_pattern = {k: v for k, v in decision_vars.items() if k.startswith("y")}
                    self.data["continuous_patterns"][newVar.name] = cur_continuous_pattern
                    cur_continuous_encoding = str(cur_continuous_pattern)

                    # to make lookup easier when branching
                    if cur_continuous_encoding in self.data["continuous_encoding"][subprob]:
                        self.data["continuous_encoding"][subprob][cur_continuous_encoding].append(newVar.name)
                    else:
                        self.data["continuous_encoding"][subprob][cur_continuous_encoding] = [newVar.name]

                    if self.data["params"]["discrete_production"]:
                        cur_discrete_production_pattern = {k: v for k, v in decision_vars.items() if k.startswith("d")}
                        self.data["discrete_production_pattern"][newVar.name] = cur_discrete_production_pattern
                        cur_discrete_production_encoding = str(cur_discrete_production_pattern)

                        if cur_discrete_production_encoding in self.data["discrete_production_encoding"][subprob]:
                            self.data["discrete_production_encoding"][subprob][cur_discrete_production_encoding].append(newVar.name)
                        else:
                            self.data["discrete_production_encoding"][subprob][cur_discrete_production_encoding] = [newVar.name]

                    self.data["full_patterns"][subprob][newVar.name] = vars[i]
                    self.data["pattern_encoding"][subprob][''.join(str(decision_vars))] = newVar.name

                    # To more easily get fractional sums when branching
                    for k, v in cur_integer_pattern.items():
                        self.data["mvars_by_integer_variable"][subprob][(k, v)].append(newVar.name)

                if pricing_formulation == 1:
                    if not identical:
                        self.data["Delta"][subprob][new_delta.name]              = new_delta
                        self.data["Delta_patterns"][subprob][new_delta.name]     = delta_patterns[i]
                        self.data["compatibility_cons"][subprob][new_delta.name] = new_compatibility_cons
                        self.data["Mu"][subprob][new_delta.name]                 = {}
                        self.data["Mu_patterns"][subprob][new_delta.name]        = {}

                    # Adding mu to the new delta data and compatibility constraint
                    mu = converted_mus[i]
                    # self.data["Mu"][subprob][new_delta.name][mu.name] = mu
                    # self.data["Mu_patterns"][subprob][new_delta.name][mu.name] = mu_patterns[i]

                    self.remove_column_from_RMP(var=mu, subprob=subprob, old_delta=old_delta[i])
            
                    if not identical:
                        new_compatibility_cons = self.model.addCons(0 >= -new_delta, modifiable=True, name="A_compatibility_%s" % (new_delta.name))
                        self.data["compatibility_cons"][subprob][new_delta.name] = new_compatibility_cons
                    
                    # Adding transfered mu to the problem
                    added_mus = self.add_column_to_RMP(subprob=subprob, result={"mu_name": mu.name, "given_delta": {0: new_delta.name}, "maintenance_cost": 0, "fixed_redcost_contribution": 0, "objval": [-1], "vars": [], "mu_patterns": [mu_patterns[i]], "delta_patterns": [], "pricing_formulation": 0})
                    added_mus[0].data["is_optimal"] = True

                if pricing_formulation in [1,2]:
                    self.data["all_delta_patterns"][new_delta.name] = delta_patterns[i]
                    key = self._ARMP_get_delta_key_for_hashing(delta_pattern=delta_patterns[i], subprob=subprob)

                    # to make lookup easier when branching
                    if key not in self.data["delta_encoding"][subprob]:
                        self.data["delta_encoding"][subprob][key] = [new_delta.name]
                        self.data["delta_encoding_rev"][subprob][new_delta.name] = key

                # if delta_patterns[i] in self.data["Delta_patterns"][subprob].values():
                #     pass

                if pricing_formulation == 2 and not identical:
                    self.data["Delta"][subprob][new_delta.name]              = new_delta
                    self.data["Delta_patterns"][subprob][new_delta.name]     = delta_patterns[i]
                    self.data["compatibility_cons"][subprob][new_delta.name] = new_compatibility_cons
                    self.data["Mu"][subprob][new_delta.name]                 = {}
                    self.data["Mu_patterns"][subprob][new_delta.name]        = {}

                if pricing_formulation == 2: given_delta[i] = new_delta.name

                if pricing_formulation in [0,2]:
                    self.data["Mu"][subprob][given_delta[i]][new_mu.name]          = new_mu
                    self.data["Mu_patterns"][subprob][given_delta[i]][new_mu.name] = mu_patterns[i]

        # Had an issue here with using epsilon instead of dualfeastol
        assert have_new_col or "compact_run" in result, "Repeated column with negative redcost"

        if pricing_formulation == -1:
            return added_vars
        elif pricing_formulation == 0:
            return added_mus
        elif pricing_formulation == 1:
            return added_deltas
        elif pricing_formulation == 2:
            return list(zip(added_mus, added_deltas))
        else:
            raise ValueError("Invalid formulation")

    # Error safe remove_column_from_RMP
    def remove_column_from_RMP(self, var, subprob, old_delta=""):
        try:
            return self._remove_column_from_RMP(var, subprob, old_delta)
        except Exception as e:
            log_error("remove_column_from_RMP", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    # Indirectly removes a column from the RMP, along with master constraint manipulation
    def _remove_column_from_RMP(self, var, subprob, old_delta):
        """
        Removes a variable (column) from the Restricted Master Problem (RMP) and updates associated data structures.
        Depending on the type of variable (`lambda`, `delta`, or `mu`), this method:
        - Sets the variable's upper bound to 0 in the model, marking it for deletion.
        - Removes the variable from relevant dictionaries tracking variables, patterns, encodings, and constraints.
        - For `delta` variables, also removes associated `mu` variables and updates encoding mappings.
        - For `mu` variables, removes them from the corresponding `delta` and updates compatibility constraints.
        - If a `delta` variable has no associated `mu` variables left, recursively removes the `delta` variable.
        - Optionally prints verbose information about the removal process based on verbosity settings.
        Args:
            var: The variable to be removed from the RMP.
            subprob: The subproblem identifier associated with the variable.
            old_delta: The previous delta pattern associated with a `mu` variable (used for cleanup).
        Returns:
            None
        """
        if self.data["params"]["verbose"] >= 2:
            if var.name.startswith("lambda"):
                self.data["removed_lambdas"] += 1
            elif var.name.startswith("delta"):
                self.data["removed_deltas"] += 1
            elif var.name.startswith("mu"):
                self.data["removed_mus"] += 1

            if self.data["params"]["verbose"] >= 4:
                print(f"Removing {var.name}")

        # adds aux variable that is equal to -var.
        if var.name.startswith("lambda"):
            self.model.chgVarUb(var, 0) # setting upper bound to 0, so variable is later deleted
            del self.data["vars"][subprob][var.name]
            del self.data["patterns"][subprob][var.name]

        elif var.name.startswith("delta"):
            self.model.chgVarUb(var, 0) # setting upper bound to 0, so variable is later deleted
            delta_pattern_encoding = self.data["delta_encoding_rev"][subprob].pop(var.name, None)
            del self.data["Delta"][subprob][var.name]
            del self.data["Delta_patterns"][subprob][var.name]
            del self.data["Mu"][subprob][var.name] # removing all mus associated with this delta
            del self.data["Mu_patterns"][subprob][var.name]
            del self.data["delta_encoding"][subprob][delta_pattern_encoding]

        elif var.name.startswith("mu"):
            self.model.chgVarUb(var, 0) # setting upper bound to 0, so variable is later deleted
            del self.data["Mu"][subprob][old_delta][var.name]
            del self.data["Mu_patterns"][subprob][old_delta][var.name]

            # maybe don't remove the delta, since you might regenerate it for other columns. Maybe put it way down in the sorted list of deltas?
            if not self.data["Mu"][subprob][old_delta]:
                self.remove_column_from_RMP(var=self.data["Delta"][subprob][old_delta], subprob=subprob, old_delta="")

        return   

    def col_is_new(self, vars, pricing_formulation, subprob, mu_patterns, given_delta, delta_patterns):
        try:
            return self._col_is_new(vars, pricing_formulation, subprob, mu_patterns, given_delta, delta_patterns)
        except Exception as e:
            log_error("col_is_new", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    # Checks if column was already added to RMP    
    def _col_is_new(self, vars, pricing_formulation, subprob, mu_patterns, given_delta, delta_patterns) -> bool:
        """
        Checks whether column has already been added to the given patterns
        """
        #return True
        if pricing_formulation == -1:
            new_col = ''.join(str(vars)) not in self.data["pattern_encoding"][subprob]

        elif pricing_formulation == 0:
            new_col = ''.join(str(mu_patterns)) not in self.data["mu_encoding"][subprob]
        elif pricing_formulation == 1:
            new_col = ''.join(str(delta_patterns)) not in self.data["delta_encoding"][subprob]
        elif pricing_formulation == 2:
            new_continuous_col = True
            new_discrete_col   = True
            if given_delta in self.data["Mu"][subprob]:
                new_col = ''.join(str(mu_patterns)) not in self.data["mu_encoding"][subprob]
            if self.data["Delta"][subprob]:
                new_col = ''.join(str(delta_patterns)) not in self.data["delta_encoding"][subprob]
            new_col = new_discrete_col or new_continuous_col
        else:
            raise ValueError("Invalid formulation")

        return new_col

    def mvar_should_be_added_to_branching_cons(self, branching_thresholds, pat):
        """
        Determines whether a variable should be added to the branching constraints by
        checking if all associated thresholds are verified.

        Args:
            branching_decision (Constraint): The branching decision constraint.
            subprob (int): The subproblem index.
            pat (str): The pattern string.

        Returns:
            bool: True if the variable should be added to the branching constraints, False otherwise.
        """
        return self._mvar_should_be_added_to_branching_cons(branching_thresholds, pat)

    def _mvar_should_be_added_to_branching_cons(self, branching_thresholds, pat):
        # Checking if all thresholds are satisfied 
        add_to_branching_cons = True
        for cur_branching_threshold in branching_thresholds:

            # sum of all variables was fractional
            if cur_branching_threshold == "all":
                assert len(branching_thresholds) == 1
                break

            # sum of variables in subprob was fractional
            if cur_branching_threshold == "subprob":
                assert len(branching_thresholds) == 1
                break

            pricing_var, inequality, threshold = cur_branching_threshold

            if inequality == "<=":
                if self.model.isGT(pat[pricing_var], threshold):
                    add_to_branching_cons = False
                    break
            elif inequality == ">=":
                if self.model.isLT(pat[pricing_var], threshold):
                    add_to_branching_cons = False
                    break
            else:
                raise ValueError("Something went wrong with the inequalities.")
        return add_to_branching_cons

    def add_mvar_to_branching_cons(self, mvar, branching_decision, cur_node_number, pricing_formulation):
        """
        Adds a master variable to the branching constraints of a specific branching decision.
        """

        return self._add_mvar_to_branching_cons(mvar, branching_decision, cur_node_number, pricing_formulation)

    def _add_mvar_to_branching_cons(self, mvar, branching_decision, cur_node_number, pricing_formulation):
        cur_aggregate_master_vars = branching_decision.aggregate_master_vars
        branching_decision.naggregate_master_vars += 1

        if pricing_formulation == -1:
            if mvar.name in cur_aggregate_master_vars:
                assert self.var_in_branching_cons(mvar, branching_decision)
                return True

            cur_aggregate_master_vars[mvar.name] = mvar

            # because the constraint is only added in the event handler, not when the node is created (addConsNode issues)
            if cur_node_number in self.data["branching_cons"]:

                # this is annoying, because you can't preform a proper copy of a SCIP constraint, so you're storing the same constraint in more than one place
                if self.var_in_branching_cons(mvar, branching_decision):
                    return True

                self.model.addConsCoeff(branching_decision.branching_con, mvar, 1)
        else:
            cur_aggregate_master_vars[mvar.name] = mvar
            if "branching_cons" in self.data["branching_decisions"][cur_node_number]:
                self.model.addConsCoeff(branching_decision.branching_con, mvar, 1)

        return

    def optimize_integer_master_problem(self):
        """
        Attempts to optimize the integer restricted master problem in a column generation framework.

        This method is typically called during branching when a sufficient number of columns have been added to the model.
        It creates a copy of the current problem without branching constraints, sets aggressive heuristics and emphasis
        on improving the primal bound, and solves the integer restricted master problem with a limited number of nodes and time.

        If an improving integer solution is found, it updates the primal bound and stores the best solution values for
        relevant variables. If no improving solution is found, it increases the required number of columns for future
        optimization attempts.

        Returns:
            dict: A dictionary with the result status, either SCIP_RESULT.SUCCESS if an improving solution is found,
                  or SCIP_RESULT.DIDNOTFIND otherwise.
        """
        # todo: when optimal solution is repaired, this does not need to run. maybe it should be called in branching after repair?
        # only run if a sufficient number of columns have been added (it starts to get increasingly expensive)
        cur_nvars = self.model.getNVars(transformed=True)
        if self.cur_node_number == 1:
            self.ncols_required_for_imp_opt = cur_nvars//2

        self.irmp_cooldown -= 1
        if cur_nvars - self.prev_node_nvars <= self.ncols_required_for_imp_opt or self.irmp_cooldown > 0:
            return {"result": None, "optimal": False}

        self.ran_integer_rmp = True
        self.irmp_cooldown = IRMP_COOLDOWN_DEFAULT # to not run IRMP too often
        self.model.writeProblem("integer_rmp.cip", trans=True, verbose=False)
        self.__remove_branching_cons("integer_rmp.cip", "integer_rmp_no_branching.cip")

        m = Model()
        m.readProblem("integer_rmp_no_branching.cip")

        # focus on the primal bound
        m.setHeuristics(SCIP_PARAMSETTING.AGGRESSIVE)
        m.setEmphasis(SCIP_PARAMEMPHASIS.PHASEIMPROVE)
        m.setObjlimit(self.primal_bound - 1)
        
        # apparently SCIP keeps branching and branching in some instances. explicitely using longint because some bugs were happening
        m.setParam("limits/nodes", 500)

        time_left = self.compute_time_left()
        m.setParam("limits/time", min(time_left, self.data["params"]["time_limit"]/10))
        m.setObjIntegral()

        if self.data["params"]["verbose"] >= 2:
            print("Optimizing integer master problem")

        if self.data["params"]["verbose"] <= 3:
            m.hideOutput()

        try:
            m.optimize() # debug: SCIP bug sometimes has ERROR: Invalid value <-2004313176> for longint parameter <limits/nodes>. Must be in range [-1,9223372036854775807] 
        except:
            return {"result": SCIP_RESULT.DIDNOTFIND, "optimal": False}

        self.primal_bound = min(self.primal_bound, self.model.getPrimalbound()) # in case some other heuristic found a primal bound
        if self.model.isEQ(m.getPrimalbound(), self.model.getDualbound()): 
            optimal = True
        else:
            optimal = False

        if m.getNSols() > 0 and self.model.isLT(m.getPrimalbound(), self.primal_bound) and m.getStatus() != "infeasible": # found an improving integer solution
            if self.data["params"]["verbose"] >= 2:
                print("Found improving solution. New bound: %.3f" % m.getPrimalbound())
                if optimal:
                    print("Optimal solution found.")
                else:
                    dual_bound = self.model.getDualbound()
                    if not self.model.isZero(dual_bound):
                        print("New gap: %.3f%%" % (100*(m.getPrimalbound()-dual_bound)/dual_bound))
                    else:
                        print("Dual remains at zero.")

            self.primal_bound = m.getPrimalbound() # to cutoff nodes later. recall that SCIP doesn't know that this is a primal solution
            best_int_sol = ast.literal_eval(str(m.getBestSol()))
            self.best_sol = {}
            self.best_mu  = {}
            self.best_delta = {}
            sol = self.model.createSol()
            for subprob in range(self.n_subprobs):
                if self.data["model"] == 0:
                    self.best_sol[subprob] = defaultdict(int)
                    for mvar_name, mvar in self.data["var"][subprob].items():
                        mvar_name = mvar.name
                        self.best_sol[subprob][mvar_name] = best_int_sol[mvar_name]
                        self.model.setSolVal(sol, mvar, self.best_sol[subprob][mvar_name])
                elif self.data["model"] == 2:
                    self.best_mu[subprob]  = defaultdict(int)
                    self.best_delta[subprob] = defaultdict(int)
                    for delta_name, delta in self.data["Delta"][subprob].items():
                        delta_name = delta.name
                        self.best_delta[subprob][delta_name] = best_int_sol[delta_name]
                        self.model.setSolVal(sol, delta, self.best_delta[subprob][delta_name])
                        for mu_name, mu in self.data["Mu"][subprob][delta_name].items():
                            mu_name = mu.name
                            self.best_mu[subprob][mu_name] = best_int_sol[mu_name]
                            self.model.setSolVal(sol, mu, self.best_mu[subprob][mu_name])

            self.model.addSol(sol)
            self.best_sol["obj"] = self.model.feasCeil(self.primal_bound) # numerics

            return {"result": SCIP_RESULT.SUCCESS, "optimal": optimal}

            # assert self.model.isEQ(m.getPrimalbound(), self.model.getSolObjVal(sol))
        else: # punishing in case no improving solution was found
            if self.data["params"]["verbose"] >= 2:
                print("No improving integer solution found.")
            self.prev_node_nvars = cur_nvars
            self.ncols_required_for_imp_opt = round((1+FAILED_IRMP_PENALTY_FACTOR)*self.ncols_required_for_imp_opt)
        # assert False
        return {"result": SCIP_RESULT.DIDNOTFIND, "optimal": False}

    def __remove_branching_cons(self, input_file, output_file):
        with open(input_file, "r") as f_in:
            lines = f_in.readlines()

        start_of_file = []
        # Find the line with "CONSTRAINTS"
        for i, line in enumerate(lines):
            start_of_file.append(line)
            if "CONSTRAINTS" in line:
                constraints_line = lines[i + 1:-1]  # assuming the constraints are on the next line
                break
        else:
            raise ValueError("No CONSTRAINTS line found")

        # Split into individual constraints
        constraints = constraints_line

        filtered_constraints = []
        if self.data["model"] == 0:
            # Keep only constraints starting with 'O'
            filtered_constraints = [c for c in constraints if "<O_" in c[:20]]
        elif self.data["model"] == 2:
            # Keep only constraints starting with 'O' or 'C'
            filtered_constraints = [c for c in constraints if ("<A_" in c[:20])]

        # Write back to file (you can also keep the header line if you want)
        with open(output_file, "w") as f_out:
            f_out.writelines(start_of_file)  # write the header and everything before constraints
            f_out.writelines(filtered_constraints)
            f_out.write("END\n")

    # Finish pricing if negative redcost found
    def break_for_better_duals(self, subprob):
        self.break_early[self.cur_node_number] = False
        if not self.farkas:
            if self.n_subprobs > 1:
                for i in self.data["iterations_since_last"]:
                    if i != subprob:
                        self.data["iterations_since_last"][i]+=1

                for i in self.data["iterations_since_last"]:
                    if self.data["iterations_since_last"][i] > (self.n_subprobs-1)*10: # arbitrary
                        self.break_early[self.cur_node_number] = True
                        break

            return self.break_early[self.cur_node_number] # breaking straight away to get updated duals

    # Solves pricing problem (-1 to 2) and prepares to add column to RMP
    def solve_pricing(self, subprob, dualSolutions, reopt, heuristic, pricing_formulation, given_delta, given_mu, old_delta=None):
        try:
            return self._solve_pricing(subprob, dualSolutions, reopt, heuristic, pricing_formulation, given_delta, given_mu, old_delta)
        except Exception as e:
            log_error("solve_pricing", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}

    def get_duals_for_pricing(self, pricing_formulation, dualSolutions, subprob, given_delta, old_delta, given_mu):
        cur_node_number = self.model.getCurrentNode().getNumber()

        if pricing_formulation == -1:
            cur_dualSolutions = {"convexity_duals": dualSolutions["convexity_cons"][subprob], "demand_duals": dualSolutions["demand_cons"], "branching_duals": dualSolutions["branching_cons"][cur_node_number][subprob]}
            pi    = [cur_dualSolutions["convexity_duals"]] + cur_dualSolutions["demand_duals"]
            gamma = cur_dualSolutions["branching_duals"]
            eta   = None
            mu_dual_contribution = None
        else:
            # assert not self.data["params"]["dual_stabilization"], "Dual stabilization not implemented for ARMP yet"

            cur_dualSolutions = {"convexity_duals": dualSolutions["convexity_cons"][subprob], "compatibility_duals": dualSolutions["compatibility_cons"][subprob], "demand_duals": dualSolutions["demand_cons"], "branching_duals": dualSolutions["branching_cons"][cur_node_number][subprob]}
            pi    = [cur_dualSolutions["convexity_duals"]] + cur_dualSolutions["demand_duals"]
            if pricing_formulation == 0:
                assert given_delta != None
                eta   = cur_dualSolutions["compatibility_duals"][given_delta]
            else:
                eta = "alsdnkajn"

            if pricing_formulation == 1:
                assert given_mu != None
                assert old_delta != None
                given_mu = self.data["Mu"][subprob][old_delta][given_mu]
                mu_val = self.model.getSolVal(sol=None, expr=given_mu)
                mu_dual_contribution = self.ARMP_key_for_sorting_mus(mu=given_mu, old_delta=old_delta, mu_val=mu_val, pi=pi, subprob=subprob)
            else:
                mu_dual_contribution = None

            gamma = cur_dualSolutions["branching_duals"]

        return pi, gamma, eta, mu_dual_contribution

    def optimize_pricing_problem(self, pi, gamma, eta, subprob, fixed_delta, fixed_mu, pricing_formulation, branching_decisions, mu_dual_contribution, given_delta, optimal=False):
        """
        Solves the pricing problem for a given subproblem in a column generation or branch-and-price framework.
        This method creates and configures a pricing model, applies dual stabilization if enabled, and optimizes the model
        either heuristically or to optimality depending on the parameters. It handles different pricing formulations, 
        manages objective limits, and processes solutions to extract relevant columns and reduced costs.
        Args:
            pi (list or np.ndarray): Dual variables associated with the master problem constraints.
            gamma (list or np.ndarray): Dual variables for additional constraints.
            eta (list or np.ndarray): Dual variables for further constraints.
            subprob (int): Index or identifier of the subproblem being solved.
            fixed_delta (Any): Fixed values for delta variables in the pricing problem.
            fixed_mu (Any): Fixed values for mu variables in the pricing problem.
            pricing_formulation (int): Indicates which pricing formulation to use (e.g., 0, 1, -1, 2).
            branching_decisions (Any): Branching decisions to be enforced in the pricing model.
            mu_dual_contribution (float): Contribution of mu duals to the reduced cost.
            given_delta (Any): Delta values provided externally for the pricing problem.
            optimal (bool, optional): If True, solves the pricing problem to optimality. Defaults to False.
        Returns:
            dict: A dictionary containing the result of the pricing problem, including:
                - "result": Status of the pricing (e.g., SCIP_RESULT.DIDNOTRUN, INFEASIBLE, DIDNOTFIND).
                - "objval": Objective value(s) of the solution(s) found.
                - "pricing_formulation": The formulation used.
                - "subprob": The subproblem index.
                - "fixed_redcost_contribution": The fixed part of the reduced cost.
                - "given_delta": The delta values used.
                - Additional keys depending on the solution and maintenance cost extraction.
        Raises:
            Exception: Propagates exceptions from underlying model creation or optimization routines.
        Notes:
            - The method supports dual stabilization and may recursively call itself for stabilized duals.
            - Handles different pricing formulations and their impact on reduced cost calculation.
            - Solution filtering is performed based on reduced cost thresholds.
            - Updates internal statistics and bounds relevant to the column generation process.
        """
        pricing_model = create_model(farkas=self.farkas, 
                                pi=pi,
                                gamma=gamma,
                                eta=eta,
                                subprob=subprob,
                                fixed_delta=fixed_delta,
                                fixed_mu=fixed_mu,
                                params=self.data["params"],
                                pricing_formulation=pricing_formulation,
                                branching_decisions=branching_decisions)

        if pricing_formulation != 0:
            fixed_redcost_contribution = pi[0] # only convexity constraint in most cases, except PP1, where it's also the dual of the fixed mu
        else:
            fixed_redcost_contribution = 0 # mu's don't show up in the convexity constraints

        if pricing_formulation == 1:
            fixed_redcost_contribution += mu_dual_contribution

        # valid cut
        # need to be careful with these cuts, because t
        # if pricing_formulation == -1 and self.n_subprobs == 1:
        #     obj = pricing_model.getObjective()
        #     pricing_model.addCons(self.data["params"]["machines_per_group"][0] * obj <= self.model.getPrimalbound() - self.model.getLPObjVal())

        pricing_model.data = {}
        pricing_model.data["objLim_stop"] = False

        # TODO: check whether you can now enable setObjlimit
        if False:
            pricing_model.setObjlimit(convexity_redcost) # we're subtracting the convexity redcost later

        if not optimal:
            pricing_model.setParam("limits/gap", 0.05) # maybe this is too large
            pricing_model.setParam("limits/solutions", 3)

            time_left = self.compute_time_left()
            if time_left <= 0:
                return {"result": SCIP_RESULT.DIDNOTRUN}

            pricing_model.setParam("limits/time", time_left)

            if self.data["params"]["verbose"] <= 4:
                pricing_model.hideOutput()

            pricing_model.optimize()

            # if objective limit is hit
            objlimit_hit = False
            if False and self.model.getStage() == SCIP_STAGE.SOLVED and not self.isInfinity(self.model.getPrimalbound()):
                objlimit_hit = True

            # might be able to use this in conjunction with setObjlimit() now
            if False and pricing_model.getNSolsFound() == 0 and not objlimit_hit:
                return {"result": SCIP_RESULT.INFEASIBLE}

        # should probably just refactor this
        # misprice. just solving it to optimality
        if self.data["params"]["dual_stabilization"] and not self.farkas:
            if pricing_formulation == 0: # todo: while the benefit is dubious for ORMP, for the continuous pricing problem stabilization should be a game changer
                pass

            if self.model.isLT(pricing_model.getPrimalbound(), -self.dualfeastol):
                self.misprice[subprob] = max(0, self.misprice[subprob] - 1)
                self.alpha             = min(MAX_ALPHA, self.alpha * ALPHA_RATE_OF_CHANGE)
            else:
                self.misprice[subprob] += 1
                self.alpha             /= ALPHA_RATE_OF_CHANGE
                stabilized_duals = self.get_stabilized_duals()
                pi, gamma, eta, mu_dual_contribution = self.get_duals_for_pricing(pricing_formulation, stabilized_duals, subprob, given_delta, fixed_delta, fixed_mu)
                self.optimize_pricing_problem(pi, gamma, eta, subprob, fixed_delta, fixed_mu, pricing_formulation, branching_decisions, mu_dual_contribution, given_delta, optimal=True)
        
        # solving to optimality
        if pricing_model.getStatus() not in ["optimal", "infeasible"] and (optimal or self.model.isInfinity(pricing_model.getPrimalbound()) or self.model.isGE(pricing_model.getPrimalbound() - fixed_redcost_contribution, -self.dualfeastol)):
            pricing_model.setParam("limits/gap", 0.01)
            pricing_model.setParam("limits/solutions",-1)
            # pricing_model.writeProblem("test.cip")
            pricing_model.optimize()
            if pricing_model.getStatus() not in ["optimal", "infeasible"] and (optimal or self.model.isInfinity(pricing_model.getPrimalbound()) or self.model.isGE(pricing_model.getPrimalbound() - fixed_redcost_contribution, -self.dualfeastol)):
                pricing_model.setParam("limits/gap", 0)
                pricing_model.setParam("limits/solutions",-1)
                pricing_model.optimize()

        self.optimal_cols += 1
        # self.redcosts[subprob] = pricing_model.getPrimalbound() - fixed_redcost_contribution
        
        if self.data["model"] == 0:
            sols = pricing_model.getSols()
        elif self.data["model"] == 2:
            sols = [pricing_model.getBestSol()] # Just trying out keeping the RMP as small as possible with ARMP

        if len(sols) == 0:
            if pricing_formulation in [-1,2]:
                return {"result": SCIP_RESULT.INFEASIBLE, "pricing_formulation": pricing_formulation}
            elif pricing_formulation in [0,1]:
                return {"result": SCIP_RESULT.DIDNOTFIND, "pricing_formulation": pricing_formulation}
            else:
                raise ValueError("Invalid formulation")

        threshold = -self.dualfeastol
        if pricing_formulation == 0: # stricter limit for continuous pricing
            threshold *= 1000
        elif pricing_formulation == 1:
            threshold *= 10
        sols = [s for s in sols if self.model.isLE(pricing_model.getSolObjVal(s) - fixed_redcost_contribution, threshold)]

        # if no negative redcost solution found, return
        if sols == []:
            return {"result": SCIP_RESULT.DIDNOTFIND, "objval": [pricing_model.getPrimalbound()], "pricing_formulation": pricing_formulation}
        
        # trying to get better bounds
        if not self.farkas and pricing_formulation in [-1,2] and pricing_model.getNSols() > 0:
            # TODO think of what happens in all different cases. should we only set this if we have a negative redcost? probably, and otherwise the bound changes by 0
            self.explored_subproblems[subprob] = 1
            self.lagrangian_bound += min(0,self.data["params"]["machines_per_group"][subprob]*(pricing_model.getDualbound()-fixed_redcost_contribution))

        result: dict[str, Any] = self.get_sols_maintenance_cost(sols=sols, pricing_model=pricing_model, subprob=subprob, pricing_formulation=pricing_formulation)

        # if self.data["params"]["verbose"] >= 3:
        #     self.print_redcost_info(subprob=subprob, best_obj=result["objval"][0]-fixed_redcost_contribution, pricing_formulation=pricing_formulation)

        result["subprob"]                    = subprob
        result["pricing_formulation"]        = pricing_formulation
        result["fixed_redcost_contribution"] = fixed_redcost_contribution
        result["given_delta"]                = given_delta
        
        return result

    def handle_heuristic(self, pricing_formulation, cur_node_number, subprob, pi, gamma, eta, heuristic):
        heuristic_found_sol = False

        # trying the heuristic first
        heur1_start_time = time()
        cur_perturbation = -0.1
        cur_tries = 0

        result = {"heuristic_found_sol": False}
        while not heuristic_found_sol and cur_tries < N_HEURISTIC_TRIES: # should be a parameter
            cur_tries += 1
            cur_perturbation += 0.01 # this randomizes the duals a little bit

            result = self.solve_pricing_heuristically(
                cur_perturbation=cur_perturbation,
                pricing_formulation=pricing_formulation,
                cur_node_number=cur_node_number,
                subprob=subprob,
                pi=pi,
                gamma=gamma,
                eta=eta
            )

            if result["heuristic_found_sol"]:
                heuristic_found_sol = True

        self.data["discriminated_heur_time"][2] += time() - heur1_start_time
        return result
    
    def solve_pricing_heuristically(self, cur_perturbation, pricing_formulation, cur_node_number, subprob, pi, gamma, eta) -> dict: 

        if pricing_formulation != 0:
            fixed_redcost_contribution = pi[0]

        result = {"heuristic_found_sol": False}
        heuristic_model = PFHeuristic(model=self.model, farkas=self.farkas, optimal=False, pricing_formulation=pricing_formulation, optimize_production=True, params=self.data["params"], subprob=subprob, pi=pi, gamma=gamma, eta=eta, cur_perturbation=cur_perturbation)
        heuristic_result, vars = heuristic_model.get_column_given_production(self.data["branching_decisions"][cur_node_number][subprob], gamma)
        if self.model.isLT(heuristic_result - fixed_redcost_contribution, -self.dualfeastol - 0.1): # being a bit harsher with the heuristic
            if self.data["params"]["heuristic"] == 2:
                self.found_negative_redcost = True

            self.data["heuristics"]["success"] += 1

        result = {
            "objval": [heuristic_result],
            "vars": [vars],
            "mu_patterns": [{}],
            "delta_patterns": [{}],
            "heuristic_found_sol": True,
            "pricing_formulation": pricing_formulation,
            "fixed_redcost_contribution": pi[0] if pricing_formulation != 0 else 0,
            "maintenance_cost": [int(vars["total_cost"])] # numerics
        }

        # We have the option of trying to get the optimal maintenance given a fixed production
        if False:#heuristic_result > 0:
            heuristic_result, vars = get_column_given_production(optimal=True,params=self.data["params"],subprob=cur_subprob, pi=cur_dualSolutions)

        self.data["heuristics"]["total"] += 1
        return result

    # Solves pricing problem (-1 to 2) and prepares to add column to RMP
    def _solve_pricing(self, subprob, dualSolutions, reopt, heuristic, pricing_formulation, given_delta, given_mu, old_delta=None) -> dict:
        """
        Solves the various pricing problems of the different formulations
        parameters:
                    :subprob: subproblem number
                    :dualSolutions: values for the dual variables of the current iteration of the RMP
                    :lagrangian_bound: shared variable between subproblem for MP lower bound 
                    :heuristic: combination of heuristics to be used (1 for exact pricing)
                    :found: boolean indicating whether negative redcost column was found
                    :farkas: boolean indicating whether we are doing farkas" pricing
                    :formulation: which pricing problem should we solve? (-1 for original, 0 for production, 1 for maintenance, 2 for full)  
        """

        # Dual Stabilization
        # for c in dualSolutions["demand_duals"]:
        #     dualSolutions["demand_duals"][c] = fmean(c[-5:])

        if pricing_formulation == 0:
            assert given_delta != -1, "PP 0 needs to be given a discrete pattern!" 

        # Getting duals of the relevant subprob for current node
        cur_node_number = self.model.getCurrentNode().getNumber()

        pi, gamma, eta, mu_dual_contribution = self.get_duals_for_pricing(pricing_formulation=pricing_formulation,
                                                                          dualSolutions=dualSolutions,
                                                                          subprob=subprob,
                                                                          given_delta=given_delta,
                                                                          old_delta=old_delta,
                                                                          given_mu=given_mu)
        heuristic_result = float("inf")
        heuristic_vars = {}
        heuristic_found_sol = False
        if heuristic % 2 == 0:
            if any(pi):
                heuristic_result = self.handle_heuristic(pricing_formulation=pricing_formulation,
                                    cur_node_number=cur_node_number,
                                    subprob=subprob,
                                    pi=pi,
                                    gamma=gamma,
                                    eta=eta,
                                    heuristic=heuristic)
            else:
                heuristic_result = {"heuristic_found_sol": False, "objval": [float("inf")], "vars": [{}]}
        
            return heuristic_result

        if heuristic == 1 or not heuristic_found_sol or self.model.isGE(heuristic_result,0) or ''.join(str(heuristic_vars)) in self.data["pattern_encoding"][subprob]:
            self.data["exact_pricing_start_time"] = time()

            # we need to be careful about passing the right duals
            if pricing_formulation == 0:
                fixed_delta = self.data["Delta_patterns"][subprob][given_delta]
            else:
                fixed_delta = {}

            if pricing_formulation == 1:
                fixed_mu = self.data["Mu_patterns"][subprob][old_delta][given_mu]
            else:
                fixed_mu = {}

            branching_decisions = self.get_branching_decision(cur_node_number, subprob)
            
            
            result = self.optimize_pricing_problem(
                pi=pi, 
                gamma=gamma,
                eta=eta,
                subprob=subprob,
                given_delta=given_delta,
                fixed_delta=fixed_delta,
                fixed_mu=fixed_mu,
                pricing_formulation=pricing_formulation,
                branching_decisions=branching_decisions,
                mu_dual_contribution=mu_dual_contribution
            )

            return result

    def get_sols_maintenance_cost(self, sols, pricing_model, pricing_formulation, subprob):
        try:
            return self._get_sols_maintenance_cost(sols, pricing_model, pricing_formulation, subprob)
        except Exception as e:
            log_error("get_sols_maintenace_cost", e, self.data["params"]["filename"], self.data["params"]["stop_at_error"])
            self.data["error"] = True
            return {"error": str(e)}
            
    # Get info from pricing run
    def _get_sols_maintenance_cost(self, sols, pricing_model, pricing_formulation, subprob):
        objval = {}
        vars = {}
        delta = {}
        mu = {}
        maintenance_cost = {}
        seen_deltas = []
        for i, s in enumerate(sols):
            obj = pricing_model.getSolObjVal(s)
            objval[i] = obj

            if pricing_formulation > -1:
                cur_mu = {}
                cur_delta = {}
                cur_maintenance_cost = 0
                for var in pricing_model.getVars():
                    if "m[" in var.name:
                        cur_delta[var.name]   = pricing_model.getSolVal(s, var) 
                        cur_component_name    = var.name.split(",")[1]
                        cur_component_cost    = self.data["params"][subprob].components[cur_component_name].C
                        cur_maintenance_cost += cur_delta[var.name]*cur_component_cost
                    elif "y" in var.name:
                        cur_mu[var.name] = pricing_model.getSolVal(s, var)
                    else:
                        continue

                cur_delta["maintenance_cost"] = cur_maintenance_cost
                maintenance_cost[i] = cur_delta["maintenance_cost"]

                mu[i] = cur_mu
                delta[i] = cur_delta
                # str_cur_delta = str(cur_delta)
                # if str_cur_delta not in seen_deltas:
                #     seen_deltas.append(str_cur_delta)
            else:
                cur_vars = {}
                cur_maintenance_cost = 0
                for var in pricing_model.getVars():
                    cur_vars[var.name] = pricing_model.getSolVal(s, var)
                    if "m[" in var.name:
                        # cur_vars[var.name] = self.model.feasFloor(cur_vars[var.name]) # numerics
                        cur_maintenance_var = cur_vars[var.name]
                        if self.model.isGT(cur_maintenance_var, 0):
                            component_name = var.name.split(",")[1]
                            component=self.data["params"][subprob].components[component_name]
                            cur_maintenance_cost += cur_vars[var.name]*component.C
                maintenance_cost[i] = self.model.feasFloor(cur_maintenance_cost)

                vars[i] = cur_vars
                vars[i]["total_cost"] = cur_maintenance_cost
                vars[i]["maintenance_cost"] = cur_maintenance_cost
                mu[i] = None
                delta[i] = cur_vars
                # str_cur_vars = str(cur_vars)
                # if str_cur_vars not in seen_deltas:
                #     seen_deltas.append(str_cur_vars)

        result = {
            'objval'             : objval,
            'vars'               : vars,
            'maintenance_cost'   : maintenance_cost,
            'mu_patterns'        : mu,
            'delta_patterns'     : delta,
            'pricing_formulation': pricing_formulation
        }

        return result

    # helper functions
    def check_column_feasibility(self, subprob, vars):
        # if self.data["params"]["debug_mode"]:
        #     import create_model_w_cons_names
        #     local_model = create_model_w_cons_names.create_model(subprob=subprob, pi={i:0 for i in self.data["params"]["T_prime"]}, params=self.data["params"], pricing_formulation=-1)
        # else:
        local_model = create_model(subprob=subprob, pi={i:0 for i in self.data["params"]["T_prime"]}, params=self.data["params"], pricing_formulation=-1)
        local_model.setParam("numerics/feastol", 1e-5) # being a bit more lenient, as SCIP itself sometimes returns slightly infeasible solutions
        local_sol = local_model.createSol()
        for var in local_model.getVars():
            # if self.model.isEQ(vars[var.name], self.model.feasFloor(vars[var.name])):
            #     vars[var.name] = self.model.feasFloor(vars[var.name])  # rounding due to numerics (-1e-15 might lead to complex numbers)
            local_model.setSolVal(local_sol, var, vars[var.name])

        column_feasible = local_model.checkSol(local_sol, completely=True, original=True, printreason=True)
        return column_feasible

    def compute_time_left(self):
        # because the time might be slightly negative
        time_limit = self.data["params"]["time_limit"]
        return min(time_limit, max(0, time_limit - (time() - self.data["params"]["start_time"])))

    def get_branching_decision(self, node_number, subprob, branching_index=None):
        if branching_index is None:
            return self.data["branching_decisions"][node_number][subprob]
        else:
            return self.data["branching_decisions"][node_number][subprob][branching_index]
    
    def get_n_branching_decisions(self, node_number, subprob):
        return len(self.data["branching_decisions"][node_number][subprob])
    
    def get_branching_cons(self, node_number, subprob, index):
        return self.data["branching_cons"][node_number][subprob][index]
    
    def set_branching_decision(self, node_number, subprob, branching_index, decision: BranchingDecision):
        if branching_index == -1:
            branching_index = len(self.data["branching_decisions"][node_number][subprob])
        self.data["branching_decisions"][node_number][subprob][branching_index] = decision

    def set_branching_cons(self, node_number, subprob, cons, branching_index=None):
        if not branching_index:
            self.data["branching_cons"][node_number][subprob] = [cons]
        else:
            self.data["branching_cons"][node_number][subprob][branching_index] = cons
    
    def var_in_branching_cons(self, var, branching_decision):
        return var.name in [v.name for v in self.model.getConsVars(branching_decision.branching_con)]

    def patterns_compatible(self, delta_pattern: dict, mu_pattern: dict) -> bool:
        """
        Compatible iff no time period has both maintenance and production (bitwise AND == 0).
        """
        return (self.ARMP_encode_delta_pattern(delta_pattern) & self.ARMP_encode_mu_pattern(mu_pattern)) == 0

    def visualize_tree(self):
        """
        Visualizes the branch-and-price tree using matplotlib and networkx.
        Displays the order of visited nodes and the local dual bounds at each node.
        """
        import networkx as nx
        import matplotlib.pyplot as plt

        # Create a directed graph
        tree = nx.DiGraph()
        nodes_visited = self.data["nodes_visited"]
        local_dual_bounds = self.data["local_dual_bounds"]

        # Add nodes and edges
        for parent, current in nodes_visited:
            tree.add_node(current)
            if parent is not None:
                tree.add_edge(parent, current)

        # Generate positions for the nodes in a tree layout
        pos = nx.drawing.nx_agraph.graphviz_layout(tree, prog="dot")

        # Create the figure and subplots
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))

        # Left plot: Order of visited nodes
        axes[0].set_title("Order of Visited Nodes")
        nx.draw_networkx_edges(tree, pos, ax=axes[0], arrows=True)  # Draw edges
        nx.draw_networkx_labels(tree, pos, ax=axes[0], font_size=8, font_color="black")  # Draw labels
        axes[0].axis("off")  # Remove axes

        # Right plot: Local dual bounds
        axes[1].set_title("Local Dual Bounds")
        nx.draw_networkx_edges(tree, pos, ax=axes[1], arrows=True)  # Draw edges
        nx.draw_networkx_labels(
            tree, pos, ax=axes[1],
            labels={node: f"{local_dual_bounds.get(node, 'N/A'):.2f}" if isinstance(local_dual_bounds.get(node), (int, float)) else local_dual_bounds.get(node, 'N/A') for node in tree.nodes()},
            font_size=8, font_color="black"
        )  # Draw labels with local dual bounds
        axes[1].axis("off")  # Remove axes

        # Show the plots
        plt.tight_layout()
        plt.show()
    
    def _fmt_time(self, seconds: float) -> str:
        """Format seconds as HH:MM:SS.mmm."""
        seconds = float(seconds or 0.0)
        h, rem = divmod(seconds, 3600.0)
        m, s = divmod(rem, 60.0)
        return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

    def print_pricing_timings(self):
        times = {
            "Exact pricing":        self.data.get("exact_pricing_time", 0.0),
            "Branching":            self.data.get("branching_time", 0.0),
            "Integer RMP":          self.data.get("integer_rmp_time", 0.0),
            "Heuristics":           self.data.get("heuristic_time", 0.0),
            "Python (overhead)":    self.data.get("python_time", 0.0),
            "Master (reopt)":       self.data.get("master_time", 0.0),
        }
        total = sum(times.values())

        width = 46
        print("\n" + "-" * width)
        print(f"{'Pricing time breakdown':^{width}}")
        print("-" * width)
        print(f"{'Stage':<24}{'Time':>14}{'%':>6}")
        print("-" * width)
        for k, v in times.items():
            pct = (100.0 * v / total) if total > 0 else 0.0
            print(f"{k:<24}{self._fmt_time(v):>14}{pct:>6.1f}")
        print("-" * width)
        print(f"{'Total':<24}{self._fmt_time(total):>14}{(100.0 if total>0 else 0.0):>6.1f}")
        print("-" * width)

# Initialize MP and Pricer
def create_pricer(params=params):
    """
    Initializes and configures the master problem and pricer for machine maintenance scheduling using column generation.
    This function sets up the required data structures, encodings, and parameters for the pricer and master problem,
    including objective scaling, branching rules, event handlers, and auxiliary statistics. It supports multiple model
    types (original and alternative master problem formulations) and prepares the environment for solving the
    scheduling problem with advanced branching and pricing strategies.
    Args:
        params (dict): Dictionary containing all model parameters, including:
            - "machines_per_group": List specifying the number of machines in each group.
            - "model": Integer indicating the model type (e.g., 0 for original, 2 for alternative).
            - "T": List of time periods.
            - "T_prime": List of maintenance time periods.
            - "compact_run": Boolean flag for compact initialization.
            - "time_limit": Time limit for solving.
            - "verbose": Verbosity level for logging.
            - Other problem-specific parameters.
    Returns:
        tuple:
            - master_problem: The initialized master problem object, ready for solving.
            - pricer: The configured pricer object containing all necessary data and settings for column generation.
    Raises:
        ValueError: If an invalid model number is provided in params["model"].
    Notes:
        - The function disables presolve, separating, and propagation in the master problem to ensure proper duality handling.
        - Branching rules and event handlers are included to support advanced branching strategies.
        - Objective coefficients are scaled by their greatest common divisor for better bound tightening.
        - The pricer object is populated with extensive auxiliary data for tracking statistics, branching decisions, and solution progress.
    """
    n_subprobs = len(params["machines_per_group"])

    # The columns will be stored here
    X = {i: {} for i in range(n_subprobs)}
    Delta = {i: {} for i in range(n_subprobs)}
    Mu = {i: {} for i in range(n_subprobs)} # will then have a set of columns per delta    

    if params["model"] == 0:
        Delta = {i: [1] for i in range(n_subprobs)}

    # Scaling the objective
    import math
    component_costs = []
    for subprob in range(n_subprobs):
        for k in params[subprob].components.values():
            component_costs.append(int(k.C))

    gcd = math.gcd(*component_costs)
    for subprob in range(n_subprobs):
        for k in params[subprob].components.values():
            if gcd == 0:
                gcd = 1
                break
            k.C/=gcd
    
    if params["verbose"] >= 1 and gcd > 1:
        print("Scaling objective by %i" % gcd)

    # master_problem will coordinate the subproblems. 
    if params["model"] == 0:
        master_problem, convexity_cons, demand_cons = master_model(X,params=params)
    elif params["model"] == 2:
        master_problem, convexity_cons, compatibility_cons, demand_cons = alternative_master_problem(Delta, Mu, params=params)
    else:
        raise ValueError("Invalid model number")

    master_vars = master_problem.getVars()

    master_problem.setParam("limits/time", params["time_limit"])

    pricer = CutPricer(n_subprobs=n_subprobs)
    master_problem.includePricer(
        pricer, "Pricer for machine maintenance scheduling", "Pricer to identify patterns for machine maintenance scheduling")
    
    if params["verbose"] >= 4:
        master_problem.setParam("display/lpinfo", True)

    # Setting the pricer data
    pricer.n_subprobs = len(params["machines_per_group"])
    if pricer.n_subprobs == 1:
        pricer.ordered_subprobs = [0]

    # Set initialize_with_compact based on average subproblem size
    avg_subprob_size = sum(params["machines_per_group"]) / len(params["machines_per_group"])
    pricer.initialize_with_compact = params["compact_run"] and (avg_subprob_size <= MAX_SUBPROB_SIZE_FOR_COMPACT_INITIALIZATION)

    pricer.data = {}
    if params["model"] == 0:
        pricer.data["convexity_cons"]     = convexity_cons
        pricer.data["demand_cons"]        = demand_cons
        pricer.data["compatibility_cons"] = {i: {} for i in range(n_subprobs)}
        pricer.data["branching_cons"]     = {}
        pricer.data["del_vars"]           = {i: [] for i in range(n_subprobs)}
    elif params["model"] == 2:
        pricer.data["convexity_cons"]     = convexity_cons
        pricer.data["compatibility_cons"] = compatibility_cons
        pricer.data["demand_cons"]        = demand_cons
        pricer.data["branching_cons"]     = {}
        pricer.data["del_vars"]           = {i: [] for i in range(n_subprobs)}

    pricer_vars = {i: {} for i in range(n_subprobs)}
    if params["model"] == 0:
        pricer.data["var"]        = pricer_vars
        pricer.data["young_vars"] = pricer_vars # removing old variables
        pricer.data["patterns"]   = X
        pricer.data["full_patterns"] = X
        pricer.data["pattern_encoding"] = [{} for _ in range(n_subprobs)]
    elif params["model"] == 2:
        pricer.data["mu_encoding"]         = [{} for _ in range(n_subprobs)]   # (delta_name, mu_key) -> [mu_var_names]
        pricer.data["mu_encoding_rev"]     = [{} for _ in range(n_subprobs)]   # mu_var_name -> (delta_name, mu_key)
        pricer.data["delta_encoding"]      = [{} for _ in range(n_subprobs)]   # delta_key -> [delta_var_names]
        pricer.data["delta_encoding_rev"]  = [{} for _ in range(n_subprobs)]   # delta_var_name -> delta_key
        pricer.data["all_delta_patterns"] = {}
    else:
        raise ValueError("Invalid model")

    # only relevant for ARMP. adding to ORIG as well to avoid code duplication
    pricer.data["Delta_patterns"] = {i: {} for i in range(n_subprobs)}
    pricer.data["Mu_patterns"]    = {i: {} for i in range(n_subprobs)}
    pricer.data["Delta"]          = Delta
    pricer.data["Mu"]             = Mu

    # to facilitate lookup
    pricer.data["integer_patterns"]             = {}
    pricer.data["integer_encoding"]             = {i: {} for i in range(n_subprobs)}
    pricer.data["continuous_patterns"]          = {i: {} for i in range(n_subprobs)}
    pricer.data["continuous_encoding"]          = {i: {} for i in range(n_subprobs)}
    pricer.data["discrete_production_pattern"]  = {i: {} for i in range(n_subprobs)}
    pricer.data["discrete_production_encoding"] = {i: {} for i in range(n_subprobs)}
    pricer.data["filtered_mvars"]               = {i: {} for i in range(n_subprobs)}
    for i in range(n_subprobs):
        for t in params["T"]:
            for k in params[i].components.values():
                component_name = k.name
                cur_var_name = "m[0,%s,%i]" % (component_name, t)
                pricer.data["filtered_mvars"][i][cur_var_name] = []

        pricer.data["filtered_mvars"][i]["maintenance_cost"] = []
        for t in params["T_prime"]:
            pricer.data["filtered_mvars"][i]["y[0,%i]" % t] = []

    # Dual stabilization
    pricer.stabilized_duals = {} # todo

    # Redcost fixing
    pricer.data["n_redcost_fixings"]        = {1: 0}
    pricer.data["n_strong_redcost_fixings"] = {1: 0}
    pricer.data["optimal_duals"]            = {}
    pricer.data["redcost_fixed_vars"]       = {1: {}} # because you can't get ubs of different nodes, so you need to skip the vars differently

    # settings and auxiliary data
    pricer.break_early                     = {}
    pricer.n_subprobs                      = n_subprobs
    pricer.explored_subproblems            = {i: 0 for i in range(n_subprobs)}
    pricer.data["params"]                  = params
    pricer.data["iterations_since_last"]   = {i: 0 for i in range(n_subprobs)}
    pricer.data["model"]                   = params["model"]
    pricer.data["previous_redcosts"]       = {i:[] for i in range(n_subprobs)}
    pricer.data["straight_subprobs"]       = [-1,-1]

    # Branching
    pricer.data["branching_decisions"]            = {1:{i: [] for i in range(-1, n_subprobs)}}
    pricer.data["last_branching"]                 = {1: BranchingDecision("")}
    pricer.data["early_branch"]                   = {}
    pricer.data["repaired_variables"]             = {i: [] for i in range(pricer.n_subprobs)} # Were columns produced during branching?
    pricer.data["integrality_check"]              = defaultdict(int)
    pricer.data["optimal_sol_is_repaired"]        = False
    pricer.data["implicit_integer_sol"]           = {1: {}}
    pricer.data["implicit_integer_sol_vals"]      = {}
    pricer.best_sol                               = {"obj": master_problem.infinity()}
    pricer.data["mvars_by_integer_variable"]      = {i: defaultdict(list) for i in range(n_subprobs)}
    pricer.data["node_depth"]                     = {1: 0} # depth of unexplored nodes, to switch to bfs
    pricer.data["bfs"]                            = 0
    pricer.data["lpsol"]                          = {} # to fix the issue with pseudo solution branching

    # ARMP
    pricer.data["n_straight_0_pricing_rounds"] = {i: 0 for i in range(n_subprobs)} 
    pricer.data["n_straight_1_pricing_rounds"] = {i: 0 for i in range(n_subprobs)}

    # statistics
    pricer.data["bound"]                   = [-float("inf")]
    pricer.data["gcd"]                     = gcd 
    pricer.data["redcost"]                 = []
    pricer.data["heuristics"]              = {"total": 0, "success": 0}
    pricer.data["discriminated_heur_time"] = {2: 0}
    pricer.data["incumbent"]               = [float("inf")]
    pricer.data["setup time"]              = 0
    pricer.data["nodes_visited"]           = []
    pricer.data["local_dual_bounds"]       = {}
    pricer.primal_bound                    = master_problem.infinity()
    pricer.data["aggregatevarbound"]       = {
                                                "n_calls": 0,
                                                "n_successes": 0,
                                                "time": 0
                                             }
    pricer.data["disaggregate"]            = {
                                                "n_calls": 0,
                                                "n_successes": 0,
                                                "time": 0
                                            }
    pricer.data["single"]                   = {
                                                "n_calls": 0,
                                                "n_successes": 0,
                                                "time": 0
                                            }
    pricer.data["repair_step"]              = {
                                                "n_calls": 0,
                                                "n_successes": 0,
                                                "time": 0
                                            }

    # timings
    pricer.data["master_start_time"]       = time()
    pricer.data["master_time"]             = 0
    pricer.data["end_pricing_time"]        = 0
    pricer.data["start_branching_time"]    = 0
    pricer.data["end_branching_time"]      = 0
    pricer.data["branching_time"]          = 0
    pricer.data["integer_rmp_time"]        = 0
    pricer.data["exact_time"]              = 0
    pricer.data["python_time"]             = 0
    pricer.data["heuristic_time"]          = 0
    pricer.data["exact_pricing_time"]      = 0
    pricer.data["branching_start"]         = 0
    # Unified callback anchor to account master time slices between callbacks
    pricer.data["last_callback_end"]       = pricer.data["master_start_time"]
    
    # misc (some can be deleted)
    pricer.data["deactivate"]              = {1:False} # for price and branch heuristic
    pricer.data["pseudo_branching"]        = {1:()}
    pricer.data["seen_nodes"]              = {}
    pricer.data["infeasibilities"]         = {}
    pricer.data["added_local_constraints"] = {1: True}
    pricer.data["buggy_heuristic"]         = 0
    pricer.data["objLim_stop"]             = False
    pricer.data["compact_model"]           = { # to resume compact model runs when feasibility is hard
                                                "model": None,
                                                "time": 0,
                                                "n_solutions": 0,
                                            }
    pricer.compact_found_sol               = False
    if params["model"] == 0:
        for subprob in pricer.data["patterns"]:
            pricer.data["patterns"][subprob][-1] = {} # for initialization purposes in the heuristic
    elif params["model"] == 2:
        pass # still need to think what the heuristic will do here
    else:
        raise ValueError("Invalid model")

    # useful for closing nodes after finding repaired solution
    pricer.data["nodes"] = {}
    pricer.data["closed_nodes"] = {}

    data_any = cast(Dict[str, Any], master_problem.data) # To access pricer data from the branching rule
    data_any["pricer"] = pricer 

    # Initializing the auxiliar original formulation to avoid solving PP2 in ARMP
    if params["model"] == 2:
        pricer._initialize_aux_ORMP()

    # Starting the solving process
    # Must disable some settings in order to use duality properly
    master_problem.setPresolve(SCIP_PARAMSETTING.OFF)
    master_problem.setSeparating(SCIP_PARAMSETTING.OFF)

    master_problem.disablePropagation()

    pricer.data["branching_rules"] = []

    # Branching on original variables (size must be one)
    pricingBranchingRule = PricingBranchingDisaggregate(master_problem)
    master_problem.includeBranchrule(pricingBranchingRule, "Pricing disaggregate branching rule", "Branches on original variables", 99999999, -1, 1)
    pricer.data["branching_rules"].append("disaggregate")

    pricingBranchingRule = PricingBranchingAggregateVarbound(master_problem)
    master_problem.includeBranchrule(pricingBranchingRule, "Pricing branching", "Branches on interger variable bounds", 9999999, -1, 1)
    pricer.data["branching_rules"].append("aggregate")

    pricer.data["branching_rules"].append("single")

    # if addConsNode is fixed, this isnt' needed
    pricingEventHdlr = PricingEventHdlr(master_problem)
    master_problem.includeEventhdlr(pricingEventHdlr, "Pricing Event handler", "Enforces branching decisions in master variables")

    return master_problem, pricer
