from pyscipopt import Branchrule, SCIP_RESULT, Eventhdlr, SCIP_EVENTTYPE, quicksum
from collections import defaultdict
from copy import copy

class PricingBranching(Branchrule):
    # This branching rule indentifies variables in the pricing problem that are fractional in the RMP

    def __init__(self, model):
        self.model = model
        return
    
    def branchexeclp(self, allowaddcons=False):

        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()

        var_index_by_subprob = {}
        for subprob in range(self.model.data["pricer"].data["params"]["n_groups"]):
            var_index_by_subprob[subprob] = []
        
        for subprob in range(self.model.data["pricer"].data["params"]["n_groups"]):
            # getting fractional master variables
            for var in self.model.data["pricer"].data["var"][subprob].values(): 
                var_val = self.model.getVal(var) 

                if self.model.isGT(abs(var_val - int(var_val)), 0): # if fractional master vars
                    var_index_by_subprob[subprob].append((var.name,var_val))
        
        fractional_master_vars = False
        for subprob in range(self.model.data["pricer"].data["params"]["n_groups"]):
            if var_index_by_subprob[subprob]:
                fractional_master_vars = True
                break
        
        # If no fractional master vars then we can't branch
        assert fractional_master_vars, "Can't branch without fractional master vars."

        # Collecting branching candidates (fractional pricing vars)
        fractional_pricing_vars = {}
        for subprob in range(self.model.data["pricer"].data["params"]["n_groups"]):
            pricing_vars = defaultdict(int)
            for var_name, var_val in var_index_by_subprob[subprob]: # only looking at fractional master variables' patterns
                cur_sol = self.model.data["pricer"].data["patterns"][subprob][var_name]

                # checking maintenance variables only
                for v_ in cur_sol:
                    if v_[0:2] == "m[":
                      pricing_vars[(subprob,v_)] += var_val*cur_sol[v_]

            # collecting the fractional variables
            for subprob, var in pricing_vars:
                if not self.model.isEQ(pricing_vars[subprob,var] - int(pricing_vars[subprob,var]), 0) and not self.model.isEQ(pricing_vars[subprob,var] - int(pricing_vars[subprob,var]), 1):
                    fractional_pricing_vars[var] = [subprob, pricing_vars[subprob,var]]

        if not fractional_pricing_vars:
            # If you cannot find fractional pricing variables, it means that the sum of the corresponding patterns is integer feasible
            return {'result': SCIP_RESULT.DIDNOTFIND}
        
        # In case this node was created by another branching rule
        while cur_node_number not in self.model.data["pricer"].data["branching_decisions"]:
            cur_node = cur_node.getParent()
            cur_node_number = cur_node.getNumber()

        while fractional_pricing_vars:
            full_chosen_var = fractional_pricing_vars.popitem() 
            chosen_var = full_chosen_var[0]
            chosen_subprob = full_chosen_var[1][0]
            chosen_val = full_chosen_var[1][1]
            already_picked = False

        if already_picked:
            return {'result': SCIP_RESULT.DIDNOTFIND}
        
        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()

        while cur_node_number not in self.model.data["pricer"].data["branching_decisions"]:
            cur_node = cur_node.getParent()
            cur_node_number = cur_node.getNumber()

        parent_branching = self.model.data["pricer"].data["branching_decisions"][cur_node_number] 
        
        pricing_var_component_name = int(chosen_var.split(",")[0].split("[")[1])
        chosen_component = self.model.data["pricer"].data["params"][chosen_subprob].components[pricing_var_component_name]
        
        # the problem is usually with the incumbent
        down = self.model.createChild(1, self.model.getLocalEstimate())
        up = self.model.createChild(100, self.model.getLocalEstimate() + chosen_component.C)  

        assert chosen_var != None
        assert chosen_val != int(chosen_val), "variable is not fractional"

        self.model.data["pricer"].data["branching_decisions"][down.getNumber()] = parent_branching + [(chosen_subprob, chosen_var,"<=",int(chosen_val))]
        self.model.data["pricer"].data["branching_decisions"][up.getNumber()] = parent_branching + [(chosen_subprob, chosen_var,">=", int(chosen_val) + 1)]

        if self.model.data["pricer"].data["params"]["verbose"] >= 3:
            print("Branched on %s = %f" % (chosen_var, chosen_val))
        return {'result': SCIP_RESULT.BRANCHED}

    def branchexecps(self, allowaddcons=False):
        # pseudo-solution       
        
        cur_node_number = self.model.getCurrentNode().getNumber()
        for i in self.model.getPseudoBranchCands()[0]:
            # cur_node_number is already present if it was created by pseudo branching
            if cur_node_number == 1 or cur_node_number not in self.model.data["pricer"].data["pseudo_branching"] or i.name != self.model.data["pricer"].data["pseudo_branching"][cur_node_number][0].name: # need to compare names. doing x != y yields an error.

                down = self.model.createChild(1, self.model.getLocalEstimate())
                up   = self.model.createChild(100, self.model.getLocalEstimate() + i.getObj())  
                
                self.model.data["pricer"].data["pseudo_branching"][down.getNumber()] = (i, "0")
                self.model.data["pricer"].data["pseudo_branching"][up.getNumber()]   = (i, "1")

                return {'result': SCIP_RESULT.BRANCHED}
            
        raise ValueError("You shouldn't be here. Loosen tolerances") # you can arrive here if LP can't be solved (e.g. for numerical reasons). 
    

class PricingEventHdlr(Eventhdlr):
    """
    Enforces branching decisions in master variables.
    """

    def __init__(self, model):
        self.model = model

    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexec(self, event):
        cur_node = self.model.getCurrentNode()
        cur_node_number = cur_node.getNumber()

        if cur_node_number == 1 or cur_node_number in self.model.data["pricer"].data["seen_nodes"]:
            return 
        
        if cur_node_number not in self.model.data["pricer"].data["branching_decisions"]:
            if cur_node_number in self.model.data["pricer"].data["pseudo_branching"]:
                cur_branching = self.model.data["pricer"].data["pseudo_branching"][cur_node_number]

                if cur_branching[1] == "0":
                    # we need the duals of these columns. how should they factor in pricing? see good-to-know. 
                    # should the redcost not be 0, since we would just be adding the same column again?
                    self.model.addCons(cur_branching[0] <= 0)
                elif cur_branching[1] == "1":
                    self.model.addCons(cur_branching[0] >= 1)
                else:
                    raise ValueError
            return
        
        subprob, local_branch_var, inequality, var_val = self.model.data["pricer"].data["branching_decisions"][cur_node_number][-1]
        
        relevant_master_vars = []
        for master_var in self.model.getVars(transformed=True):
            if "lambda" not in master_var.name:
                continue
            
            # if different subprob
            if int(master_var.name.split(",")[0].split("[")[1]) != subprob:
                continue

            pattern_var = self.model.data["pricer"].data["patterns"][subprob][master_var.name][local_branch_var]
            if self.model.isGT(pattern_var,0): # == 1
                relevant_master_vars.append(master_var)

        if inequality == "<=":
            new_con = self.model.addCons(quicksum(relevant_master_vars) <= var_val, local=True)
        elif inequality == ">=":
            new_con = self.model.addCons(quicksum(relevant_master_vars) >= var_val, local=True)
        else:
            raise ValueError

        parent_branching_cons = self.model.data["pricer"].data["branching_cons"][cur_node.getParent().getNumber()]

        self.model.data["pricer"].data["branching_cons"][cur_node_number] = copy(parent_branching_cons)
        self.model.data["pricer"].data["branching_cons"][cur_node_number][local_branch_var] = new_con
        
        self.model.data["pricer"].data["seen_nodes"][cur_node_number] = 1