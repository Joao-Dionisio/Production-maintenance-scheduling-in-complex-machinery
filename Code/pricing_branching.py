import numpy as np
from pyscipopt import Branchrule, SCIP_RESULT, Eventhdlr, SCIP_EVENTTYPE, quicksum, Constraint, Model
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import defaultdict
from copy import copy, deepcopy
from scipy.stats import median_abs_deviation
import random
import time
from testing import log_error
import heapq
from typing import Union
import time

random.seed(0)

@dataclass
class BranchingDecision:
    branching_rule: str
    node_position: Optional[str] = None
    var_val: Optional[float] = None
    subprob: Optional[int] = None
    inequality: Optional[str] = None
    aggregate_master_vars: Optional[dict] = field(default_factory=dict)
    naggregate_master_vars: Optional[int] = None # just for record keeping
    branching_thresholds: Optional[list] = field(default_factory=list)
    branching_var_subprob: Optional[int] = None
    disaggregate_branching_var: Optional[str] = None
    single_master_var: Optional[Any] = None
    master_pattern: Optional[Any] = None
    master_var: Optional[Any] = None    
    branching_con: Optional[Constraint] = None


# @total_ordering
@dataclass(order=True)
class PriorityQueueItem:
    sort_index: tuple = field(init=False, repr=False)
    id: int
    score: tuple  # Priority queue will use this for sorting
    subset: Union[list, dict]
    n_thresholds: int
    subprob: int
    subset_sum: float
    thresholds: list

    def __post_init__(self):
        self.sort_index = (self.score, self.n_thresholds, -self.subset_sum, self.id)

# initializes branching (mostly to handle different models)
def branching_init(self, model):
    self.model = model
    self.pricer = model.data["pricer"]
    if self.pricer.data["model"] == 0:
        self.var_names = "var"
        self.patterns = "patterns"
        self.integer_patterns = "integer_patterns"
        self.integer_encoding = "integer_encoding"
    elif self.pricer.data["model"] == 2:
        self.var_names = "Delta"
        self.patterns = "Delta_patterns"
        self.integer_patterns = "all_delta_patterns"
        self.integer_encoding = "delta_encoding"
    else:
        raise ValueError

# Helper function to get branching decisions of parent
def get_parent_node_with_branching_decisions(self, node):
    """Traverse up the tree until finding a node originated one of our branching rules"""
    while node.getNumber() not in self.pricer.data["branching_decisions"]:
        node = node.getParent()
    return node, node.getNumber()

def initialize_branching_decisions(pricer, subprob, parent_decisions, downnr, upnr, down_branching, up_branching, branched_in_subprob=False):
    """
    Initialize branching decisions for the down and up nodes
    """

    pricer.data["branching_decisions"][downnr][subprob] = {}
    pricer.data["branching_decisions"][upnr][subprob]   = {}

    for branching_index in range(len(parent_decisions)):
        branching = parent_decisions[branching_index]
        if subprob == -1:
            for i in range(-1, pricer.n_subprobs):
                pricer.set_branching_decision(downnr, i, branching_index, branching)
                pricer.set_branching_decision(upnr, i, branching_index, branching)
        else:
            pricer.set_branching_decision(downnr, subprob, branching_index, branching)
            pricer.set_branching_decision(upnr, subprob, branching_index, branching)

    if branched_in_subprob:
        if subprob == -1:
            for i in range(-1, pricer.n_subprobs):
                pricer.set_branching_decision(downnr, i, -1, down_branching)
                pricer.set_branching_decision(upnr, i, -1, up_branching)
        else:
            pricer.set_branching_decision(downnr, subprob, -1, down_branching)
            pricer.set_branching_decision(upnr, subprob, -1, up_branching)

        pricer.data["last_branching"][downnr] = down_branching
        pricer.data["last_branching"][upnr]   = up_branching

    return

def print_branching_info(pricer, rule, var_to_branch_on_name=None, var_val=None, all_chosen_thresholds=[], sum_vars_satisfying_threshold=0, subprob=None, last_subprob=False, n_repaired_variables=None):
    if not pricer.data["params"]["debug_mode"] or not pricer.data["params"]["verbose"] >= 3:
        return

    if subprob == 0:
        print("\n")

    if rule == "single":
        print("\nSingle var branching\n")
    elif rule == "disaggregate":
        print("\nDisaggregate: Branched on %s = %f\n" % (var_to_branch_on_name, var_val))
    elif rule == "aggregatevarbounds":
        if len(all_chosen_thresholds) > 0:
            print("Aggregate subprob %i: Branched on %s. Current sum: %f" % (subprob, str(all_chosen_thresholds), sum_vars_satisfying_threshold))
        else:
            print("Branched on convexity constraints in subproblem %i. Current sum: %f" % (subprob, sum_vars_satisfying_threshold))
    elif rule == "repair_step":
        print("Repaired %i variables in subproblem %i." % (n_repaired_variables, subprob))

    if last_subprob:
        print()

    return

# Class constants
DOWN_PRIORITY = 100
UP_PRIORITY   = 100
class PricingBranchingAggregateVarbound(Branchrule):
    """
    Performs branching on pricing variable bounds, as described in the branch and price GOK book.
    """

    def __init__(self, model):
        self.model: Model
        self.pricer: Any
        self.var_names: str
        self.patterns: str
        self.integer_patterns: str
        self.integer_encoding: str
        branching_init(self, model)

    def branchexeclp(self, allowaddcons=False):
        start_branching_time = time.time()
        # Attribute master time slice since last callback up to this branching callback
        last_end = self.pricer.data.get("last_callback_end", self.pricer.data.get("master_start_time", start_branching_time))
        self.pricer.data["master_time"] += max(0.0, start_branching_time - last_end)
        result = self._branchexeclp(allowaddcons)
        branching_end = time.time()
        self.pricer.data["end_branching_time"] = branching_end
        self.pricer.data["branching_time"] += (branching_end - start_branching_time)
        # Update unified callback anchor
        self.pricer.data["last_callback_end"] = branching_end
        return result

        # except Exception as e:
        #     log_error("aggregatevarbound_exec", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
        #     self.pricer.data["error"] = True
        #     return {"error": str(e)}
        
    def _branchexeclp(self, allowaddcons=False) -> dict:
        if not self.pricer.data["lpsol"]:
            for subprob in range(self.pricer.data["params"]["n_groups"]):
                for mvar_name, mvar in self.pricer.data[self.var_names][subprob].items():
                    self.pricer.data["lpsol"][mvar_name] = self.model.getSolVal(sol=None, expr=mvar)

        self.pricer.data["aggregatevarbound"]["n_calls"] += 1

        self.pricer.data["branching_start"] = time.time()

        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()
        self.pricer.data["deactivate"][cur_node_number] = False

        var_threshold_dict = self.find_var_threshold()

        # Branched in case of success, Cutoff in case of repaired solution
        result = self.perform_branching(var_threshold_dict)

        self.pricer.data["aggregatevarbound"]["n_successes"] += 1

        self.pricer.data["lpsol"] = {} # freeing lpsol for next branching

        return result

    def solvepriceandbranch(self):
        """
        Deactivates pricer and optimizes the RMP with the current columns.
        """
        self.model.deactivatePricer(self.pricer)
        for c in self.model.getConss():
            self.model.setModifiable(c, False)
        self.model.optimize()

    def find_var_threshold(self) -> dict:
        """
        Finds a list of integer variables and thresholds that split the fractional variables into two fractional sets.
        If no such list can be found, integrality check is passed and solution is integer in the compact space.
        """

        """
        Adding the non-zero fractional master variables. The idea here is that it's them that are more
        likely to be non-zero in the optimal MP solution and should thus be weighed more heavily when
        choosing a branching candidate.
        """
        # getting fractional master variables
        n_subprobs             = self.pricer.data["params"]["n_groups"]
        patterns               = self.pricer.data[self.integer_patterns]
        self.repaired          = {i: False for i in range(n_subprobs)}
        self.integral          = {i: False for i in range(n_subprobs)}
        self.variables_to_fix  = []
        self.integer_fractionalities = {i: [] for i in range(n_subprobs)}
        all_chosen_thresholds = {i: [] for i in range(n_subprobs)}
        all_chosen_branching_vars = {i : {} for i in range(n_subprobs)} # to avoid picking the same var
        sum_vars_satisfying_threshold = {i: 0 for i in range(n_subprobs)}
        mvar_dict = {}

        # fix: this suffers from the getVal issue already in the repo
        #mvar_dict              = self.model.getVarDict(transformed=True)

        result = self.collect_fractional_master_vars(self.pricer.data["lpsol"], n_subprobs)
        filtered_master_vars   = result["filtered_master_vars"]
        n_fractional_vars      = result["n_fractional_vars"]
        current_fractional_sum = result["current_fractional_sum"]
        current_total_sum      = result["current_total_sum"]

        # TODO: finish implementing the all variable sum to fractional number
        """
        # if sum of all variables is fractional
        if not self.model.isFeasIntegral(sum(current_total_sum.values())):
            result_dict = {"filtered_master_vars": {}, "all_chosen_thresholds": {}, "sum_vars_satisfying_threshold": {}}
            for i in range(n_subprobs):
                result_dict["filtered_master_vars"][i] = {}
                result_dict["all_chosen_thresholds"][i] = {}
                result_dict["sum_vars_satisfying_threshold"][i] = 0

            result_dict["filtered_master_vars"][-1] = copy(self.model.getVars(True))
            result_dict["all_chosen_thresholds"][-1] = {"all": []} # no thresholds, just the sum
            result_dict["sum_vars_satisfying_threshold"][-1] = sum(current_total_sum.values())
            return result_dict
        """

        # TODO: we're just going for the first subproblem that has fractional variables
        # TODO: need to pick better. maybe the one with more variables?
        for subprob in range(n_subprobs):
            if self.pricer.data["params"]["machines_per_group"][subprob] <= 1: # repeating here, already skipped before
                continue

            if n_fractional_vars[subprob] == 0:
                self.integral[subprob] = True # just to make it easier to check for repair branching
                continue
            
            # todo: also have the option to branch on variables across thresholds
            # We can also branch on the sum of all variables being fractional
            sum_vars_satisfying_threshold[subprob] = current_total_sum[subprob]
            if not self.model.isFeasIntegral(sum_vars_satisfying_threshold[subprob]):
                result_dict = {"filtered_master_vars": {}, "all_chosen_thresholds": {}, "sum_vars_satisfying_threshold": {}}
                for i in range(n_subprobs):
                    result_dict["filtered_master_vars"][i] = {}
                    result_dict["all_chosen_thresholds"][i] = {}
                    result_dict["sum_vars_satisfying_threshold"][i] = sum_vars_satisfying_threshold[i]

                result_dict["filtered_master_vars"][subprob] = copy(self.pricer.data[self.var_names][subprob])
                result_dict["all_chosen_thresholds"][subprob] = {"subprob": []} # no thresholds, just the sum
                result_dict["sum_vars_satisfying_threshold"][subprob] = sum_vars_satisfying_threshold[subprob]
                return result_dict

        # uses a priority queue to find hyperplane to branch on, or prove that none exists
        chosen_item = self.split_and_explore(filtered_master_vars, patterns)        

        # if we couldn't find any branching variable, then solution is optimal.
        if type(chosen_item) is list and chosen_item == [(False, float("inf"))]:
            assert all(self.integral.values()), "Some subproblems were either sucessfull or not explored"
            return {'result': SCIP_RESULT.SUCCESS}

        # collecting all variables satisfying the thresholds
        subprob = chosen_item.subprob
        chosen_item.subset = {}
        for mvar in self.pricer.data[self.var_names][subprob].values():
            if self.master_var_satisfies_threshold(mvar, chosen_item.thresholds, patterns):
                chosen_item.subset[mvar.name] = mvar

        return chosen_item

    def collect_fractional_master_vars(self, mvar_dict, n_subprobs):
        filtered_master_vars   = {i: {} for i in range(n_subprobs)}
        n_fractional_vars      = {i: 0 for i in range(n_subprobs)}
        current_fractional_sum = {i: 0 for i in range(n_subprobs)}
        current_total_sum      = {i: 0 for i in range(n_subprobs)}

        for subprob in range(n_subprobs):

            for master_var in self.pricer.data[self.var_names][subprob].values():
                master_var_name = master_var.name
                if self.model.isZero(mvar_dict[master_var_name]):
                    continue

                if not self.model.isFeasIntegral(mvar_dict[master_var_name]):
                    filtered_master_vars[subprob][master_var_name] = master_var
                    current_fractional_sum[subprob] += mvar_dict[master_var_name]
                    n_fractional_vars[subprob] += 1
                else:
                    current_total_sum[subprob] += mvar_dict[master_var_name]

            current_total_sum[subprob] += current_fractional_sum[subprob]
        
        if self.pricer.data["params"]["debug_mode"]:
            for subprob in range(n_subprobs):
                assert n_fractional_vars[subprob] == len(filtered_master_vars[subprob]), "Fractional vars count does not match filtered master vars count"
        
        result = {
            "filtered_master_vars": filtered_master_vars,
            "n_fractional_vars": n_fractional_vars,
            "current_fractional_sum": current_fractional_sum,
            "current_total_sum": current_total_sum
        }
        return result
                    
    def master_var_satisfies_threshold(self, master_var, chosen_thresholds, patterns):
        """
        Checks if the master variable satisfies the thresholds for the given branching variable.
        """

        cur_pattern = patterns[master_var.name]
        add_master_var = True
        for branching_var, inequality, new_threshold in chosen_thresholds:
            if inequality == "<=":
                if self.model.isGT(cur_pattern[branching_var], new_threshold):
                    add_master_var = False
                    break
            elif inequality == ">=":
                if self.model.isLT(cur_pattern[branching_var], new_threshold):
                    add_master_var = False
                    break
            else:
                raise ValueError("Something went wrong picking the thresholds")
        return add_master_var

    def split_and_explore(self, initial_set, patterns) -> PriorityQueueItem:
        """
        Dynamically splits subspaces in the RMP, gives them a score, and explores the most valuable subset first.

        Args:
            initial_set (list): The initial set to split.
            score_function (function): A function that computes the score of a subset.
            split_function (function): A function that splits a subset into two.
            max_iterations (int): Maximum number of iterations to explore subsets.

        Returns:
            list: The final list of explored subsets.
        """

        def manage_priority_queue(priority_queue, id, subset, score, n_thresholds, subprob, subset_sum, chosen_branching_vars):
            item = PriorityQueueItem(id, (score, id), subset, n_thresholds, subprob, subset_sum, chosen_branching_vars)
            heapq.heappush(priority_queue, item)
            return item

        def split_subset(subprob, subset, var, threshold):
            result = self.split_vars_by_threshold(subprob, subset, var, threshold, queue=True)
            return result["vars_below_threshold"], result["vars_above_threshold"]

        def compute_subset_score(subset, subprob, n_thresholds):
            """
            Computes the score of a fractional subset based on its size, value in the LP solution, and number of thresholds.
            Lower is better (priority queue)
            """
            n_machines = self.pricer.data["params"]["machines_per_group"][subprob]
            if n_thresholds == 0:
                n_thresholds = 0.5  # to avoid division by zero and favor surface level branching

            subset_sum = sum([entry[1] for entry in subset])
            subset_size = sum([entry[2] for entry in subset])  # including variable multiplicity
            return - subset_size * subset_sum * n_machines/ n_thresholds, subset_sum

        def is_integral(subset_sum):
            return self.model.isFeasIntegral(subset_sum)

        # Idea: Add variables with the same integer pattern, so that you guarantee that not finding a branching variable implies integral sum
        # get representative out of each integer pattern (maybe do this outside the function. Doing it here for now so I don't forget)
        # use the list that you already computed in the pricer
        
        # saving initial set because we might need it later for the repair step
        initial_set_copy = {}
        for subprob in range(self.pricer.n_subprobs):
            initial_set_copy[subprob] = copy(initial_set[subprob])

        compact_set = {}
        for subprob in range(self.pricer.n_subprobs):
            if self.pricer.data["params"]["machines_per_group"][subprob] <= 1: # skipping subproblems with only one machine
                continue
            
            compact_set[subprob] = []
            if self.pricer.data["params"]["model"] == 2: # no need to aggregate same integer patterns in ARMP
                for var in initial_set[subprob].values():
                    var_val = self.pricer.data["lpsol"][var.name]
                    compact_set[subprob].append([var, var_val, 1, [var]])
                del initial_set[subprob]
                continue

            while initial_set[subprob]:
                to_remove = []
                representative = list(initial_set[subprob]).pop()
                representative_var = initial_set[subprob][representative]
                cur_integer_pattern = str(sorted(list(self.pricer.data["integer_patterns"][representative].items())))
                current_sum = 0
                current_multiplicity = 0
                aggregated_vars = []
                for mvar_name in initial_set[subprob]:
                    mvar = initial_set[subprob][mvar_name]
                    if self.mvar_has_integer_pattern(mvar, cur_integer_pattern):
                        #if mvar_name in self.pricer.data["integer_encoding"][subprob][cur_integer_pattern]:
                        to_remove.append(mvar_name)
                        current_sum += self.pricer.data["lpsol"][mvar.name]
                        current_multiplicity += 1
                        aggregated_vars.append(mvar)

                # only keeping compact variables with fractional sum. # Todo: check if you can do this 
                #if not self.model.isFeasIntegral(current_sum):
                compact_set[subprob].append([representative_var, current_sum, current_multiplicity, aggregated_vars])

                for mvar_name in to_remove:
                    del initial_set[subprob][mvar_name]

        assert not any(initial_set.values()), "Some subproblems have non-represented variables left."

        # Priority queue (max-heap using negative scores)
        priority_queue = []
        id = 0
        for subprob in range(self.pricer.n_subprobs):
            if not compact_set[subprob]: # if no fractional master variables
                continue

            if self.pricer.data["params"]["machines_per_group"][subprob] <= 1: # skipping subproblems with only one machine
                continue

            # If all the aggregated variables in a subproblem are integral, we cannot branch on it
            if self.pricer.data["params"]["model"] == 0: # only relevant in ORMP
                if all([self.model.isFeasIntegral(entry[1]) for entry in compact_set[subprob]]):
                    self.integral[subprob] = True
                    self.integer_fractionalities[subprob] = [entry[3] for entry in compact_set[subprob]]
                    continue

            score, subset_sum = compute_subset_score(compact_set[subprob], subprob, 0)
            manage_priority_queue(priority_queue, id, compact_set[subprob], -score, 0, subprob, subset_sum, [])
            id += 1

        integral_subsets = []
        while priority_queue:
            # Get the most valuable subset
            item = heapq.heappop(priority_queue)

            # here you check if sum is integral
            if not is_integral(item.subset_sum):
                return item

            # try to find threshold
            var, threshold = self.pick_var_and_threshold(
                    subprob=item.subprob,
                    master_vars=item.subset,
                    patterns=patterns,
                    n_fractional_vars=len(item.subset),
                    all_chosen_branching_vars=item.thresholds
                    )

            if not var: # integral subset
                integral_subsets.append(item.subset)
                continue
            
            if self.pricer.data["params"]["debug_mode"]:
                assert var not in [i[0] for i in item.thresholds], "Branching variable was already chosen"

            # Split the subset into two
            subset1, subset2 = split_subset(item.subprob, item.subset, var, threshold)
            
            if self.pricer.data["params"]["debug_mode"]:
                assert len(item.subset) == len(subset1) + len(subset2), "Subset was not split correctly"

            # Compute scores for the new subsets
            assert subset1 and subset2, "Subset was not split"

            score1, subset_sum1 = compute_subset_score(subset1, item.subprob, item.n_thresholds+1)
            item1_thresholds = copy(item.thresholds)
            item1_thresholds.append([var, "<=", threshold])
            id += 1
            item1 = manage_priority_queue(priority_queue, id, subset1, score1, item.n_thresholds+1, item.subprob, subset_sum1, item1_thresholds)
            if self.pricer.data["params"]["debug_mode"]:
                assert self.model.isEQ(subset_sum1, sum([entry[1] for entry in subset1])), "Subset 1 sum does not match LP sum"
                for entry in subset1:
                    assert self.model.isEQ(entry[1], self.get_mvars_lp_sum(entry[-1])), "Subset 1 sum does not match LP sum"

            score2, subset_sum2 = compute_subset_score(subset2, item.subprob, item.n_thresholds+1)
            item2_thresholds = copy(item.thresholds)
            item2_thresholds.append([var, ">=", threshold])
            id += 1
            item2 = manage_priority_queue(priority_queue, id, subset2, score2, item.n_thresholds+1, item.subprob, subset_sum2, item2_thresholds)
            if self.pricer.data["params"]["debug_mode"]:
                assert self.model.isEQ(subset_sum2, sum([entry[1] for entry in subset2])), "Subset 2 sum does not match LP sum"
                for entry in subset2:
                    assert self.model.isEQ(entry[1], self.get_mvars_lp_sum(entry[-1])), "Subset 2 sum does not match LP sum"

        # no branching variable was found, so solution is integer feasible
        for subprob in range(self.pricer.n_subprobs):
            if self.pricer.data["params"]["debug_mode"]:
                for compact_var in compact_set[subprob]:
                    assert self.model.isFeasIntegral(compact_var[1])
                    assert self.model.isEQ(compact_var[1], sum([self.pricer.data["lpsol"][mvar.name] for mvar in compact_var[3]])), "Compact variable is not integral"

        return [(False, float("inf"))]
    
    def split_vars_by_threshold(self, subprob: int, master_vars: dict, branching_var: str, new_threshold: float, queue: bool = False) -> dict:
        """
        Given a list of master variables, a branching variable and a threshold, splits the master variables
        """
        vars_below_threshold = []
        vars_above_threshold = []
        master_vars_to_delete = []
        patterns = self.pricer.data[self.patterns][subprob]

        for master_var in master_vars:
            cur_pattern = patterns[master_var[0].name]
            branching_var_value = cur_pattern[branching_var]
            if self.model.isGT(branching_var_value, new_threshold):
                vars_above_threshold.append(master_var)
            else:
                vars_below_threshold.append(master_var)
        
        # in priority queue we don't want to delete variables
        if queue:
            return {
                "vars_below_threshold": vars_below_threshold,
                "vars_above_threshold": vars_above_threshold,
            }

        if len(vars_below_threshold) > len(vars_above_threshold):
            master_vars_to_delete = vars_above_threshold
            vars_satisfying_threshold = vars_below_threshold
            inequality = "<="
        elif len(vars_below_threshold) < len(vars_above_threshold):
            master_vars_to_delete = vars_below_threshold
            vars_satisfying_threshold = vars_above_threshold
            inequality = ">="
        else:
            # favoring side with more activity
            # todo: we're repeating this computation outside, but shouldn't be too bad
            sum_vars_below_threshold = sum([self.pricer.data["lpsol"][mvar.name] for mvar in vars_below_threshold])
            sum_vars_above_threshold = sum([self.pricer.data["lpsol"][mvar.name] for mvar in vars_above_threshold])
            if sum_vars_below_threshold >= sum_vars_above_threshold:
                master_vars_to_delete = vars_above_threshold
                vars_satisfying_threshold = vars_below_threshold
                inequality = "<="
            else:
                master_vars_to_delete = vars_below_threshold
                vars_satisfying_threshold = vars_above_threshold
                inequality = ">="

        result = {
            "master_vars_to_delete": master_vars_to_delete,
            "vars_satisfying_threshold": vars_satisfying_threshold,
            "inequality": inequality
        }

        return result

    def pick_var_and_threshold(self, subprob, master_vars, patterns, n_fractional_vars, all_chosen_branching_vars):
        # Finds a variable and a threshold that splits the fractional variables in roughly half

        # Tries to find integer variable that distinguishes two patterns
        if n_fractional_vars > 1:
            (var, threshold) = self.smart_var_and_threshold(subprob, master_vars, all_chosen_branching_vars, use_std_mad=False)

            if not var:
                (var, threshold) = self.force_var_and_threshold(master_vars, subprob)

            if var:
                if self.pricer.data["params"]["debug_mode"]:
                    assert all([var != entry[0] for entry in all_chosen_branching_vars]), "Branching variable was already chosen"
                return var, threshold

        # TODO: assert that when you get here, you're done, you don't need to come back (except for different subproblem ofc)

        # No integer variable found, so all patterns are the same. Check if their sum is fractional
        # If yes, just pick a variable from the pattern and a threshold that makes all variables stay in it
        # If not, then we must do the repair step
        integral_sum = self.vars_add_up_to_integer(master_vars)
        if integral_sum: # todo: we can probably assert this
            return (False, float("inf"))
        else:
            cur_pattern = patterns[next(iter(master_vars[0])).name]
            
            # Randomly pick a variable which wasn't yet picked
            available_vars = [v for v in cur_pattern.keys() if v != "total_cost" and v not in all_chosen_branching_vars]
            var = random.choice(available_vars) # todo: pick better
            
            threshold = 0.5
            return (var, threshold)

    def smart_var_and_threshold(self, subprob, master_vars, all_chosen_branching_vars, use_std_mad=False):
        """
        Picks a variable and a threshold that splits the fractional variables in roughly half
        """

        best_cv = 0
        branching_var = None
        most_even_var_n = 0

        if type(master_vars) is list:
            mvar_val     = {entry[0].name: entry[1] for entry in master_vars}
            multiplicity = {entry[0].name: entry[2] for entry in master_vars}
            master_vars  = [entry[0] for entry in master_vars]
            n_master_vars = sum(multiplicity.values())
        else:
            multiplicity = {mvar.name: 1 for mvar in master_vars}
            n_master_vars = len(master_vars)
            mvar_val = {}
            for mvar in master_vars:
                mvar_val[mvar.name] = self.pricer.data["lpsol"][mvar.name]

        cur_m_patterns = {}
        for mvar in master_vars:
            cur_m_patterns[mvar.name] = self.pricer.data[self.integer_patterns][mvar.name]

        for t in self.pricer.data["params"]["T"]:
            for k in self.pricer.data["params"][subprob].components.values():
                if k.artificial: # no branching on artificial variables
                    continue

                cur_x = "m[0,%s,%i]" % (k.name, t)
                already_picked = any([cur_x == entry[0] for entry in all_chosen_branching_vars])
                if use_std_mad and not already_picked:
                    a = False
                    assert a, "bug with cv. Why are multiplying by the LP solution? If all masters vars have the same value for a pricing var, the pricing var could still be chosen, because relevant_variables would be very distinct"
                    # for mvar in master_vars:
                    #     if cur_m_patterns[mvar.name][cur_x] != 0:
                    #         continue

                    # Value of original variable in pattern times value of master variable in LP solution
                    relevant_variables = [
                        cur_m_patterns[mvar.name][cur_x] for mvar in master_vars if not self.model.isZero(cur_m_patterns[mvar.name][cur_x])
                    ]
                    if not relevant_variables:
                        continue

                    cv = self.coefficient_of_variation(relevant_variables)
                    if cv > best_cv and (cur_x, 0.5) not in all_chosen_branching_vars:
                        best_cv = cv
                        branching_var = cur_x
                else:
                    cur_var_n = 0
                    for mvar in master_vars:
                        cur_val = cur_m_patterns[mvar.name][cur_x]
                        if self.model.isLE(cur_val, 0.5):
                            cur_var_n += multiplicity[mvar.name]
                
                    if abs(n_master_vars//2 - cur_var_n) < abs(n_master_vars//2 - most_even_var_n):
                        branching_var = cur_x
                        most_even_var_n = cur_var_n

        return branching_var, 0.5

    def force_var_and_threshold(self, master_vars, subprob):
        """
        Chooses two random columns, picks an original variable that is different, and sets the threshold to the average
        """

        master_vars = [mvar[0] for mvar in master_vars]
        for index1, mvar_1 in enumerate(master_vars):
            integer_pattern1 = self.pricer.data[self.integer_patterns][mvar_1.name]
            encoding_key1 = str(sorted(list(integer_pattern1.items())))

            for mvar_2 in master_vars[index1+1:]:

                if self.mvar_has_integer_pattern(mvar_2, encoding_key1):
                    continue

                integer_pattern2 = self.pricer.data[self.integer_patterns][mvar_2.name]
                for pricing_var in integer_pattern1:
                    val1 = integer_pattern1[pricing_var]
                    val2 = integer_pattern2[pricing_var] 
                    if not self.model.isEQ(val1, val2): # todo: possibly don't return here, but give a score instead
                        chosen_var = pricing_var
                        chosen_threshold = (val1 + val2)/2
                        return (chosen_var, chosen_threshold)

        # could not find an integer variable to branch on. need repair step.
        return (False, float("inf"))

    def perform_branching(self, result_dict):
        try:
            return self._perform_branching(result_dict)
        except Exception as e:
            log_error("aggregatevarbound_perform_branching", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}

    def _perform_branching(self, result) -> dict:

        if all(self.integral.values()):
            if self.pricer.data["params"]["verbose"] >= 2:
                print("Passed integrality check.")
            return self.repair_branching()

        if type(result) is PriorityQueueItem:
            all_chosen_thresholds = {}
            filtered_master_vars = {}
            sum_vars_satisfying_threshold = {}
            for subprob in range(self.pricer.data["params"]["n_groups"]):
                if subprob == result.subprob:
                    all_chosen_thresholds[subprob] = result.thresholds
                    filtered_master_vars[subprob] = result.subset
                    sum_vars_satisfying_threshold[subprob] = self.get_mvars_lp_sum(result.subset.values())
                else:
                    all_chosen_thresholds[subprob] = []
                    filtered_master_vars[subprob] = {}
                    sum_vars_satisfying_threshold[subprob] = 0
        else:
            filtered_master_vars = result["filtered_master_vars"]
            all_chosen_thresholds = result["all_chosen_thresholds"]
            sum_vars_satisfying_threshold = result["sum_vars_satisfying_threshold"]

        # down_frac = sum_vars_satisfying_threshold[subprob] - int(sum_vars_satisfying_threshold[subprob])
        # up_frac = int(sum_vars_satisfying_threshold[subprob]) + 1 - sum_vars_satisfying_threshold[subprob]
        # todo get something like the maintenance cost and multiply by the fractionality, so you have a proxy of the local estimate.

        # need to think what would be the priorities here, where would the dual and primal improve more
        # it probably depends on whether the treshold is big or small
        # also, bnp book mentions that the upbranch tends to provide more information - makes sense
        down = self.model.createChild(DOWN_PRIORITY, self.model.getLocalEstimate() )
        up   = self.model.createChild(UP_PRIORITY, self.model.getLocalEstimate())

        cur_node = self.model.getCurrentNode()
        cur_node, cur_node_number = get_parent_node_with_branching_decisions(self, cur_node)
        parent_branching_decisions = self.pricer.data["branching_decisions"][cur_node_number]

        cur_depth = self.pricer.data["node_depth"][cur_node_number]
        self.pricer.data["node_depth"][down.getNumber()] = cur_depth + 1
        self.pricer.data["node_depth"][up.getNumber()]   = cur_depth + 1
        del self.pricer.data["node_depth"][cur_node_number]

        max_depth = max(self.pricer.data["node_depth"].values())
        min_depth = min(self.pricer.data["node_depth"].values())

        # If big difference in subtree depth, do bfs for 10 nodes or depth is small again.
        # if cur_depth - min_depth >= 5 or self.pricer.data["bfs"] >= 10:
        #     self.pricer.data["bfs"] = -20
        #     self.model.setParam("nodeselection/bfs/stdpriority", 1073741822) # forcing bsf in this case
        # elif max_depth - min_depth <= 3 and self.pricer.data["bfs"] >= 0:
        #     self.model.setParam("nodeselection/bfs/stdpriority", 100000) # default value
        # self.pricer.data["bfs"] += 1

        # self.pricer.data["deactivate"][down.getNumber()] = False
        # self.pricer.data["deactivate"][up.getNumber()]   = False

        if self.pricer.data["params"]["debug_mode"]:
            # Checking if there is a loop
            for subprob in range(self.pricer.data["params"]["n_groups"]): # fix: I don't think that you can add thresholds per subproblem, becasue you'd need to create multiple children
                for branching_index in range(len(parent_branching_decisions[subprob])):
                    branching_decision = parent_branching_decisions[subprob][branching_index]
                    if branching_decision.branching_rule != "aggregatevarbounds":
                        continue

                    different_branching_decision = sorted(branching_decision.branching_thresholds) != sorted(all_chosen_thresholds[subprob])
                    
                    # This is not looping if the values are entirely different, or if the value is the same but the node position will be different
                    # Eg. If we previously branched on sum <= 8 and the current sum is 7.5, we'll create a node with a var_val == 8, but it will
                    # be an up node, thus the constraint is sum >= 8
                    different_var_val = \
                        branching_decision.node_position == "down" and self.model.isGT(branching_decision.var_val, sum_vars_satisfying_threshold[subprob]) \
                        or \
                        branching_decision.node_position == "up" and self.model.isLT(branching_decision.var_val, sum_vars_satisfying_threshold[subprob])

                    if not (different_branching_decision or different_var_val):
                        agg = branching_decision.aggregate_master_vars
                        agg_keys = [i for i in agg.keys()]
                        agg_vals = [i for i in agg.values()]
                        agg_sum = sum([self.pricer.data["lpsol"][v.name] for v in agg_vals])

                        filt = filtered_master_vars[0]
                        filt_keys = [i for i in filt.keys()]
                        filt_vals = [i for i in filt.values()]
                        filt_sum = sum([self.pricer.data["lpsol"][v.name] for v in filt_vals])
                        con_vars = self.model.getConsVars(self.pricer.data["branching_cons"][cur_node_number][0][0])
                        con_vars_name = [v.name for v in con_vars]
                        cons_vars_sum = sum([self.pricer.data["lpsol"][v.name] for v in con_vars])

                        nagg = len(agg)
                        nfilt = len(filt)
                        ncon_vars = self.model.getConsNVars(self.pricer.data["branching_cons"][cur_node_number][0][0])
                        z = [i for i in filt_keys if i not in agg_keys]
                        y = [i for i in agg_keys if i not in filt_keys]
                        p = [i for i in filt_keys if i not in con_vars_name]
                        
                    assert different_var_val or different_branching_decision, "Aggregate branching looping"

        self.pricer.data["branching_decisions"][down.getNumber()] = {}
        self.pricer.data["branching_decisions"][up.getNumber()]   = {}

        for subprob in sum_vars_satisfying_threshold: # possible that not all subprobs have been checked
            if -1 in sum_vars_satisfying_threshold:
                subprob = -1
            
            branched_in_subprob = len(all_chosen_thresholds[subprob]) > 0

            down_branching_decision = BranchingDecision(
                branching_rule="aggregatevarbounds",
                node_position="down",
                var_val=self.model.feasFloor(sum_vars_satisfying_threshold[subprob]),
                aggregate_master_vars=copy(filtered_master_vars[subprob]),
                naggregate_master_vars=len(filtered_master_vars[subprob]),
                branching_thresholds=all_chosen_thresholds[subprob],
                subprob=subprob,
                inequality="<=",
                )
            
            up_branching_decision = BranchingDecision(
                branching_rule="aggregatevarbounds",
                node_position="up",
                var_val=self.model.feasCeil(sum_vars_satisfying_threshold[subprob]),
                aggregate_master_vars=copy(filtered_master_vars[subprob]),
                naggregate_master_vars=len(filtered_master_vars[subprob]),
                branching_thresholds=all_chosen_thresholds[subprob],
                subprob=subprob,
                inequality="<=",
                )

            initialize_branching_decisions(
                pricer              = self.pricer,
                subprob             = subprob,
                parent_decisions    = parent_branching_decisions[subprob],
                downnr              = down.getNumber(),
                upnr                = up.getNumber(),
                down_branching      = down_branching_decision,
                up_branching        = up_branching_decision,
                branched_in_subprob = branched_in_subprob
            )

            if subprob == -1:
                break

        for subprob in sum_vars_satisfying_threshold:
            if -1 in sum_vars_satisfying_threshold:
                subprob = -1

            branched_in_subprob = len(all_chosen_thresholds[subprob]) > 0
            if not branched_in_subprob:
                continue

            print_branching_info(
                pricer=self.pricer,
                rule="aggregatevarbounds",
                subprob=subprob,
                all_chosen_thresholds=all_chosen_thresholds[subprob],
                sum_vars_satisfying_threshold=sum_vars_satisfying_threshold[subprob],
                last_subprob=(subprob==self.pricer.n_subprobs-1)
            )
        
            if subprob == -1: break

        return {'result': SCIP_RESULT.BRANCHED}
    
    # cuts off all nodes with a worse bound
    def handle_tree_following_repair_step(self, pricer):

        if self.model.isEQ(self.model.getDualbound(), pricer.best_sol["obj"]):
            pricer.data["optimal_sol_is_repaired"] = True
            for node_number, node in pricer.data["nodes"].items():
                if node.getType() == 4:
                    continue
                self.model.cutoffNode(node)

            return

        nodes_to_cut = []
        for node_number, node in pricer.data["nodes"].items():
            if self.model.isGE(node.getLowerbound(), pricer.best_sol["obj"]):
                self.model.cutoffNode(node)
                nodes_to_cut.append(node_number)

        for node_number in nodes_to_cut:
            pricer.data["closed_nodes"][node_number] = True
            del pricer.data["nodes"][node_number]

        return
    
    # constructs the repaired solution
    def construct_repaired_solution(self, pricer):
        if self.model.isLE(self.model.getLPObjVal(), pricer.primal_bound):
            pricer.primal_bound = self.model.getLPObjVal()
            pricer.best_sol = {}
            for subprob in range(pricer.n_subprobs):
                pricer.best_sol[subprob] = defaultdict(int)
                for mvar_name, mvar in pricer.data["var"][subprob].items():
                    pricer.best_sol[subprob][mvar_name] = self.pricer.data["lpsol"][mvar_name]

        pricer.best_sol["obj"] = pricer.primal_bound

    # stores the repaired solution in the pricer data structures
    def store_repaired_solution(self, pricer):
        cur_node_number = self.model.getCurrentNode().getNumber()

        for subprob in range(pricer.n_subprobs):

            pricer.found_negative_redcost = True
            for aggregated_var in pricer.data["implicit_integer_sol"][cur_node_number][subprob]:
                if len(aggregated_var) == 1:
                    continue

                mvar_val = {}
                for mvar in aggregated_var:
                    mvar_val[mvar.name] = pricer.data["implicit_integer_sol_vals"][cur_node_number][mvar.name]

                val_sum = sum(mvar_val.values())
                if self.model.isZero(val_sum): # can technically be an aggregate variable? maybe?
                    continue

                assert self.model.isFeasIntegral(val_sum), "If solution is integer, aggregated variable must be integer"

                self._create_and_add_repaired_columns(pricer, subprob, aggregated_var, val_sum, mvar_val)
        return

    # creates the column and adds it to the RMP
    def _create_and_add_repaired_columns(self, pricer, subprob, aggregated_var, val_sum, mvar_val):
        new_pattern = defaultdict(int)

        for mvar in aggregated_var:
            for v_name, v_val in pricer.data["patterns"][subprob][mvar.name].items():
                new_pattern[v_name] += (v_val*mvar_val[mvar.name])

        for v_name in new_pattern:
            new_pattern[v_name] /= val_sum # numerics

        new_pattern["maintenance_cost"] = new_pattern["total_cost"]

        result = {
            "objval": [-1],
            "vars": [new_pattern],
            "mu_patterns": [],
            "delta_patterns": [],
            "maintenance_cost": [int(new_pattern["maintenance_cost"])], # numerics
            "fixed_redcost_contribution": -1,
            "pricing_formulation": -1,
            "compact_run": False
        }
        pricer.add_column_to_RMP(result=result, subprob=subprob)
        return

    def repair_branching(self) -> dict:
        cur_node = self.model.getCurrentNode()
        cur_node, cur_node_number = get_parent_node_with_branching_decisions(self, cur_node)
            
        self.pricer.data["integrality_check"][cur_node_number] = True
        self.pricer.data["implicit_integer_sol"][cur_node_number] = {i: {} for i in range(self.pricer.n_subprobs)}
        # storing the solution that originated this implicit integer solution
        # (note that when solving the child, soplex can find a different solution, 
        #  so you cannot just use self.model.getSolVal(sol=None, expr=mvar))
        self.pricer.data["implicit_integer_sol_vals"][cur_node_number] = {}

        for subprob in range(self.pricer.n_subprobs):
            self.pricer.data["implicit_integer_sol"][cur_node_number][subprob] = self.integer_fractionalities[subprob]

            for aggregated_var in self.integer_fractionalities[subprob]:
                for mvar in aggregated_var:
                    mvar_val = self.pricer.data["lpsol"][mvar.name]
                    self.pricer.data["implicit_integer_sol_vals"][cur_node_number][mvar.name] = mvar_val

        for subprob in range(self.pricer.data["params"]["n_groups"]):
            print_branching_info(self.pricer, "repair_step", subprob=subprob, last_subprob=(subprob==self.pricer.n_subprobs-1), n_repaired_variables=len(self.integer_fractionalities[subprob]))

        self.model.cutoffNode(self.model.getCurrentNode()) # just ensuring that the current node is cut off

        if self.model.isLE(self.model.getLPObjVal(), self.pricer.primal_bound):
            self.construct_repaired_solution(self.pricer)
            # self.store_repaired_solution(self.pricer)
        self.handle_tree_following_repair_step(self.pricer)

        return {'result': SCIP_RESULT.CUTOFF}

    def mvars_have_same_integer_pattern(self, mvars):
        mvar = mvars[next(iter(mvars))]
        subprob = mvar.data["subprob"]
        string_integer_encoding = str(sorted(list(self.pricer.data[self.integer_patterns][mvar.name].items())))

        if any([i.name not in self.pricer.data[self.integer_encoding][subprob][string_integer_encoding] for i in mvars.values()]):
            return False
        else:
            return True

    def get_mvars_lp_sum(self, mvars):
        return sum([self.pricer.data["lpsol"][mvar.name] for mvar in mvars])

    def mvar_has_integer_pattern(self, mvar, integer_encoding):
        subprob = mvar.data["subprob"]
        return mvar.name in self.pricer.data[self.integer_encoding][subprob][integer_encoding]

    def vars_add_up_to_integer(self, master_vars):
        if type(master_vars) is list:
            return sum([entry[1] for entry in master_vars])
        return self.model.isFeasIntegral(sum([self.pricer.data["lpsol"][mvar.name] for mvar in master_vars]))

    def robust_std_mad(self, arr):
    # Helper function to get pricing variables with a big distribution over fractional columns
        return 1.4826 * median_abs_deviation(arr)

    def coefficient_of_variation(self, arr):
        # Helper function to get the coefficient of variation of a list of numbers
        arr = np.array(arr)
        mean = np.mean(arr)
        std = np.std(arr)
        len_factor = np.log(len(arr))
        if np.isclose(mean, 0):
            return 0
        return std * mean * len_factor

    def sort_master_vars_on_pricing_var(self, var_val):
    # Helper function to sort master variables by pricing variable value
        return var_val

    def branchexecps(self, allowaddcons=False):
        # for some reason, sometimes SCIP is not able to solve the LP during normal solve, but is able to solve it here
        return self.branchexeclp()   

    def fix_repaired_master_variables(self):
        for mvar, mvar_val_floor in self.variables_to_fix:
            self.model.addCons(mvar == mvar_val_floor, local=True, name = "branching_repair_step_%s_%s" % (mvar.name, mvar.data["subprob"]))

        return {'result': SCIP_RESULT.SUCCESS}

    def integrality_check(self):
        """
        Checks if the solution is integer with respect to the compact variables
        """
        return True

class PricingBranchingDisaggregate(Branchrule):
    """
    Performs branching on the fractional original variables. Can only be used in subproblems of size 1.
    """

    def __init__(self, model):
        self.model: Model
        self.pricer: Any
        self.var_names: str
        self.patterns: str
        self.integer_patterns: str
        self.integer_encoding: str
        branching_init(self, model)

    def branchexeclp(self, allowaddcons=False):
        try:
            start_branching_time = time.time()
            # Attribute master time slice prior to this branching callback
            last_end = self.pricer.data.get("last_callback_end", self.pricer.data.get("master_start_time", start_branching_time))
            self.pricer.data["master_time"] += max(0.0, start_branching_time - last_end)

            result = self._branchexeclp(allowaddcons)
            branching_end = time.time()
            self.pricer.data["end_branching_time"] = branching_end
            self.pricer.data["branching_time"] += (branching_end - start_branching_time)
            self.pricer.data["last_callback_end"] = branching_end
            return result
        except Exception as e:
            log_error("disaggregate_branchexec", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}
    
    def _branchexeclp(self, allowaddcons=False):
        if not self.pricer.data["lpsol"]:
            for subprob in range(self.pricer.data["params"]["n_groups"]):
                for mvar_name, mvar in self.pricer.data[self.var_names][subprob].items():
                    self.pricer.data["lpsol"][mvar_name] = self.model.getSolVal(sol=None, expr=mvar)

        self.pricer.data["disaggregate"]["n_calls"] += 1
        self.pricer.data["branching_start"] = time.time()
        self.filtered_master_vars = {}

        result_dict = {"found_var_to_branch_on": False}
        for subprob in range(self.pricer.data["params"]["n_groups"]):
            if self.pricer.data["params"]["machines_per_group"][subprob] == 1:
                result_dict = self.find_var_to_branch_on(subprob)
                if result_dict["found_var_to_branch_on"]:
                    break

        if result_dict["found_var_to_branch_on"]:
            self.pricer.data["lpsol"] = {} # freeing lpsol for next branching
            # todo: here we're just taking the first subproblem that has a fractional variable
            self.perform_branching(result_dict)
            self.pricer.data["disaggregate"]["n_successes"] += 1
            return {'result': SCIP_RESULT.BRANCHED}
        else:
            return {'result': SCIP_RESULT.DIDNOTFIND}

    def branchexecps(self, allowaddcons=False):
        try:
            return self._branchexecps(allowaddcons)
        except Exception as e:
            log_error("disaggregate_branchexecps", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}
        
    def _branchexecps(self, allowaddcons=False):
        if self.pricer.data["params"]["verbose"] >= 2:
            print("Trying to re-solve LP instead of using pseudo solution.")

        # for some reason, sometimes SCIP is not able to solve the LP during normal solve, but is able to solve it here
        self.model.writeProblem("problematic_lp.cip", trans=True, verbose=False)
        curlp = Model()
        curlp.readProblem("problematic_lp.cip")
        curlp.relax()
        curlp.hideOutput()
        curlp.optimize()
        if curlp.getNSols() > 0:
            self.pricer.data["lpsol"] = curlp.getVarDict()
            return self.branchexeclp()
        else:
            raise ValueError("You shouldn't be here. Loosen tolerances") # you can arrive here if LP can't be solved (e.g. for numerical reasons). 

    # Finds a fractional original variable to branch on
    def find_var_to_branch_on(self, subprob):
        try:
            return self._find_var_to_branch_on(subprob)
        except Exception as e:
            log_error("disaggregate_find_var", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e), "found_var_to_branch_on": False}
    
    def _find_var_to_branch_on(self, subprob):
        patterns = self.pricer.data[self.patterns]
        original_variable_sum = defaultdict()

        # iterating over discrete master variables
        for master_var in self.pricer.data[self.var_names][subprob].values():
            mvar_val = self.pricer.data["lpsol"][master_var.name]
            if self.model.isZero(mvar_val):
                continue

            for discrete_var in self.pricer.data[self.integer_patterns][master_var.name]:
                cur_val = patterns[subprob][master_var.name][discrete_var]
                if not self.model.isZero(cur_val):
                    try: # faster since only goes to except once
                        original_variable_sum[discrete_var] += mvar_val*cur_val
                    except KeyError:
                        original_variable_sum[discrete_var]  = mvar_val*cur_val

        result_dict = {}
        for discrete_var in original_variable_sum:
            if not self.model.isFeasIntegral(original_variable_sum[discrete_var]):
                result_dict[discrete_var] = original_variable_sum[discrete_var]

        if result_dict:
            result_dict["found_var_to_branch_on"] = True
            result_dict["var_to_branch_on"] = list(result_dict.keys())[0] # fix: choose the best guy
            result_dict["subprob"] = subprob
        else: # subproblem has size 1 but no fractional variables
            result_dict["found_var_to_branch_on"] = False

        return result_dict

    # Creates the nodes and the branching constraints
    def perform_branching(self, result_dict):
        try:
            return self._perform_branching(result_dict)
        except Exception as e:
            log_error("disaggregate_perform_branching", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}
    
    def _perform_branching(self, result_dict): 
        # need to think what would be the priorities here, where would the dual and primal improve more
        # it probably depends on whether the treshold is big or small
        # also, bnp book mentions that the upbranch tends to provide more information - makes sense
        down = self.model.createChild(DOWN_PRIORITY, self.model.getLocalEstimate()) 
        up   = self.model.createChild(UP_PRIORITY, self.model.getLocalEstimate())  

        var_to_branch_on      = result_dict["var_to_branch_on"]
        var_val               = result_dict[var_to_branch_on]
        branching_var_subprob = result_dict["subprob"]

        cur_node = self.model.getCurrentNode()
        cur_node, cur_node_number = get_parent_node_with_branching_decisions(self, cur_node)
        parent_branching_decisions = self.pricer.data["branching_decisions"][cur_node_number]

        self.pricer.data["branching_decisions"][down.getNumber()] = {}
        self.pricer.data["branching_decisions"][up.getNumber()]   = {}

        down_branching_decision = BranchingDecision(
            branching_rule="disaggregate",
            node_position="down",
            inequality="<=",
            var_val=self.model.feasFloor(var_val),
            branching_var_subprob=branching_var_subprob,
            disaggregate_branching_var=var_to_branch_on, 
            subprob=branching_var_subprob,
            )
        
        up_branching_decision = BranchingDecision(
            branching_rule="disaggregate",
            node_position="up",
            inequality=">=",
            var_val=self.model.feasCeil(var_val),
            branching_var_subprob=branching_var_subprob,
            disaggregate_branching_var=var_to_branch_on, 
            subprob=branching_var_subprob,
            )

        subprob = None
        for subprob in range(self.pricer.data["params"]["n_groups"]):

            initialize_branching_decisions(
                pricer           = self.pricer,
                subprob          = subprob,
                parent_decisions = parent_branching_decisions[subprob],
                downnr           = down.getNumber(),
                upnr             = up.getNumber(),
                down_branching   = down_branching_decision,
                up_branching     = up_branching_decision,
                branched_in_subprob = subprob == branching_var_subprob
            )

            if self.pricer.data["params"]["debug_mode"]:
                for branching_decision in parent_branching_decisions[subprob]:
                    if branching_decision.branching_rule == "disaggregate":
                        different_branching_decision = (var_to_branch_on != branching_decision.disaggregate_branching_var) \
                                                    or (branching_decision.branching_var_subprob != branching_var_subprob)

                        assert different_branching_decision, "Disaggregate branching looping"
        
        var_prefix = var_to_branch_on.split("[")[0]
        var_components = var_to_branch_on.split("[")[1].strip("]").split(",")
        modified_var_name = f"{var_prefix}[{branching_var_subprob},{','.join(var_components[1:])}]"
        var_to_branch_on = modified_var_name

        print_branching_info(
            pricer=self.pricer,
            rule="disaggregate",
            var_to_branch_on_name=var_to_branch_on,
            var_val = var_val,
            last_subprob=(subprob==self.pricer.n_subprobs-1)
        )
        print()

        return {'result': SCIP_RESULT.BRANCHED}

class PricingEventHdlr(Eventhdlr):
    """
    Enforces branching decisions in master variables.
    """

    def __init__(self, model):
        self.pricer: Any
        self.n_conss: int = 0
        self.var_names: str
        branching_init(self, model)

    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexec(self, event):
        try:
            branching_start = time.time() # getting branching start again here, because visiting nodes in different orders might screw things up
            # Attribute master time between last callback end and this event handler start
            last_end = self.pricer.data.get("last_callback_end", self.pricer.data.get("master_start_time", branching_start))
            self.pricer.data["master_time"] += max(0.0, branching_start - last_end)
            result = self._eventexec(event)
            self.pricer.data["end_branching_time"] = time.time()
            self.pricer.data["branching_time"] += (self.pricer.data["end_branching_time"] - branching_start)
            # Update unified callback anchor to close interval
            self.pricer.data["last_callback_end"] = self.pricer.data["end_branching_time"]
            return result

        except Exception as e:
            log_error("eventhdlr_exec", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}
    
    def _eventexec(self, event):
        self.pricer.data["single"]["n_calls"] += 1

        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()

        self.pricer.data["nodes"][cur_node_number] = cur_node

        # resetting dual-stabilization when focusing new node
        if self.pricer.data["params"]["dual_stabilization"]:
            self.pricer.stabilized_duals = []

        if cur_node_number == 1:
            self.pricer.data["nodes_visited"].append([None, 1])
            return
        
        parent_number = cur_node.getParent().getNumber()
        self.pricer.data["n_redcost_fixings"][cur_node_number] = self.pricer.data["n_redcost_fixings"][parent_number]
        self.pricer.data["redcost_fixed_vars"][cur_node_number] = copy(self.pricer.data["redcost_fixed_vars"][parent_number])

        # all the variables that were strongly fixed can now be normal fixed
        self.pricer.data["n_redcost_fixings"][cur_node_number] += self.pricer.data["n_strong_redcost_fixings"][parent_number]
        self.pricer.data["n_strong_redcost_fixings"][cur_node_number] = 0

        self.pricer.data["nodes_visited"].append([cur_node.getParent().getNumber(), cur_node_number])

        assert cur_node_number not in self.pricer.data["seen_nodes"], "You shouldn't be here"

        cur_branching_decisions = self.pricer.data["last_branching"][cur_node_number]
        branching_rule = cur_branching_decisions.branching_rule
        node_position  = cur_branching_decisions.node_position
        inequality     = cur_branching_decisions.inequality
        var_val        = cur_branching_decisions.var_val
        subprob        = cur_branching_decisions.subprob
        self.pricer.data["branching_cons"][cur_node_number] = {}

        # Handling disaggregate subproblem branching
        if branching_rule == "disaggregate":
            branching_var_subprob = cur_branching_decisions["branching_var_subprob"]
            disaggregate_branching_var = cur_branching_decisions["disaggregate_branching_var"]
        
            # locally removing the variables that violate the branching decision
            subprob = branching_var_subprob
            for mvar_name in self.pricer.data[self.var_names][subprob]:
                mvar = self.pricer.data[self.var_names][subprob][mvar_name]
                val_in_mvar = self.pricer.data[self.patterns][subprob][mvar_name][disaggregate_branching_var]
                if inequality == "<=":
                    if self.model.isGT(val_in_mvar, var_val):
                        self.model.chgVarUb(mvar, 0)
                elif inequality == ">=":
                    if self.model.isLT(val_in_mvar, var_val):
                        self.model.chgVarUb(mvar, 0)
                else:
                    raise ValueError("Something went wrong with the branching decision.")            
            
            self.pricer.data["seen_nodes"][cur_node_number] = 1
            self.pricer.data["disaggregate"]["time"] += (time.time() - self.pricer.data["branching_start"])

            # parents may have been generated by different branching rule
            parent_branching_cons = self.pricer.data["branching_cons"][parent_number]
            for subprob in range(self.pricer.n_subprobs):
                self.pricer.data["branching_cons"][cur_node_number][subprob] = deepcopy(parent_branching_cons[subprob])

            return {'result': SCIP_RESULT.SUCCESS}

        elif branching_rule == "aggregatevarbounds":
            aggregate_master_vars = cur_branching_decisions.aggregate_master_vars.values()
            branching_thresholds = cur_branching_decisions.branching_thresholds
            branching_thresholds = tuple(branching_thresholds)

            n_cons = self.model.getNConss(True)
            if node_position == "down":
                new_con = self.model.addCons(quicksum(aggregate_master_vars) <= var_val, local=True, modifiable=True, name="D_agg_branching_" + str(cur_node_number) + "_" + str(self.n_conss))
                if len(aggregate_master_vars) == 1: # because of duals in bound constraints
                    self.model.addConsCoeff(new_con, self.model.data["aux_var"], 1)

            elif node_position == "up":
                new_con = self.model.addCons(quicksum(aggregate_master_vars) >= var_val, local=True, modifiable=True, name="U_agg_branching_" + str(cur_node_number)+ "_" + str(self.n_conss))
                if len(aggregate_master_vars) == 1:
                    self.model.addConsCoeff(new_con, self.model.data["aux_var"], -1) # because of duals in bound constraints

            else:
                raise ValueError("Something went wrong with the branching decision.")

            self.n_conss += 1
            self.pricer.set_branching_cons(cur_node_number, subprob, new_con)
            cur_branching_decisions.branching_con = new_con

            parent_branching_cons = self.pricer.data["branching_cons"][parent_number]

            for i in range(self.pricer.n_subprobs):
                self.pricer.data["branching_cons"][cur_node_number][i] = copy(parent_branching_cons[i])
            
            t_new_con = self.model.getTransformedCons(new_con)
            self.pricer.set_branching_cons(cur_node_number, subprob, t_new_con)
            self.pricer.data["seen_nodes"][cur_node_number] = 1

            self.pricer.data["aggregatevarbound"]["time"] += (time.time() - self.pricer.data["branching_start"])
            return {'result': SCIP_RESULT.SUCCESS}

        elif branching_rule == "repair_step":
            self.pricer.data["repair_step"]["n_calls"] += 1
            self.pricer.data["repair_step"]["n_successes"] += 1
            return {'result': SCIP_RESULT.SUCCESS}

        else:
            raise ValueError("Branching decision not known.")
