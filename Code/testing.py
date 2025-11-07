# Robust import: allow this module to be imported in environments without SCIP
try:
    import pyscipopt as scip
except Exception:
    # Minimal shim so that defining functions referencing scip APIs doesn't crash on import.
    import types, math as _math
    _EventType = types.SimpleNamespace(BESTSOLFOUND=1)
    _ParamEmph = types.SimpleNamespace(FEASIBILITY=0)
    class _Eventhdlr:
        pass
    scip = types.SimpleNamespace(
        exp=_math.exp,
        log=_math.log,
        Eventhdlr=_Eventhdlr,
        SCIP_EVENTTYPE=_EventType,
        SCIP_PARAMEMPHASIS=_ParamEmph,
    )

# Delaying heavy imports to runtime to avoid circular imports during tests
from parameters import Component, Machine, params
from typing import Any

try:
    from create_model import create_model
    import sequential_pricer
    import parallel_pricer
except Exception:
    # Allow importing specific utilities from this module in test context without full runtime deps
    create_model = None
    sequential_pricer = None
    parallel_pricer = None

# Maths and stats
import numpy as np
import math
import random
from time import time

# Instances
from importlib import import_module
import os

# Misc
import traceback # for debugging
import sys
from contextlib import redirect_stdout, redirect_stderr
import inspect # getting lambda functions
from types import SimpleNamespace # to create dummy classes for linter
import re
from collections import defaultdict
from datetime import datetime
import json # for keeping data

"""
Heuristic guide:

Each heuristic has associated to it a prime number. Change the heuristic parameter in the test function to
the minimum common multiple of the prime numbers associated to the heuristics that you want to use. 
Set the heuristic parameter to 1 if you want to use exact pricing.
"""

# Global parameters
MIN_DEMAND = 0.1
CHECK_CONVEXITY = True

# Feasibility checkers

def pricer_is_feasible(model, params):

    optimal_sol_is_repaired = not model.isInfinity(model.data["pricer"].best_sol["obj"]) and \
                            model.isLT(model.data["pricer"].best_sol["obj"], model.getPrimalbound())

    if optimal_sol_is_repaired and model.getNSols() == 0:
        if params["verbose"] >= 2:
            print("Instance is actually feasible, and we found the optimal solution: %i." % round(model.data["pricer"].best_sol["obj"]))

    if params["verbose"] >= 2:
        print()
        print("------------------------")
        print("| Checking feasibility |")
        print("------------------------")

    pricer = model.data["pricer"]

    if optimal_sol_is_repaired:
        integrality_check(model, pricer)
        if params["verbose"] >= 2:
            print("Integrality check passed.")
        if params["verbose"] >= 1:
            print("Optimal objective actually: %i." % round(pricer.best_sol["obj"]))

    if model.getNSols() > 0:
        best_sol = model.getBestSol()
    else:
        best_sol = None

    # Checking convexity and integrality constraints
    for subprob in range(len(params["machines_per_group"])):
        subproblem_varsum = 0
        for var in pricer.data["var"][subprob].values():
            if optimal_sol_is_repaired:
                var_val = model.data["pricer"].best_sol[subprob][var.name]
            else:
                var_val = model.getSolVal(sol=best_sol, expr=var)
                assert model.isFeasIntegral(var_val), "Integrality. %s: %.6f" % (var.name, var_val)
            subproblem_varsum += model.feasFloor(var_val) # numerics (each variable may have tiny fractionality, but they add up to big fractionality)

        assert model.isLE(subproblem_varsum, params["machines_per_group"][subprob]), "Convexity"

    if params["verbose"] >= 2:
        print("Convexity feasible.")

    # Checking demand constraints
    T_prime = params["T_prime"]
    sol_demand = len(T_prime)*[0]
    for subprob in range(len(params["machines_per_group"])):
        for cur_var in pricer.data["var"][subprob].values():
            if optimal_sol_is_repaired:
                for t in T_prime:
                    sol_demand[t-1] = params["demand"][t] # since repaired solution is lp-feasible, it satisfies the demand constraints directly
                break
            else:
                cur_var_val = model.getSolVal(sol=best_sol, expr=cur_var)

            if model.isGT(cur_var_val, 0):
                cur_pattern = pricer.data["patterns"][subprob][cur_var.name]
                for t in T_prime:
                    sol_demand[t-1] += cur_var_val*cur_pattern["y[0,%i]" % t]

    for t in T_prime:
        assert model.isGE(sol_demand[t-1], params["demand"][t]-0.000001), "Demand at %i. %.9f" % (t, sol_demand[t-1] - params["demand"][t])

    if params["verbose"] >= 2:
        print("Demand feasible.")
        if params["debug_mode"]: # only in debug mode because it takes a while
            print("Double-checking individual column feasibility.")

    # Also need to ensure each individual column is feasible, like in ARMP
    # I suppose it would be easier just to convert the solution back to the original space
    pi = {i:1 for i in params["T_prime"]} # for feasibility checking purposes
    counter = 1
    n_cols = model.getNVars(transformed=True)

    for subprob in range(len(params["machines_per_group"])):
        if not params["debug_mode"]:
            break

        for cur_var in pricer.data["var"][subprob].values():
            # (have epsilon-like infeasibilities)
            # check zero variables as well only in debug mode
            if not params["debug_mode"]:
                if optimal_sol_is_repaired:
                    if model.isZero(model.data["pricer"].best_sol[subprob][cur_var.name]):
                        continue
                else:
                    if model.getNSols() >= 0 and model.isZero(model.getVal(cur_var)):
                        continue

            cur_pattern = pricer.data["patterns"][subprob][cur_var.name]

            model.data["pricer"].check_column_feasibility(subprob=subprob, vars=cur_pattern)

            counter += 1
            if params["verbose"] >= 3:
                if counter % 20 == 0:
                    print("Checked %i/%i columns." % (counter, n_cols))
    
    if params["verbose"] >= 2:
        if n_cols%20 != 0 or params["verbose"] == 1:
            print("Checked %i/%i columns." % (counter, n_cols))
        print("Every column valid.\n")

    return True

def integrality_check(model, pricer):
    """ 
    From a fractional solution to the extended formulation, recover the underlying integer 
    original formulation solution.

    Given columns c1, .., cn, with the same integer variables, any convex combination of them
    remains feasible in the original problem space. Thus, if variables lambda_1, ..., lambda_n
    are fractional and their sum is not, then we can use the column
    sum_{i=1}^n lambda_i * c_i, eliminating the fractionalities.

    Post-CGS update: You actually don't need to get integer master variables, you only need to
    guarantee integrality in the compact space. So this repair step shouldn't be here, it should
    be at the end instead, to recover the solution in original variables.
    """
    
    for subprob in range(pricer.n_subprobs):
        new_pattern = {}
        new_mvar_val = 0
        for mvar_name, mvar_val in pricer.best_sol[subprob].items():
            if model.isZero(mvar_val) or model.isFeasIntegral(mvar_val):
                continue

            mvar_val_floor = model.feasFloor(mvar_val)
            mvar_fractionality = mvar_val - mvar_val_floor

            pattern = pricer.data["full_patterns"][subprob][mvar_name]
            
            # Adding the fractional part, unless it exceeds 1
            if model.isGT( new_mvar_val + mvar_fractionality, 1 ):
                remainder = new_mvar_val + mvar_fractionality - 1
                mvar_that_fits = mvar_fractionality - remainder
                new_mvar_val = 1
            else:
                remainder = 0
                new_mvar_val = new_mvar_val + mvar_fractionality
                mvar_that_fits = mvar_val - mvar_val_floor

            if model.isGT(mvar_that_fits, 0):
                for pricing_var in pattern:
                    try:
                        new_pattern[pricing_var] += pattern[pricing_var]*mvar_that_fits
                    except:
                        new_pattern[pricing_var]  = pattern[pricing_var]*mvar_that_fits

            assert model.isLE(new_mvar_val, 1)

            # If the columns add up to 1, then the new column cannot be increased any longer
            if model.isEQ(new_mvar_val, 1):
                result = {
                    "objval": [-10], # to guarantee addition
                    "fixed_redcost_contribution": 10,
                    "vars": [new_pattern],
                    "mu_patterns": [],
                    "delta_patterns": [],
                    "pricing_formulation": -1,
                    "maintenance_cost": [new_pattern["total_cost"]]
                }
                pricer.data["repaired_variables"][subprob].append({'result': result, 'subprob': subprob})

                # The remainder of the column that did not fit must be added
                new_mvar_val = remainder
                new_pattern = {}
                if model.isGT(new_mvar_val, 0):
                    for pricing_var in pricer.data["full_patterns"][subprob][mvar_name]:
                        new_pattern[pricing_var] = pattern[pricing_var]*new_mvar_val

        # We only got here because we couldn't find a fractionality, so what's left 
        # at the end must be zero
        assert model.isZero(new_mvar_val), "Integrality check failed."

def ARMP_is_feasible(model, params):
    pricer = model.data["pricer"]
    model.writeProblem(trans=True)

    if params["verbose"] >= 4:
        for i,j in model.getVarDict(True).items():
            if j > 0:
                print(i,j)

    # Checking convexity constraints
    for subprob in range(len(params["machines_per_group"])):
        subproblem_varsum = 0
        for delta in pricer.data["Delta"][subprob].values():
            subproblem_varsum += model.getVal(delta)
        # We must ensure every machine is working. Idle machines may still need repairs
        assert model.isLE(subproblem_varsum, params["machines_per_group"][subprob]), "Convexity"

    # Checking demand constraints
    T = params["T"]
    sol_demand = len(T)*[0]
    for subprob in range(len(params["machines_per_group"])):
        for cur_Delta in pricer.data["Mu"][subprob]:
            for mu in pricer.data["Mu"][subprob][cur_Delta].values():
                cur_mu_val = model.getVal(mu)
                if model.isGT(cur_mu_val, 0):
                    cur_pattern = pricer.data["Mu_patterns"][subprob][cur_Delta][mu.name]
                    for t in T:
                        sol_demand[t-1] += cur_mu_val*cur_pattern["y[0,%i]" % t]

    for t in T:
        assert model.isGE(sol_demand[t-1]-params["demand"][t], -0.00001), "Demand. %.9f" % (sol_demand[t-1] - params["demand"][t])

    if params["verbose"] >= 2:
        print("Convexity feasible.")
        print("Demand feasible.")
        print("Checking column compatibility.")

    assert ARMP_columns_are_compatible(model, params=params)

    return True

def ARMP_columns_are_compatible(model, params):
    if model.getNSols() > 0:
        # Checking compatibility constraints
        for subprob in range(len(params["machines_per_group"])):
            for cur_delta in model.data["pricer"].data["Delta"][subprob].values():
                if model.getVal(cur_delta) > 0:
                    pass#print(cur_delta.name, model.getVal(cur_delta))
                cur_mu_count = 0
                for cur_mu in model.data["pricer"].data["Mu"][subprob][cur_delta.name].values():
                    cur_mu_count += model.getVal(cur_mu)
                    if model.getVal(cur_mu) > 0:
                        pass#print(cur_mu.name, model.getVal(cur_mu))
                assert model.isLE(cur_mu_count, model.getVal(cur_delta))

    incompatible = 0
    total_cols = 0
    for subprob in range(len(params["machines_per_group"])):
        for cur_delta in model.data["pricer"].data["Delta"][subprob]:
            for cur_mu in model.data["pricer"].data["Mu"][subprob][cur_delta]:
                cur_mu_pattern    = model.data["pricer"].data["Mu_patterns"][subprob][cur_delta][cur_mu] 
                cur_delta_pattern = model.data["pricer"].data["Delta_patterns"][subprob][cur_delta]

                total_cols += 1
                if not model.data["pricer"].ARMP_is_compatible(cur_mu_pattern, cur_delta_pattern, subprob=subprob):
                    incompatible += 1
    
    if params["verbose"] >= 2:
        print("Used %i/%i incompatible columns" % (incompatible, total_cols))

    return True

def _compute_recipe_id(seed: float | int | None = None, extra: dict | None = None) -> str:
    """Compute a collision-resistant fingerprint for the instance-generation "recipe".

    The ID should change whenever any of the following change in a way that affects
    generated instances:
      - The logic of the generator helpers (get_component_degradation / get_production_limit)
      - Key generation parameters (e.g., time sets, groups, seeds)
      - Explicit overrides supplied by the caller via ``extra``

    Implementation details:
      - Hash a canonical JSON blob containing a filtered snapshot of ``params`` that controls
        instance generation (e.g., T, T_prime, machines_per_group, discrete_production,
        global_seed, model).
      - Include the function "fingerprints" of generator helpers using their bytecode,
        constants, names, and source where available. This reacts to code edits even if the
        textual source is formatted differently.
      - Include the optional ``seed`` and ``extra`` values.

    Returns a short hex digest suitable for directory names. Length increased to 16 to reduce
    accidental collisions across many runs.
    """
    import hashlib
    import inspect

    def _func_fingerprint(fn) -> str:
        try:
            co = getattr(fn, "__code__", None)
            parts: list[bytes | str] = []
            if co is not None:
                # co_code is bytes; co_consts may contain nested code objects and literals
                parts.append(co.co_code)
                # Convert potentially non-serializable tuples to strings deterministically
                parts.append(str(co.co_consts))
                parts.append(str(co.co_names))
                parts.append(str(co.co_varnames))
            # Defaults and kwdefaults affect behavior without changing source
            try:
                parts.append(str(getattr(fn, "__defaults__", None)))
                parts.append(str(getattr(fn, "__kwdefaults__", None)))
            except Exception:
                pass
            # Closure cell contents (constants captured from outer scope)
            try:
                clos = getattr(fn, "__closure__", None)
                if clos:
                    parts.append(str(tuple(getattr(c, "cell_contents", None) for c in clos)))
            except Exception:
                pass
            # Source as a fallback/context (robust to constants captured outside)
            try:
                parts.append(inspect.getsource(fn))
            except Exception:
                pass
            return hashlib.sha1("|".join([p if isinstance(p, str) else p.hex() for p in parts]).encode("utf-8")).hexdigest()
        except Exception:
            return ""

    def _filtered_params() -> dict:
        # Select only stable, JSON-serializable knobs that influence generation
        wanted_keys = [
            "global_seed", "T", "T_prime", "machines_per_group", "discrete_production",
            "model", "PT", "time_limit", "heuristic", "dual_stabilization"
        ]
        snap: dict[str, object] = {}
        try:
            if isinstance(params, dict):
                for k in wanted_keys:
                    if k in params:
                        snap[k] = params[k]
        except Exception:
            pass
        return snap

    # Build a canonical blob
    filt_params = _filtered_params()
    # Determine PT mode from filtered params (default False if missing)
    try:
        PT_flag = bool(filt_params.get("PT", False))
    except Exception:
        PT_flag = False

    # Fingerprint the appropriate generator helpers depending on PT mode
    if PT_flag:
        fn_map = {
            "get_pt_components_degradation": _func_fingerprint(get_pt_components_degradation),
            "PT_get_random_machine": _func_fingerprint(PT_get_random_machine),
        }
    else:
        fn_map = {
            "get_component_degradation": _func_fingerprint(get_component_degradation),
            "get_production_limit": _func_fingerprint(get_production_limit),
        }

    blob = {
        "seed": seed,
        "params": filt_params,
        "extra": extra or {},
        "PT": PT_flag,
        "functions": fn_map,
    }

    try:
        payload = json.dumps(blob, sort_keys=True, separators=(",", ":"), default=str)
    except Exception:
        # Extremely defensive: fall back to str()
        payload = str(blob)

    # Use a strong hash; truncate to 16 characters to keep paths short while reducing clashes
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return digest[:16]

def retrieve_stored_optimal_sols(results_file: str | None = None, recipe: str | None = None):
    """
    Loads past best solutions for consistency checks and warm-starts.

    Args:
        results_file: Path to the CSV-like storage file.
    recipe: Optional recipe id; if None, uses current recipe id.

    Returns:
        is_infeasible (dict[str,bool])
        is_optimal   (dict[str,bool])
        best_primals (dict[str,float|None])
        best_duals   (dict[str,float|None])
    """
    import csv
    if recipe is None:
        # No seed context here; callers can pass one if needed
        recipe = _compute_recipe_id()

    # Default: one file per recipe under Results/recipes/<recipe>/optimal_results.txt
    if results_file is None:
        results_file = os.path.join("./Results", "recipes", recipe, "optimal_results.txt")

    best_duals: dict[str, float | None] = {}
    best_primals: dict[str, float | None] = {}
    is_infeasible: dict[str, bool] = {}
    is_optimal: dict[str, bool] = {}

    if not os.path.exists(results_file):
        return is_infeasible, is_optimal, best_primals, best_duals

    with open(results_file, "r", newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            instance = (row.get("instance") or "").strip()
            if not instance:
                continue
            infeas = str(row.get("is_infeasible", "")).strip().lower() == "yes"
            primal_s = (row.get("primal", "") or "").strip()
            dual_s = (row.get("dual", "") or "").strip()
            def _parse_num(s: str) -> float | None:
                s = s.strip()
                if s == "":
                    return None
                if s.lower() == "inf":
                    return float('inf')
                if s.lower() == "-inf":
                    return float('-inf')
                if s.lower() == "nan":
                    return float('nan')
                try:
                    return float(s)
                except Exception:
                    return None
            primal = _parse_num(primal_s)
            dual = _parse_num(dual_s)

            is_infeasible[instance] = infeas
            is_optimal[instance] = (primal is not None and dual is not None and abs(primal - dual) < 1e-9)
            best_primals[instance] = primal
            best_duals[instance] = dual

    return is_infeasible, is_optimal, best_primals, best_duals

def update_optimal_results(filename: str,
                            objval: dict[str, float] | float | None,
                            dual: dict[str, float] | float | None,
                            is_infeasible: bool,
                            results_file: str | None = None,
                            recipe: str | None = None,
                            error: Any | None = None):
    """Update or insert the best-known results for an instance.

    - Minimization objective: lower primal is better, higher dual is better.
    - Distinguishes instances by (instance, recipe) to avoid mixing across generator changes.
    - Backward-compatible with legacy files that don't have a recipe column.
    """
    import csv
    if recipe is None:
        recipe = _compute_recipe_id()

    # Default file per recipe
    if results_file is None:
        results_file = os.path.join("./Results", "recipes", recipe, "optimal_results.txt")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    # Resolve scalar vs mapping inputs
    if isinstance(objval, dict):
        pobj = objval.get(filename)
    else:
        pobj = objval
    if isinstance(dual, dict):
        dval = dual.get(filename)
    else:
        dval = dual

    # recipe resolved above

    # If infeasibility not proven and bounds are missing, use ±infinity conventions
    if not is_infeasible:
        if pobj is None:
            pobj = float('inf')
        if dval is None:
            dval = float('-inf')

    # Load existing rows (if file exists)
    rows: list[dict] = []
    fieldnames = ["instance", "is_infeasible", "primal", "dual", "error"]
    if os.path.exists(results_file):
        with open(results_file, "r", newline="") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            existing_fields = reader.fieldnames or []
            # Normalize to expected fieldnames
            for row in reader:
                r = {
                    "instance": (row.get("instance") or "").strip(),
                    "is_infeasible": (row.get("is_infeasible") or "").strip(),
                    "primal": (row.get("primal") or "").strip(),
                    "dual": (row.get("dual") or "").strip(),
                    "error": (row.get("error") or "").strip(),
                }
                rows.append(r)

    # Find match by instance+recipe
    def parse_float(s: str) -> float | None:
        try:
            return float(s)
        except Exception:
            return None

    found_idx = None
    for i, r in enumerate(rows):
        if r["instance"] == filename:
            found_idx = i
            break

    def fmt_num(x: float | None) -> str:
        if x is None:
            return ""
        import math as _m
        if isinstance(x, float) and (_m.isinf(x) or _m.isnan(x)):
            # Represent inf/-inf/NaN as plain strings
            if _m.isnan(x):
                return "nan"
            return "inf" if x > 0 else "-inf"
        # Prefer integer formatting when close
        if abs(x - round(x)) < 1e-9:
            return f"{int(round(x))}"
        return f"{x:.6f}"

    if found_idx is None:
        # Insert new row
        new_row = {
            "instance": filename,
            "is_infeasible": "Yes" if is_infeasible else "No",
            "primal": fmt_num(pobj),
            "dual": fmt_num(dval),
            "error": "Yes" if error else "OK",
        }
        rows.append(new_row)
    else:
        # Update existing row if improved
        r = rows[found_idx]
        if is_infeasible:
            r["is_infeasible"] = "Yes"
            r["primal"] = ""
            r["dual"] = ""
            if error:
                r["error"] = error.strip()
        else:
            r["is_infeasible"] = "No"
            old_p = parse_float(r.get("primal", ""))
            old_d = parse_float(r.get("dual", ""))
            # Update primal if better (lower)
            if pobj is not None and (old_p is None or pobj < old_p - 1e-9):
                r["primal"] = fmt_num(pobj)
            # Update dual if better (higher)
            if dval is not None and (old_d is None or dval > old_d + 1e-9):
                r["dual"] = fmt_num(dval)
            if error:
                if error == True:
                    r["error"] = "Yes"
                else:
                    r["error"] = error.strip()

    # Write back
    with open(results_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

def save_best_solution_file(model, filename: str, results_file: str | None = None, recipe: str | None = None, method_tag: str | None = None, keep_all: bool = True, optimal_sol_is_repaired: bool | None = None) -> str | None:
    """Persist solutions for a run in a method-specific folder next to the per-recipe results.

    Storage layout (per recipe):
      - Base directory: Results/recipes/<recipe>/
      - Solutions per method: Results/recipes/<recipe>/solutions/<method>/
        - Stable best-known files for this instance (if available):
            <instance>.sol   (preferred, via model.writeBestSol if SCIP has solutions)
            <instance>.json  (fallback compact JSON of nonzero vars if writeBestSol missing)
            <instance>.repaired.json (only when optimal_sol_is_repaired is True)
        - Run-specific snapshots (always when a solution exists):
            runs/<instance>__<method>__YYYYmmdd-HHMMSS.{sol|json|repaired.json}

    Behavior:
      - If SCIP has visible solutions (model.getNSols() > 0):
          * Try to write <instance>.sol. If not possible, write JSON fallback with nonzero vars.
      - If no SCIP-visible solution: try saving a repaired solution from pricer.best_sol.
          * When optimal_sol_is_repaired is True, write stable <instance>.repaired.json plus a run copy.
          * Otherwise, write only the run-specific repaired copy (for traceability).
    saved_path: str | None = None

    Returns the path to a stable file written for this instance (if any); otherwise None.
    """
    if recipe is None:
        recipe = _compute_recipe_id()
    base_dir = os.path.dirname(results_file) if results_file else os.path.join("./Results", "recipes", recipe)
    # Place solutions under a method-specific subfolder to avoid overlap between Compact and DW
    method_sub = (method_tag or "method").replace("/", "_").replace(" ", "_")
    sol_dir = os.path.join(base_dir, "solutions", method_sub)

    saved_path: str | None = None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Prefer native SCIP .sol output if available
    try:
        nsols = model.getNSols() if hasattr(model, "getNSols") else 0
    except Exception:
        nsols = 0
    if nsols and nsols > 0:
        wrote_sol = False
        if hasattr(model, "writeBestSol"):
            # Stable path (may overwrite): latest best for this instance
            out_path = os.path.join(sol_dir, f"{filename}.sol")
            try:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                model.writeBestSol(out_path)
                saved_path = out_path
                wrote_sol = True
            except Exception:
                wrote_sol = False
            # Optional run-specific copy to avoid overwrites when .sol is available
            if keep_all and wrote_sol:
                runs_dir = os.path.join(sol_dir, "runs")
                os.makedirs(runs_dir, exist_ok=True)
                tag = method_tag or "method"
                run_path = os.path.join(runs_dir, f"{filename}__{tag}__{ts}.sol")
                try:
                    model.writeBestSol(run_path)
                except Exception:
                    pass
        # Fallback: create a compact JSON of variable values (non-zeros) if .sol not written
        if not wrote_sol:
            try:
                best = model.getBestSol()
                vals = {}
                try:
                    for v in model.getVars():
                        try:
                            val = model.getSolVal(best, v)
                            # store only significant values
                            if isinstance(val, (int, float)) and abs(val) > 1e-12:
                                vals[v.name] = float(val)
                        except Exception:
                            continue
                except Exception:
                    vals = {}

                meta = {"filename": filename}
                try:
                    meta["objective"] = str(float(model.getSolObjVal(best)))
                except Exception:
                    pass
                out_path = os.path.join(sol_dir, f"{filename}.json")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w") as fp:
                    json.dump({"meta": meta, "vars": vals}, fp)
                saved_path = out_path
                if keep_all:
                    runs_dir = os.path.join(sol_dir, "runs")
                    os.makedirs(runs_dir, exist_ok=True)
                    tag = method_tag or "method"
                    run_path = os.path.join(runs_dir, f"{filename}__{tag}__{ts}.json")
                    try:
                        with open(run_path, "w") as fp:
                            json.dump({"meta": meta, "vars": vals}, fp)
                    except Exception:
                        pass
            except Exception:
                pass

    # No SCIP-visible solution: try to persist repaired solution from the pricer
    try:
        pricer = model.data.get("pricer") if hasattr(model, "data") else None
    except Exception:
        pricer = None
    if pricer is not None:
        try:
            bsol = getattr(pricer, "best_sol", None)
            # best_sol is expected to be a dict with key "obj" and subproblem maps
            if isinstance(bsol, dict) and "obj" in bsol and bsol["obj"] is not None:
                # Skip if objective is infinite-like placeholder
                try:
                    import math as _m
                    if isinstance(bsol["obj"], (int, float)) and _m.isinf(float(bsol["obj"])):
                        return saved_path
                except Exception:
                    pass
                # Build a compact representation
                bobj = bsol.get("obj")
                meta = {"filename": filename, "kind": "repaired", "objective": str(float(bobj)) if isinstance(bobj, (int, float)) else str(bobj)}
                # subproblem -> {var_name: value}
                assign = {}
                for k, v in bsol.items():
                    if k == "obj":
                        continue
                    if isinstance(v, dict):
                        # Filter zeros for compactness
                        nz = {name: float(val) for name, val in v.items() if isinstance(val, (int, float)) and abs(val) > 1e-12}
                        if nz:
                            assign[str(k)] = nz

                # If flagged optimal, write a stable file and a run copy; otherwise write only a run copy
                if optimal_sol_is_repaired is True:
                    out_path = os.path.join(sol_dir, f"{filename}.repaired.json")
                    try:
                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                        with open(out_path, "w") as fp:
                            json.dump({"meta": meta, "master_vars": assign}, fp)
                        if saved_path is None:
                            saved_path = out_path
                    except Exception:
                        pass
                # Always write a run-specific copy so we capture the method's found solution in this run
                if keep_all:
                    runs_dir = os.path.join(sol_dir, "runs")
                    os.makedirs(runs_dir, exist_ok=True)
                    tag = method_tag or "method"
                    run_path = os.path.join(runs_dir, f"{filename}__{tag}__{ts}.repaired.json")
                    try:
                        with open(run_path, "w") as fp:
                            json.dump({"meta": meta, "master_vars": assign}, fp)
                    except Exception:
                        pass
        except Exception:
            pass

    return saved_path

def save_infeasible_solution_debug(model, filename: str, results_file: str | None = None, recipe: str | None = None, method_tag: str | None = None, is_repaired: bool | None = None, tol: float = 1e-12) -> str | None:
    """When feasibility checks fail, dump non-zero vars and their patterns for inspection.

    Layout: Results/recipes/<recipe>/invalid_solutions/<method>/runs/<instance>__<method>__<ts>.json

    Captures:
      - meta: filename, method, repaired flag, objective (if available)
      - vars: {var_name: value} for significant non-zeros
      - patterns: {var_name: pattern_dict}
    """
    if recipe is None:
        recipe = _compute_recipe_id()
    base_dir = os.path.dirname(results_file) if results_file else os.path.join("./Results", "recipes", recipe)
    method_sub = (method_tag or "method").replace("/", "_").replace(" ", "_")
    out_dir = os.path.join(base_dir, "invalid_solutions", method_sub, "runs")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, f"{filename}__{method_sub}__{ts}.json")

    # Try to detect repaired status if not provided
    if is_repaired is None:
        try:
            bsol = model.data.get("pricer").best_sol  # type: ignore[attr-defined]
            if isinstance(bsol, dict) and "obj" in bsol:
                is_repaired = not model.isInfinity(bsol["obj"]) and model.isLT(bsol["obj"], model.getPrimalbound())
        except Exception:
            is_repaired = False

    pricer = None
    try:
        pricer = model.data.get("pricer")  # type: ignore[attr-defined]
    except Exception:
        pricer = None

    collected_vars: dict[str, float] = {}
    collected_patterns: dict[str, dict] = {}
    objective: str | None = None

    if is_repaired and pricer is not None and isinstance(getattr(pricer, "best_sol", None), dict):
        bsol = pricer.best_sol
        # Objective
        try:
            objective = str(bsol.get("obj"))
        except Exception:
            objective = None
        # Values per subproblem
        full_patterns = getattr(pricer, "data", {}).get("full_patterns")
        patterns = getattr(pricer, "data", {}).get("patterns")
        for subkey, vard in bsol.items():
            if subkey == "obj" or not isinstance(vard, dict):
                continue
            for vname, vval in vard.items():
                if isinstance(vval, (int, float)) and abs(float(vval)) > tol:
                    collected_vars[vname] = float(vval)
                    pat = None
                    try:
                        if isinstance(full_patterns, dict) and subkey in full_patterns and vname in full_patterns[subkey]:
                            pat = full_patterns[subkey][vname]
                        elif isinstance(patterns, dict) and subkey in patterns and vname in patterns[subkey]:
                            pat = patterns[subkey][vname]
                    except Exception:
                        pat = None
                    if isinstance(pat, dict):
                        collected_patterns[vname] = pat
    else:
        # Use SCIP-visible best solution
        try:
            best = model.getBestSol()
        except Exception:
            best = None
        if best is not None:
            try:
                objective = str(float(model.getSolObjVal(best)))
            except Exception:
                objective = None
        # Iterate master vars tracked by pricer
        if pricer is not None and best is not None:
            varmap = getattr(pricer, "data", {}).get("var")
            full_patterns = getattr(pricer, "data", {}).get("full_patterns")
            patterns = getattr(pricer, "data", {}).get("patterns")
            if isinstance(varmap, dict):
                for subprob, d in varmap.items():
                    if not isinstance(d, dict):
                        continue
                    for var in d.values():
                        try:
                            vname = var.name
                        except Exception:
                            vname = str(var)
                        try:
                            val = model.getSolVal(best, var)
                        except Exception:
                            continue
                        if isinstance(val, (int, float)) and abs(float(val)) > tol:
                            collected_vars[vname] = float(val)
                            pat = None
                            try:
                                if isinstance(full_patterns, dict) and subprob in full_patterns and vname in full_patterns[subprob]:
                                    pat = full_patterns[subprob][vname]
                                elif isinstance(patterns, dict) and subprob in patterns and vname in patterns[subprob]:
                                    pat = patterns[subprob][vname]
                            except Exception:
                                pat = None
                            if isinstance(pat, dict):
                                collected_patterns[vname] = pat

    payload = {
        "meta": {
            "filename": filename,
            "method": method_sub,
            "repaired": bool(is_repaired),
            "objective": objective,
        },
        "vars": collected_vars,
        "patterns": collected_patterns,
    }
    try:
        with open(out_path, "w") as fp:
            json.dump(payload, fp)
        return out_path
    except Exception:
        return None

def retrieve_dw_timings(data_dir="Results/DW/Data", time_limit=300):
    """
    Reads all data files in Results/DW/Data, extracts timing info from the second dictionary,
    classifies the instance using its .stats file (feasible vs infeasible),
    and prints timing shares separately for each class.

    Only considers instances classified as easy / medium / hard by group_instances_by_difficulty.
    """
    import re
    import os

    timing_keys = ["master_time", "python_time", "heuristic_time", "branching_time",
                   "exact_pricing_time", "integer_rmp_time"]
    timings = []

    # Build full instance list (same as elsewhere) ---------------------------------
    all_instances = []
    for complexity in ["low","high"]:
        for n_years in [10,20]:
            for machines_per_group in ["20","10_10"]:
                prefix = f"{complexity}_{n_years}x{machines_per_group}x"
                for i in range(50):
                    all_instances.append(prefix + str(i))

    # Classify (we keep infeasible instances so they can still be tagged feasible/infeasible later)
    instances_by_difficulty, _ = group_instances_by_difficulty(
        models_to_use=["DW", "Compact"],
        all_instances=all_instances,
        time_limit=time_limit,
        skip_infeasible_instances=False
    )

    # Only keep easy / medium / hard
    allowed_instances = set(instances_by_difficulty["easy"] +
                            instances_by_difficulty["medium"] +
                            instances_by_difficulty["hard"])

    # Derive stats dir
    dw_root = os.path.dirname(data_dir.rstrip("/"))
    stats_dir = os.path.join(dw_root, "Statistics")

    groups = {
        "feasible": {k: 0.0 for k in timing_keys},
        "infeasible": {k: 0.0 for k in timing_keys},
    }
    group_counts = {"feasible": 0, "infeasible": 0}

    for fname in os.listdir(data_dir):
        if not fname.endswith(".txt"):
            continue

        base = fname[:-len("_data.txt")] if fname.endswith("_data.txt") else os.path.splitext(fname)[0]

        # Skip instances not in requested difficulty tiers
        if base not in allowed_instances:
            continue

        path = os.path.join(data_dir, fname)
        stats_path = os.path.join(stats_dir, base + ".stats")

        # Classify feasible vs infeasible using stats
        try:
            if not os.path.isfile(stats_path):
                continue
            result = scip.readStatistics(stats_path)
            group = "infeasible" if getattr(result, "status", "") == "infeasible" else "feasible"
        except Exception:
            continue

        try:
            with open(path, "r") as f:
                content = f.read()

            parts = content.split("\n\n\n")
            if len(parts) < 2:
                continue
            second_dict_content = parts[1]

            timing_entry = {"file": fname, "instance": base, "group": group}
            for key in timing_keys:
                # matches: 'key': 0.123 or 'key': '0.123'
                pattern = fr"'{key}':\s*'?(-?\d+(?:\.\d*)?)'?"
                m = re.search(pattern, second_dict_content)
                if m:
                    val = float(m.group(1))
                    timing_entry[key] = val
                    groups[group][key] += val
                else:
                    timing_entry[key] = None

            timings.append(timing_entry)
            group_counts[group] += 1
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    def print_group_shares(title, totals):
        total_time = sum(totals[k] for k in timing_keys)
        print(title)
        if total_time <= 0:
            print("  No timing data.")
            return
        for k in timing_keys:
            pct = 100 * totals[k] / total_time if total_time else 0
            label = k.replace("_", " ").title()
            print(f"  {label:<17} {pct:6.2f}%")

    print(f"Counts considered (easy/medium/hard only) -> feasible: {group_counts['feasible']}, infeasible: {group_counts['infeasible']}")
    print_group_shares("Feasible instances - component time share:", groups["feasible"])
    print_group_shares("Infeasible instances - component time share:", groups["infeasible"])

    return timings

# Error logging
def log_error(method_name, error, filename, stop_at_error=True):
    """
    Log errors from pricer callbacks to a file and signal instance termination.
    
    Args:
        method_name (str): Name of the method where the error occurred.
        error (Exception): The exception object.
        filename (str): Name of the file to log the error.
        stop_at_error (bool): If True, raise an error
        
    Returns:
        bool: Always returns False to indicate an error occurred.
    """

    with open("Errors/%s.log" % filename, "a") as error_file:
        # todo instance name
        error_file.write(f"Error in {method_name}:\n")
        error_file.write(f"{type(error).__name__}: {str(error)}\n")
        error_file.write(traceback.format_exc())
        error_file.write("\n" + "-"*80 + "\n")

    if stop_at_error:
        print("Error in %s: %s" % (method_name, str(error)))
        print(traceback.format_exc())
        print("\n" + "-"*80 + "\n")
        raise error

    return False

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
    #random.seed(new_params["global_seed"])

    demand = {}
    if peak_demand:
        # to simulate peaks and valleys of demand. starting out with just one each
        high_demand = [i for i in range(len(T_prime)//2)]
        low_demand  = [i for i in range(len(T_prime)//2, len(T_prime)+1)]
        for t in high_demand:
            demand[t] = float(f"{round(max(random.random(),0.1)*n_machines*1.3, 3)}")
        for t in low_demand:
            demand[t] = float(f"{round(max(random.random(),0.1)*n_machines/4, 3)}")
    else:
        for t in T_prime:
            # demand[t] = max(MIN_DEMAND, round(random.randint(n_machines//3, n_machines//2)) )
            demand[t] = float(f"{max(MIN_DEMAND, round(random.uniform(n_machines/2, n_machines/1.5), 2))}")

    new_params["demand"] = demand

    return new_params

def get_random_machine(complexity="low", force_linear=False, seed = 1000000000000066600000000000001, params=params):
    """
    Randomizes every parameter for a group of machines. Needs a seed for randomness
    """

    random.seed(seed)
    if "PT" not in params:
        params["PT"] = False

    if params["PT"]: # specialized method
        return PT_get_random_machine(params=params, seed=seed)

    if complexity == "low":
        n_components = random.randint(1,3)
    elif complexity == "high":
        n_components = random.randint(3,7)
    else:
        n_components = 0

    cur_components = {}
    #cur_params = {}
    production_granularity = len(params["T_prime"])/len(params["T"])
    degradation_lb = 0.9**(1/production_granularity) # ~90% after 1 "year", ~80% after 2

    # todo: probably want to have complex and simple components too.
    # Component creation
    machine_Q = float("inf")
    for cur_component in range(n_components):
        # I'm truncating the random parameters so that the problem can work with the provided tolerances
        # not using params["decimal_places"] to make debugging easier
        component_name         = str(cur_component) 
        Rmax                   = random.randint(20, 100)*production_granularity
        C                      = random.randint(2, 20)
        Q                      = float("{:.2f}".format(random.uniform(1, 3)))
        L                      = float("{:.2f}".format(random.uniform(0.5, 2)))
        D                      = float("{:.4f}".format(random.uniform(degradation_lb, 1)))
        
        n_maintenance_actions  = random.randint(1,1) # debug: be very careful with more maintenance actions, you'd need to put them in indices for the duration#, 3) # number of different possible maintenance actions
        maintenance_duration   = {0: random.randint(1, 3)} # number of production periods maintenance takes. Deeper maintenance requires more periods
        for i in range(1, n_maintenance_actions):
            maintenance_duration[i] = maintenance_duration[i-1] + random.randint(1, 3)

        assert component_name not in cur_components, "Two components can't share the same name!"

        cur_components[component_name] = Component(component_name, Rmax, C, Q, L, D, n_maintenance_actions, maintenance_duration)
        machine_Q = min(machine_Q, Q)

    # Component degradation
    for index, component_name in enumerate(cur_components):

        degradation_type_sample = random.random()
        if force_linear or degradation_type_sample <= 0.7:
            degradation_type = "linear"
        elif degradation_type_sample <= 0.9:
            degradation_type = "polynomial"
        else:
            degradation_type = "exponential"
            
        production_degradation, degradation_str = get_component_degradation(
            degradation_type=degradation_type,
            source="load",
            seed=params["global_seed"]+index
        )
        cur_components[component_name].production_degradation = production_degradation
        cur_components[component_name].data["production_degradation"] = degradation_str

        limit_type_sample = random.random()
        if force_linear or limit_type_sample <= 0.7:
            limit_type = "linear"
        elif limit_type_sample <= 0.9:
            limit_type = "polynomial"
        else:
            limit_type = "exponential"

        production_limit, limit_str = get_production_limit(limit_type=limit_type, seed=2*params["global_seed"]+index)
        cur_components[component_name].production_limit = production_limit
        cur_components[component_name].data["production_limit"] = limit_str

        # Inter-component interaction
        for other_index, other_component_name in enumerate(cur_components):
            if component_name == other_component_name:
                continue

            if complexity == "low" and random.random() <= 0.1 or complexity == "high" and random.random() <= 0.15:
                cur_components[component_name].maintenance_dependencies.append(cur_components[other_component_name])

            if complexity == "low" and random.random() <= 0.1 or complexity == "high" and random.random() <= 0.15:                
                degradation_type_sample = random.random()
                if degradation_type_sample <= 0.7:
                    degradation_type = "linear"
                elif degradation_type_sample <= 0.9:
                    degradation_type = "polynomial"
                else:
                    degradation_type = "exponential"

                degradation, degradation_str = get_component_degradation(
                    degradation_type=degradation_type,
                    source="component",
                    seed=params["global_seed"]+other_index+len(cur_components)
                    )

                cur_components[component_name].degradation_dependencies.append((cur_components[other_component_name],degradation))
                cur_components[component_name].data["degradation_dependencies"][other_component_name] = degradation_str

    n = Machine(0, components=cur_components)
    n.Q = machine_Q
    n.n_production_levels = params["discrete_production"]
    return n

def get_component_degradation(degradation_type, source, seed=37):
    random.seed(seed)

    # load probably has a bigger impact that any individual component (maybe)
    if source == "load":
        max_slope       = 3
        max_intercept   = 0 # no production implies no production-based degradation
        max_n_exponents = 3
        max_exponents   = 3 # Always convex in the domain that matters
        min_basis       = 0.1
        max_basis       = 3
        max_exponent    = 3
        K_min, K_max = 0.5, 5.0
        k_min, k_max = 0.5, 2.0
        t_min, t_max = 0.5, 2.0
        max_n_terms = 3
        p_min, p_max = 1.0, 3.0
    else:
        max_slope       = 2
        max_intercept   = 4
        max_n_exponents = 1
        max_exponents   = 2
        min_basis       = 0.1
        max_basis       = 0.9
        max_exponent    = 2
        K_min, K_max = 0.2, 4.0
        k_min, k_max = 0.3, 1.5
        max_n_terms = 2
        p_min, p_max = 1.0, 2.0
    
    K = float(f"{random.uniform(K_min, K_max):.3f}")

    # helper: shift x -> t in [0,1] via t = x - 1
    # This way, g(1)=0 corresponds to t=0; g(2)=K corresponds to t=1.

    if degradation_type == "linear":
        # g(x) = K * (x - 1), convex and increasing on [1,2]
        degradation = lambda x: K * (x - 1.0)
        degradation_str = f"{K}*(x - 1)"

    elif degradation_type == "polynomial":
        # g(x) = K * sum_i w_i * (x - 1)^{p_i}, with p_i >= 1, sum w_i = 1
        # Convex, increasing on x in [1,2], normalized: g(1)=0, g(2)=K
        n = random.randint(1, max_n_terms)
        exponents = [float(f"{round(random.uniform(p_min, p_max),2)}") for _ in range(n)]
        raw_weights = [float(f"{round(random.uniform(0.1, 3.0),2)}") for _ in range(n)]
        s = sum(raw_weights)
        weights = [c/s for c in raw_weights]

        degradation = lambda x, K=K, weights=weights, exponents=exponents, n=n: K*sum(weights[i]*(x - 1.0)**exponents[i] for i in range(n))
        degradation_str = f"{K}*(" + " + ".join(f"{weights[i]:.3f}*(x - 1)**{exponents[i]:.3f}" for i in range(n)) + ")"

    elif degradation_type == "exponential":
        # Convex normalized exponential on [1,2], regardless of random base selection:
        # Use base-e form with positive slope parameter alpha = k*|log(basis)|.
        # g(x) = K * (exp(alpha*(x-1)) - 1) / (exp(alpha) - 1)
        k = float(f"{round(random.uniform(k_min, k_max),2)}")
        basis = float(f"{round(random.uniform(min_basis, max_basis),2)}")
        alpha = k * abs(math.log(basis)) if basis > 0 else k  # safeguard, though basis is >0 by construction
        denom_e = basis**k - 1.0
        if abs(denom_e) < 1e-8:
            degradation = lambda x, K=K: K * (x - 1.0)
            degradation_str = f"{K}*(x - 1)  # limit as alpha→0 of normalized exponential"
        else:
            degradation = lambda x, K=K, alpha=alpha: K * (scip.exp(alpha*(x - 1.0)) - 1.0) / (scip.exp(alpha) - 1.0)
            degradation_str = f"{K}*((exp({alpha}*(x - 1)) - 1)/(exp({alpha}) - 1))"
    else:
        raise ValueError(f"Unknown degradation type: {degradation_type}")

    # Optional debug-only sanity checks: verify monotonicity and convexity on [1,2]
    if CHECK_CONVEXITY:
        from generate_initial_pricing_columns import _eval
        try:
            a, b, grid_n = 1.0, 2.0, 50
            h = (b - a) / grid_n
            xs = [a + i*h for i in range(grid_n+1)]
            vals = [_eval(str(degradation(x))) for x in xs]
            ys = [ v for v in vals ]
            
            pass
            # Monotone nondecreasing
            for i in range(1, len(ys)):
                if ys[i] + 1e-9 < ys[i-1]:
                    raise AssertionError(f"degradation is not nondecreasing at x≈{xs[i]:.3f}: {ys[i-1]:.6g} -> {ys[i]:.6g}")
            # Convex: discrete second differences >= 0 (within tol)
            for i in range(1, grid_n):
                sec = ys[i+1] - 2*ys[i] + ys[i-1]
                if sec < -1e-8:
                    raise AssertionError(f"degradation is not convex at x≈{xs[i]:.3f}: second diff {sec:.6g}")
        except Exception as _dbg_e:
            # Surface the error with context
            raise AssertionError(f"DEBUG_CONVEXITY_SANITY failed for type={degradation_type}, source={source}: {_dbg_e}")

    return degradation, degradation_str

def get_production_limit(limit_type, seed = 1000000000000066600000000000001):
    """
    Gets the limit on the production given the condition of a particular component. The g functions in 
    the formulation.
    """

    random.seed(seed)
    # it's difficult to estimate these. It will depend heavily on the load that they operate on
    # todo bring the parameters here and make these a function of the demand somehow
    min_slope       = 3
    max_n_exponents = 3
    max_exponents   = 4
    min_basis       = 3
    min_exponent    = 3
    min_k = 1.1
    max_k = 3.0

    if limit_type == "linear":
        slope = float("{:.2f}".format(random.randint(min_slope, min_slope+2)))
        intercept = 0 # if component is at 0, then no production is possible
        limit = lambda x: slope*x + intercept
        limit_str = f"{slope}*x + {intercept}"

    # concave sum of powers with exponents in (0,1], nonnegative weights; normalized to <= 1
    elif limit_type == "polynomial":
        k = random.randint(1, max_n_exponents)
        exponents = [float("{:.3f}".format(random.uniform(0.3, 1.0))) for _ in range(k)]
        coefs_raw = [float("{:.3f}".format(random.uniform(0.1, 1.0))) for _ in range(k)]
        s = sum(coefs_raw)
        coefs = [c/s for c in coefs_raw]  # normalize so f(1)=1

        # Note: x is expected to be r/Rmax in [0,1]
        limit = lambda x: sum(coefs[i] * x**exponents[i] for i in range(len(exponents)))
        terms = [f"{ws_i:.3f}*x**{p_i:.3f}" for ws_i, p_i in zip(coefs, exponents)]
        limit_str = " + ".join(terms)

    elif limit_type == "exponential":
        # Concave, saturating form normalized on [0,1]: (1 - exp(-k x)) / (1 - exp(-k))
        k = float("{:.3f}".format(random.uniform(min_k, max_k)))
        denom = 1.0 - scip.exp(-k)
        limit = lambda x, k=k, denom=denom: (1.0 - scip.exp(-k*x)) / denom
        limit_str = f"(1 - exp(-{k}*x)) / (1 - exp(-{k}))"
    else:
        limit = None
        limit_str = None

    return limit, limit_str

# Instance set creation

def create_instance_set(set_seed=1, **kwargs) -> dict:
    """
    Creates a set of instances to the machine-scheduling problem.

    kwargs:
    """

    random.seed(set_seed)

    kwargs["T"] = [i for i in range(1,kwargs["T"]+1)]
    kwargs["machines_per_group"] = eval(kwargs["machines_per_group"])

    for i in range(kwargs["n_instances"]):
        if "specific_instance" in kwargs and kwargs["specific_instance"]:
            i = kwargs["specific_instance"]

        filename = "%s_%ix%sx%i" % (kwargs["complexity"], len(kwargs["T"]), kwargs["machines_per_group"], i)
        if kwargs["force_linear"]:
            filename += "_linear"
        filename += ".py"

        kwargs["seed"] = random.random() # I think this may not be a good way to do this

        params = create_individual_instance(kwargs=kwargs) 

        filename = filename.replace("[", "")
        filename = filename.replace("]", "")
        filename = filename.replace(",", "_")
        filename = filename.replace(" ", "")

        full_path = "Instances/" + kwargs["prefix"] + filename

        params["filename"] = filename
        params["PT"] = kwargs["PT"]

        with open(full_path, "w+") as file:
            file.write("import os\n")
            file.write("import sys\n")
            file.write("sys.path.insert(1, os.path.join(sys.path[0], '..'))\n")
            if kwargs["PT"]:
                file.write("from testing import PT_get_random_machine\n\n\n")
            else:
                file.write("from testing import get_random_machine\n\n\n")
            file.write("params = " + str(params) + "\n")     
            for index in range(len(params["machines_per_group"])):
                if kwargs["PT"]:
                    file.write("\nparams[" + str(index) + "] = PT_get_random_machine(params=params, seed=" + str(kwargs["seed"] + index) + ")\n" )
                else:
                    file.write("\nparams[" + str(index) + "] = get_random_machine(seed = " + str(kwargs["seed"] + index) + ",complexity=\"" + kwargs["complexity"] + "\",force_linear="+str(kwargs["force_linear"])+",params=params)\n" )

def create_individual_instance(kwargs):
    """
    Creates an instance to the machine-scheduling problem.

    kwargs:
    """

    seed              = kwargs["seed"]
    T                 = kwargs["T"]
    T_prime           = [t for t in range(1,len(kwargs["T"]) * kwargs["production_granularity"] + 1)]
    linear_relaxation = kwargs["force_linear"]
    n_machines        = sum(kwargs["machines_per_group"])
    peak_demand       = kwargs["peak_demand"]

    params = get_random_global_parameters(T_prime=T_prime, n_machines=n_machines, seed=seed, linear_relaxation=linear_relaxation, peak_demand=peak_demand)

    params["machines_per_group"]             = kwargs["machines_per_group"]
    params["n_groups"]                       = len(params["machines_per_group"])
    params["N"]                              = [i for i in range(sum(params["machines_per_group"]))]
    params["T"]                              = kwargs["T"]
    params["production_granularity"]         = len(params["T_prime"])/len(params["T"])
    params["discrete_production"]            = kwargs["discrete_production"]
    params["dual_stabilization"]             = kwargs["dual_stabilization"]
    params["redcost_fixing"]                 = kwargs["redcost_fixing"]
    params["debug_mode"]                     = kwargs["debug_mode"]
    params["stop_at_error"]                  = kwargs["stop_at_error"]
    params["force_linear"]                   = kwargs["force_linear"]
    params["ARMP_use_original_pricing"]      = kwargs["ARMP_use_original_pricing"]
    return params

# Testing

def run_instance(**kwargs):
    """
    Runs an individual instance from the created instance set.

    Default heuristic = 1 is exact pricing. Does not affect compact formulation.
    """
    filename                        = kwargs["filename"]
    model                           = kwargs["model"]
    plot                            = kwargs["plot"]
    discrete_production             = kwargs["discrete_production"]
    production_granularity          = kwargs["production_granularity"]
    reopt                           = kwargs["reopt"]
    feasibility                     = kwargs["feasibility"]
    heuristic                       = kwargs["heuristic"]
    price_and_branch                = kwargs["price_and_branch"]
    dual_stabilization              = kwargs["dual_stabilization"]
    redcost_fixing                  = kwargs["redcost_fixing"]
    compact_run                     = kwargs["compact_run"]
    redirect_output                 = kwargs["redirect_output"]
    parallel                        = kwargs["parallel"]
    verbose                         = kwargs["verbose"]
    debug_mode                      = kwargs["debug_mode"]
    stop_at_error                   = kwargs["stop_at_error"]
    force_linear                    = kwargs["force_linear"]
    linear_relaxation               = kwargs["linear_relaxation"]
    time_limit                      = kwargs["time_limit"]
    n_workers                       = kwargs["n_workers"]
    ARMP_use_original_pricing       = kwargs["ARMP_use_original_pricing"]

    # [webui] Optional callback to expose the model to the web GUI before optimize
    #         so the worker can interrupt solving (Stop button). If provided, it
    #         will be called once with the freshly built model.
    webui_on_model         = kwargs.get("webui_on_model")
    if filename[:3] == "PT_":
        kwargs["PT"] = True
        PT = True
    else:
        kwargs["PT"] = False
        PT = False

    prefix = ""
    if filename.split("_")[0] not in ["low", "high"]:
        prefix = filename.split("_")[0] + "_"

    # instance               = {} #linter
    # params                 = {} #linter


    if "new_instance" not in kwargs:
        new_instance = False
        # pricer = None #linter
        try:
            instance = import_module("Instances." + filename, "")
            for param in ["discrete_production", "production_granularity", "force_linear"]:
                if instance.params[param] != kwargs[param]:
                    new_instance = True
                    break

        except ModuleNotFoundError:
            new_instance = True
    else:
        new_instance = kwargs["new_instance"]

    if new_instance:
        machines_per_group = ("[" + filename.split("x")[1] + "]").replace("_", ",")
        if "linear" in filename:
            force_linear = True
            filename = filename.replace("_linear", "")
        
        if prefix:
            filename = filename.replace(prefix, "")

        kwargs = {"complexity":filename.split("_")[0],
                    "T":int(filename.split("_")[1].split("x")[0]),
                    "machines_per_group":machines_per_group,
                    "n_instances":1,
                    "specific_instance": int(filename.split("x")[2]),
                    "force_linear": force_linear,
                    "dual_stabilization": dual_stabilization,
                    "redcost_fixing": redcost_fixing,
                    "prefix":"PT_" if "PT" in filename else "",
                    "production_granularity":production_granularity, # todo: incorporate this into filename
                    "discrete_production":discrete_production,
                    "debug_mode": debug_mode,
                    "stop_at_error": stop_at_error,
                    "peak_demand":False,
                    "prefix": prefix,
                    "PT": PT,
                    "n_workers": n_workers,
                    "ARMP_use_original_pricing": ARMP_use_original_pricing
                    }

        params = create_instance_set(**kwargs)
        if force_linear:
            filename += "_linear"
        instance = import_module("Instances." + prefix+filename, "")

    params = instance.params
    model = int(model)

    params["filename"]                   = filename
    params["model"]                      = int(model)
    params["heuristic"]                  = int(heuristic)
    params["price_and_branch"]           = int(price_and_branch)
    params["dual_stabilization"]         = int(dual_stabilization)
    params["redcost_fixing"]             = int(redcost_fixing)
    params["compact_run"]                = int(compact_run)
    params["verbose"]                    = int(verbose)
    params["debug_mode"]                 = debug_mode
    params["linear_relaxation"]          = int(linear_relaxation)
    params["time_limit"]                 = int(time_limit)
    params["reopt"]                      = reopt
    params["n_workers"]                  = n_workers
    params["ARMP_use_original_pricing"]  = kwargs["ARMP_use_original_pricing"]


    stats = {}
    # Ensure heavy modules are loaded (lazy import fallback)
    global create_model, sequential_pricer, parallel_pricer
    if model == 1:
        if create_model is None:
            try:
                from create_model import create_model
            except Exception as e:
                raise
        # compact
        m = create_model(params=params)
        m.data = {}
        if feasibility: # to get a faster idea of instance status
            m.setEmphasis(scip.SCIP_PARAMEMPHASIS.FEASIBILITY)
    else:
        init_start = time()
        if parallel:
            if parallel_pricer is None:
                try:
                    import importlib as _il
                    parallel_pricer = _il.import_module("parallel_pricer")  # type: ignore
                except Exception as e:
                    raise
            m = parallel_pricer.create_pricer(params=params)
        else:
            if sequential_pricer is None:
                try:
                    import importlib as _il
                    sequential_pricer = _il.import_module("sequential_pricer")  # type: ignore
                except Exception as e:
                    raise
            m = sequential_pricer.create_pricer(params=params)
        pricer = m[1]
        m = m[0]

        init_time = time() - init_start
        m.data["setup_time"] = init_time
        pricer.data["master_time"] = 0

    m.data["sols"] = []
    m.data["sols_time"] = []
    m.data["gap_at_sol"] = []
    m.data["found_best_sol_since_last_redcost_fixing"] = {1: False}
    if model != 1:
        solsHdlr = solsEventHdlr(m)
        m.includeEventhdlr(solsHdlr, "Solutions Event handler", "To record some information")

    if not verbose:
        m.hideOutput()

    m.setParam('limits/time', params["time_limit"])
    m.setParam("display/freq", 1)

    for param in ["numerics/epsilon", "numerics/dualfeastol", "numerics/feastol", "numerics/sumepsilon"]:
        old_value = m.getParam(param)
        #m.setParam(param, old_value*100)

    params["start_time"] = time() # for correctly stopping the pricing problems

    # [webui] Allow the web app to capture the model handle just before optimization
    try:
        if callable(webui_on_model):
            try:
                webui_on_model(m)
            except Exception:
                pass
    except Exception:
        pass

    try:
        if redirect_output:
            log_name = ""

            if model == 1:
                log_name = f"./Results/Compact/Logs/{filename}"
            elif model == 0 and heuristic <= 1:
                log_name = f"./Results/DW/Logs/{filename}"
            elif model == 0 and heuristic == 2:
                log_name = f"./Results/DW_PF/Logs/{filename}"

            # [webui] Ensure log directory exists when redirecting output
            try:
                os.makedirs(os.path.dirname(log_name), exist_ok=True)
            except Exception:
                pass

            m.setLogfile(log_name+"_SCIP.log")
            with open(log_name+".log", "w") as f, redirect_stdout(f), redirect_stderr(f):
                m.optimize()
        else:
            m.optimize()
    except Exception as e:
        try:
            os.makedirs("skipped_instances", exist_ok=True)
            with open(f"skipped_instances/{filename}.log", "a") as error_file:
                error_file.write("Skipped instance %s\n" % filename)
                error_file.write(f"{type(e).__name__}: {e}\n")
                error_file.write(traceback.format_exc())
                error_file.write("\n" + "-"*80 + "\n")
        except Exception:
            pass

        # Try to persist diagnostics for post-mortem
        try:
            kind = None
            if model == 1:
                kind = "Compact"
            elif model == 0 and heuristic <= 1:
                kind = "DW"
            elif model == 0 and heuristic == 2:
                kind = "DW_PF"
            else:
                kind = "DW"
            diag_dir = os.path.join("./Results", kind, "Diagnostics")
            os.makedirs(diag_dir, exist_ok=True)
            # Problem files (orig or transformed)
            try:
                m.writeProblem(os.path.join(diag_dir, filename + ".cip"))
            except Exception:
                pass
            try:
                m.writeTransProblem(os.path.join(diag_dir, filename + ".lp"), genericnames=False)
            except Exception:
                pass
            # Stats if any
            try:
                m.writeStatistics(os.path.join(diag_dir, filename + ".stats"))
            except Exception:
                pass
        except Exception:
            pass

        try:
            if model != 1:
                if "error" not in m.data.get("pricer", {}).get("data", {}):
                    m.data["pricer"].data["error"] = True
                else:
                    m.data["pricer"].data["error"] = True
        except Exception:
            pass

        if stop_at_error:
            raise
        return m, None

    # Close the final master-time slice at the exact end of SCIP's optimize(),
    # before any feasibility checks or post-processing add overhead.
    if model != 1:
        pricer = m.data["pricer"]
        now = time()
        last_end = pricer.data.get("last_callback_end", pricer.data.get("master_start_time", now))
        pricer.data["master_time"] = pricer.data.get("master_time", 0.0) + max(0.0, now - last_end)
        pricer.data["last_callback_end"] = now

    if not model == 1 and params["heuristic"] == 2 and params["verbose"] >= 3:
        print("Heuristics n_successes vs n_calls %i/%i" % (pricer.data["heuristics"]["success"], pricer.data["heuristics"]["total"]))

    if model == 0:
        if m.getNSols() > 0 or m.data["pricer"].data["repair_step"]["n_successes"] > 0: # we may have hidden integer solution
            try:
                assert pricer_is_feasible(model=m, params=params)
            except AssertionError:
                # Persist the offending solution for later inspection
                try:
                    cur_recipe = _compute_recipe_id()
                    default_results_file = os.path.join("./Results", "recipes", cur_recipe, "optimal_results.txt")
                    # Determine method tag similar to other savers
                    model_val = params.get("model")
                    if model_val == 1:
                        method_tag = "Compact"
                    elif model_val == 0:
                        method_tag = "DW"
                    elif model_val == 2:
                        method_tag = "DW_PF"
                    else:
                        method_tag = f"model{model_val}"
                    # Is repaired optimal?
                    is_rep = None
                    try:
                        bsol = m.data["pricer"].best_sol
                        if isinstance(bsol, dict) and "obj" in bsol and isinstance(bsol["obj"], (int, float)):
                            if not m.isInfinity(bsol["obj"]) and m.isLT(bsol["obj"], m.getPrimalbound()):
                                is_rep = True
                            else:
                                is_rep = False
                    except Exception:
                        is_rep = None
                    save_infeasible_solution_debug(m, filename, results_file=default_results_file, recipe=cur_recipe, method_tag=method_tag, is_repaired=is_rep)
                finally:
                    raise

        stats["n_heuristic_cols"] = m.data["pricer"].heuristic_cols
        stats["n_optimal_cols"]   = m.data["pricer"].optimal_cols

        if params["verbose"] >= 2:
            m.data["pricer"].print_pricing_timings()

    elif model == 2:
        if m.getNSols() > 0:
            try:
                assert ARMP_is_feasible(model=m, params=params)
            except AssertionError:
                try:
                    cur_recipe = _compute_recipe_id()
                    default_results_file = os.path.join("./Results", "recipes", cur_recipe, "optimal_results.txt")
                    method_tag = "DW_PF"
                    save_infeasible_solution_debug(m, filename, results_file=default_results_file, recipe=cur_recipe, method_tag=method_tag)
                finally:
                    raise
            if params["verbose"] >= 2:
                m.data["pricer"].print_pricing_timings()
        else:
            pass # assert ARMP_columns_are_compatible(model=m, params=params)
    
    if plot and model != 1:
        plot_dual_values(m.data["pricer"], filename)
    
    return m, stats

# to record the solutions and time they were found in
class solsEventHdlr(scip.Eventhdlr):

    def eventinit(self):
        self.model.catchEvent(scip.SCIP_EVENTTYPE.BESTSOLFOUND, self)
        self.pricer = self.model.data["pricer"]

    def eventexec(self, event):
        try:
            return self._eventexec(event)
        except Exception as e:
            log_error("_eventexec", e, self.pricer.data["params"]["filename"], self.pricer.data["params"]["stop_at_error"])
            self.pricer.data["error"] = True
            return {"error": str(e)}
    
    def _eventexec(self, event):
        primal_sol = self.model.getBestSol()
        primal = round(self.model.getSolObjVal(primal_sol))
        if self.model.isLT(primal, self.pricer.primal_bound):
            self.pricer.primal_bound = primal
            self.pricer.best_sol = primal_sol

        global_dual = self.model.getDualbound()
        self.model.data["sols"].append(primal)
        self.model.data["sols_time"].append(self.model.getTotalTime())
        self.model.data["gap_at_sol"].append(100*abs(global_dual - primal) / abs(global_dual+10e-6))            

def run_instance_set(**kwargs):

    objval = {}
    time = {}
    gap = {}
    n_nodes = {}
    dual = {}
    model = {}

    total_instances = 2*2*2*50
    counter = 0
    # Getting optimal solutions from previous runs
    is_infeasible, is_optimal, best_primals, best_duals = retrieve_stored_optimal_sols()
    for complexity in ["low","high"]:
        for n_years in [10,20]:#,50]:
            for machines_per_group in ["10_10", "20"]:#["8", "10_10", "20"]:#["20","5_2","2_2_2_2"]:
                for instance_nr in range(50):
                    if kwargs["PT"]:
                        filename = "PT_%s_%ix%sx%i" % (complexity, n_years, machines_per_group, instance_nr)
                    else:
                        filename = "%s_%ix%sx%i" % (complexity, n_years, machines_per_group, instance_nr)

                    if kwargs["force_linear"]:
                        filename += "_linear"

                    # Ensure dictionaries are initialized for the effective filename (after any suffixing)
                    if filename not in is_infeasible:
                        is_infeasible[filename] = None
                        is_optimal[filename] = False
                        best_primals[filename] = float("inf")
                        best_duals[filename] = -float("inf")

                    print("Running instance: ", filename) 

                    instance_args = {
                            "filename":               filename,
                            "discrete_production":    kwargs["discrete_production"],
                            "debug_mode":             kwargs["debug_mode"],
                            "feasibility":            kwargs["feasibility"],
                            "force_linear":           kwargs["force_linear"],
                            "linear_relaxation":      kwargs["linear_relaxation"],
                            "dual_stabilization":     kwargs["dual_stabilization"],
                            "redcost_fixing":         kwargs["redcost_fixing"],
                            "production_granularity": kwargs["production_granularity"],
                            "compact_run":            kwargs["compact_run"],
                            "redirect_output":        kwargs["redirect_output"],
                            "stop_at_error":          kwargs["stop_at_error"],
                            "model":                  kwargs["model"],
                            "heuristic":              kwargs["heuristic"],
                            "price_and_branch":       kwargs["price_and_branch"],
                            "verbose":                kwargs["verbose"],
                            "time_limit":             kwargs["time_limit"],
                            "PT":                     kwargs["PT"],
                            "parallel":               kwargs["parallel"],
                            "n_workers":              kwargs["n_workers"],
                            "ARMP_use_original_pricing": kwargs["ARMP_use_original_pricing"],
                            "plot":                   False,
                            "reopt":                  False,
                            }

                    m, run_stats = run_instance(**instance_args)

                    if kwargs["statistics"] and not (kwargs["model"] != 1 and "error" in  m.data["pricer"].data):

                        model[filename] = m # might be easier to just get the results afterwards. Might also be too much memory

                        if kwargs["model"] == 1:
                            prefix = "./Results/Compact/"
                            data_prefix = "./Results/Compact/Data/"
                        elif kwargs["heuristic"] <= 1:
                            prefix = "./Results/DW/"
                            data_prefix = "./Results/DW/Data/"
                        else:
                            prefix = "./Results/DW_PF/"
                            data_prefix = "./Results/DW_PF/Data/"

                        if kwargs["model"] == 0 and kwargs["parallel"]:
                            prefix = prefix[:-1] + "_parallel/"

                        m.writeStatistics(prefix + "Statistics/"+filename+".stats")

                        if kwargs["model"] != 1:
                            gcd = m.data["pricer"].data["gcd"]
                        else:
                            gcd = 1

                        optimal_sol_is_repaired = False
                        if kwargs["model"] == 0:
                            optimal_sol_is_repaired = not m.isInfinity(m.data["pricer"].best_sol["obj"]) and \
                                                        m.isLT(m.data["pricer"].best_sol["obj"], m.getPrimalbound())
                        
                        if optimal_sol_is_repaired:
                            objval[filename] = m.data["pricer"].best_sol["obj"]

                        if kwargs["model"] == 0:
                            n_cols = m.getNVars(True)
                            n_heuristic_cols = m.data["pricer"].data["heuristics"]["total"]
                        else:
                            n_cols = 0
                            n_heuristic_cols = 0

                        result_file = prefix + "x".join(filename.split("x")[:2]) + ".txt"
                        instance_number = filename.split("x")[2]

                        if instance_nr == 0:
                            with open(result_file, "w") as header: 
                                header.write("N | OPT | Gap(%) | Nodes | Obj | Dual | N Cols | Time(s)\n")
                                header.write(48*"-" + "\n")

                        data_file = data_prefix + filename + "_data.txt"
                        with open(data_file, "w+") as file:
                            # file.write(str(m.data))
                            file.write(json.dumps(m.data, default=str)) # careful, this may fail with non-serializable data
                            if kwargs["model"] != 1:
                                file.write("\n")
                                keys_to_exclude = ["patterns", "dualSolutions", "previous_redcosts", "last_branching", "branching_cons", "branching_decisions", "filtered_mvars", "Delta_patterns", "Mu_patterns", "Delta", "Mu", "full_patterns", "pattern_encoding", "integer_enconding", "integer_patterns", "integer_encoding", "continuous_patterns", "continuous_encoding", "mvars_by_integer_variable", "var", "young_vars"]
                                dict_to_write = {k: str(v) for k, v in m.data["pricer"].data.items() if k not in keys_to_exclude}

                                file.write("\n\n" + str(dict_to_write))

                        with open(result_file, "a") as result_file:
                            if kwargs["model"] == 0 and optimal_sol_is_repaired:
                                objval[filename]  = m.data["pricer"].best_sol["obj"] # repaired solution has implicit integrality
                                objval[filename]  = gcd*m.feasFloor(objval[filename])
                                time[filename]    = m.getSolvingTime()
                                dual[filename]    = min(m.getDualbound(), objval[filename]) # because SCIP doesn't know the solution is integer and we're cutting off subtrees, it may mark it as infeasible
                                dual[filename]    = gcd*m.feasCeil(dual[filename])
                                gap[filename]     = 0 if objval[filename]==dual[filename] else m.getGap()*100 if dual[filename] > 0.001 else 100*objval[filename] # percentage
                                n_nodes[filename] = m.getNNodes() - m.data["pricer"].data["repair_step"]["n_successes"] # removing these nodes since they're artificially created and imediately discarded
                                if m.isGT(m.getSolvingTime(), kwargs["time_limit"]): # Timeout
                                    assert m.isGE(objval[filename], best_duals[filename]), "Solution is better than previously found dual bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_duals[filename])
                                    assert m.isLE(dual[filename], best_primals[filename]), "Dual is worse than previously found primal bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                    result_file.write("%s | %i | %.2f | %i | %.2f | %.2f | %i | %i | Timeout\n" % (instance_number, m.isZero(gap[filename]), gap[filename], n_nodes[filename], objval[filename], dual[filename], n_cols, n_heuristic_cols))                                
                                else:
                                    if is_optimal[filename]:
                                        assert m.isEQ(objval[filename], best_primals[filename]), "Primal does not match previously found optimal solution for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                    else:
                                        assert m.isGE(objval[filename], best_duals[filename]), "Primal is worse than previously found dual bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_duals[filename])
                                        assert m.isLE(dual[filename], best_primals[filename]), "Dual is worse than previously found primal bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                    result_file.write("%s | %i | %.2f | %i | %.2f | %.2f | %i | %i | %.2f\n" % (instance_number, m.isZero(gap[filename]), gap[filename], n_nodes[filename], objval[filename], dual[filename], n_cols, n_heuristic_cols, time[filename]))
                            else:
                                if m.getNSols() > 0: # found solution (optimal or suboptimal)
                                    objval[filename]  = gcd*m.feasFloor(m.getPrimalbound())
                                    time[filename]    = m.getSolvingTime()
                                    dual[filename]    = gcd*m.feasCeil(m.getDualbound())
                                    gap[filename]     = m.getGap()*100 if (dual[filename] > 0.001 or objval[filename]==dual[filename]) else 100*objval[filename] # percentage
                                    n_nodes[filename] = m.getNNodes()
                                    if m.isGT(m.getSolvingTime(), kwargs["time_limit"]): # Timeout
                                        assert m.isGE(objval[filename], best_duals[filename]), "Primal is smaller than previously found dual bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_duals[filename])
                                        assert m.isLE(dual[filename], best_primals[filename]), "Dual is larger than previously found primal bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                        result_file.write("%s | %i | %.2f | %i | %.2f | %.2f | %i | %i | Timeout\n" % (instance_number, m.isZero(gap[filename]), gap[filename], n_nodes[filename], objval[filename], dual[filename], n_cols, n_heuristic_cols))                                
                                    else:
                                        if is_optimal[filename]:
                                            assert m.isEQ(objval[filename], best_primals[filename]), "Solution does not match previously found optimal solution for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                        else:
                                            assert m.isGE(objval[filename], best_duals[filename]), "Primal is smaller than previously found dual bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_duals[filename])
                                            assert m.isLE(dual[filename], best_primals[filename]), "Dual is larger than previously found primal bound for instance %s: %.2f vs %.2f" % (filename, objval[filename], best_primals[filename])
                                        result_file.write("%s | %i | %.2f | %i | %.2f | %.2f | %i | %i | %.2f\n" % (instance_number, m.isZero(gap[filename]), gap[filename], n_nodes[filename], objval[filename], dual[filename], n_cols, n_heuristic_cols, time[filename]))
                                else:
                                    if m.getStage() != 10 or m.isGT(m.getSolvingTime(), kwargs["time_limit"]): # Timeout
                                        objval[filename] = "-"
                                        gap[filename]    = "-"
                                        time[filename]   = "-"
                                        dual[filename]   = "-" if m.isInfinity(abs(m.getDualbound())) else round(gcd*m.getDualbound(),2) 
                                        n_nodes[filename] = m.getNNodes()
                                        result_file.write("%s | - | - | %i | - | %s | %i | %i | Timeout\n" % (instance_number, n_nodes[filename], str(dual[filename]), n_cols, n_heuristic_cols))
                                    else: #infeasible
                                        time[filename]   = m.getSolvingTime()
                                        n_nodes[filename] = m.getNNodes()
                                        if is_infeasible[filename] is None:
                                            is_infeasible[filename] = True
                                        else:
                                            assert is_infeasible[filename], "Instance %s was previously found to be feasible!" % filename
                                        result_file.write("%s | Infeasible | - | %i | - | - | %i | %i | %.2f\n" % (instance_number, n_nodes[filename], n_cols, n_heuristic_cols, time[filename]))


                    counter += 1
                    print("Finished instance %i/%i." % (counter, total_instances))

                    # Persist best-known results for this instance
                    # We pass floats or None to the storage helper; no placeholders like "-".
                    def _as_float_or_none(v):
                        return v if isinstance(v, (int, float)) else None

                    pobj = _as_float_or_none(objval.get(filename))
                    dval = _as_float_or_none(dual.get(filename))
                    flag = is_infeasible.get(filename)
                    infeas = bool(flag) if flag is not None else False
                    err_msg = None
                    # Try to capture any error message recorded in pricer's data
                    try:
                        err_msg = m.data["pricer"].data.get("error")
                        if isinstance(err_msg, dict) and "message" in err_msg:
                            err_msg = err_msg["message"]
                    except Exception:
                        err_msg = None

                    # If timeout with no primal but finite dual, still record the dual bound improvement
                    # Also write best solution file beside the per-recipe results file (if any)
                    # We compute the default per-recipe path here to pass down for co-location.
                    cur_recipe = _compute_recipe_id()
                    default_results_file = os.path.join("./Results", "recipes", cur_recipe, "optimal_results.txt")
                    update_optimal_results(filename, pobj, dval, infeas, results_file=default_results_file, recipe=cur_recipe, error=err_msg)
                    # Method-specific tag to avoid overlapping solutions (Compact vs DW)
                    model_val = kwargs.get("model")
                    if model_val == 1:
                        method_tag = "Compact"
                    elif model_val == 0:
                        method_tag = "DW"
                    elif model_val == 2:
                        method_tag = "DW_PF"
                    else:
                        method_tag = f"model{model_val}"

                    # Determine if pricer repaired an optimal solution (available even when SCIP has no visible sol)
                    optimal_sol_is_repaired = None
                    try:
                        if hasattr(m, "data") and m.data.get("pricer") is not None:
                            bsol = m.data["pricer"].best_sol
                            if isinstance(bsol, dict) and "obj" in bsol and isinstance(bsol["obj"], (int, float)):
                                if not m.isInfinity(bsol["obj"]) and m.isLT(bsol["obj"], gcd*m.getPrimalbound()):
                                    optimal_sol_is_repaired = True
                                else:
                                    optimal_sol_is_repaired = False
                    except Exception:
                        optimal_sol_is_repaired = None

                    save_best_solution_file(m, filename, results_file=default_results_file, recipe=cur_recipe, method_tag=method_tag, keep_all=True, optimal_sol_is_repaired=optimal_sol_is_repaired)

# runs a bunch of instances in debug run while not stopping at first error
def debug_run(**kwargs):
    kwargs["debug_mode"] = True
    kwargs["stop_at_error"] = False
    kwargs["verbose"] = 0
    for n_runs in range(kwargs["n_runs"]):
        complexity = random.choice(["low", "high"])
        n_years = random.uniform(1,15)
        n_subprobs = random.randint(1,3)
        machines_per_group = random.sample(range(1,10), n_subprobs)
        str_machines_per_group = str(machines_per_group)[1:-1].replace(",", "_").replace(" ", "")
        kwargs["filename"] = "%s_%ix%sx%i" % (complexity, n_years, str_machines_per_group, 0)
        print("Running %s" % kwargs["filename"])
        m, _ = run_instance(**kwargs)
        if "error" not in m.data["pricer"].data:
            print("success")
        else:
            if kwargs["time_limit"] - m.getSolvingTime() <= 0.1:
                print("%s error, but also hit time limit" % kwargs["filename"])

# Stats
def group_instances_by_difficulty(models_to_use, all_instances, time_limit, skip_infeasible_instances=False):
    n_skipped_easy_instances = 0
    n_skipped_hard_instances = 0
    instance_by_difficulty = {"trivial": [], "easy": [], "medium": [], "hard": [], "impossible": [], "very_impossible": []}
    n_feasible_instances = {"trivial": 0, "easy": 0, "medium": 0, "hard": 0, "impossible": 0, "very_impossible": 0}
    all_prefixes = [f"./Results/{name}/Statistics/" for name in models_to_use]
    inf = True
    found_difficulty = False
    difficulty = ""

    for cur_instance in all_instances:
        if not inf and found_difficulty:
            n_feasible_instances[difficulty] += 1

        all_directories = [all_prefixes[i] + cur_instance for i in range(len(all_prefixes))]

        all_filenames = [all_directories[index]+".stats" for index in range(len(all_prefixes))]
        all_results = [scip.readStatistics(all_filenames[index]) for index in range(len(all_prefixes))]

        inf = False
        for index in range(len(all_prefixes)):
            if all_results[index].status == "infeasible":
                inf = True
                break
        if inf and skip_infeasible_instances:
            continue                

        found_difficulty = True
        for index in range(len(all_prefixes)):
            if all_results[index].total_time > time_limit/60:
                found_difficulty = False
                break

        if found_difficulty:
            instance_by_difficulty["trivial"].append(cur_instance)
            n_skipped_easy_instances += 1
            difficulty = "trivial"
            continue

        found_difficulty = False
        for index in range(len(all_prefixes)):
            if all_results[index].total_time <= time_limit/30:
                found_difficulty = True
                instance_by_difficulty["easy"].append(cur_instance)
                break
        
        if found_difficulty:
            difficulty = "easy"
            continue

        found_difficulty = False
        for index in range(len(all_prefixes)):        
            if all_results[index].total_time < time_limit:
                found_difficulty = True
                instance_by_difficulty["medium"].append(cur_instance)
                break
        
        if found_difficulty:
            difficulty = "medium"
            continue

        found_difficulty = False
        for index in range(len(all_prefixes)):
            if all_results[index].total_time >= time_limit:
                if all_results[index].n_solutions_found > 0:
                    found_difficulty = True
                    instance_by_difficulty["hard"].append(cur_instance)
                    break
        
        if found_difficulty:
            difficulty = "hard"
            continue
        else:
            instance_by_difficulty["impossible"].append(cur_instance)
            n_skipped_hard_instances += 1
            difficulty = "impossible"

    return instance_by_difficulty, n_feasible_instances

def generate_stats_report(**kwargs):
    """
    Gets model statistics (mean gap and stuff like that)

    trivial:    optimality < 10s
    easy:       optimality < 60s
    medium:     optimality < 2950s
    hard:       suboptimal solution at time limit
    impossible: found no solution at time limit
    """

    time_limit = kwargs["time_limit"]
    models_to_use = ["Compact", "DW"] #["Compact", "DW", "DW_PF"]:#, "DW_parallel", "DW_PF_parallel"]:

    all_instances = []
    for complexity in ["low","high"]:
            for n_years in [10,20]:#,30]:
                for machines_per_group in ["20","10_10"]:#,"7_7_6"]:
                    cur_instances = "%s_%ix%sx" % (complexity, n_years, machines_per_group) 
                    for i in range(50):
                        instance_name = cur_instances+str(i)
                        all_instances.append(instance_name)

    instances_by_difficulty, n_feasible_instances = group_instances_by_difficulty(models_to_use, all_instances, time_limit, skip_infeasible_instances=False) # todo: don't skip infeasible instances!!!

    print("Number of feasible instances by difficulty (out of 200):")
    for difficulty in ["trivial", "easy", "medium", "hard", "impossible"]:
        print("%10s: %i" % (difficulty, n_feasible_instances[difficulty]))

    print("Total feasible instances: %i" % (n_feasible_instances["easy"] + n_feasible_instances["medium"] + n_feasible_instances["hard"]))

    print("Number of instances by difficulty:")
    for difficulty in ["trivial", "easy", "medium", "hard", "impossible"]:
        print("%10s: %i" % (difficulty, len(instances_by_difficulty[difficulty])))
    print("Trivial and impossible instances were skipped in the main stats report.")

    # for latex pretty print
    stats = {i: {} for i in models_to_use}
    total_opt              = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_subopt           = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_infeasible       = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_timeout          = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_gap              = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_n_nodes          = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_n_cols           = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_n_heuristic_cols = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_time             = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    total_dual             = {"trivial": defaultdict(int), "easy": defaultdict(int), "medium": defaultdict(int), "hard": defaultdict(int), "impossible": defaultdict(int)}
    hard_no_sols           = {model: 0 for model in models_to_use}

    all_prefixes = [f"./Results/{name}/Statistics/" for name in models_to_use]
    for model in models_to_use:
        prefix = all_prefixes[models_to_use.index(model)]
        result_file = prefix + model + "_results"

        for difficulty in ["trivial", "easy", "medium", "hard", "impossible"]:
            for filename in instances_by_difficulty[difficulty]:
                stats_path = os.path.join(prefix, filename.split("/")[-1] + ".stats")
                assert os.path.isfile(stats_path), "Stats file %s not found!" % stats_path

                result = scip.readStatistics(stats_path)
                total_time[difficulty][model] += result.total_time
                if difficulty == "hard" and result.n_solutions_found == 0:
                    hard_no_sols[model] += 1

                if result.status == "infeasible":
                    if result.total_time >= time_limit: # D
                        assert model in ["DW", "DW_PF"]
                        total_timeout[difficulty][model] += 1
                    total_infeasible[difficulty][model] += 1
                    continue

                if result.status == "optimal":
                    total_opt[difficulty][model] += 1

                elif result.total_time >= time_limit:
                    total_subopt[difficulty][model] += 1

                if result.n_nodes:
                    total_n_nodes[difficulty][model] += result.n_nodes

                if result.gap:
                    if result.dual_bound == 0 and result.primal_bound != 0:
                        total_gap[difficulty][model] += result.primal_bound
                    else:
                        total_gap[difficulty][model] += result.gap
    

                if model != "Compact":
                    total_n_cols[difficulty][model] += result.n_presolved_vars

                if result.dual_bound:
                    total_dual[difficulty][model] += result.dual_bound

        with open(result_file, "w+") as file:
            #for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
            for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
                file.write(instance_type+"\n")

                file.write("Total optimal: %i\n" % (total_opt[instance_type][model]))
                file.write("Total suboptimal: %i\n" % (total_subopt[instance_type][model]))
                file.write("Total timeout: %i\n" % (total_timeout[instance_type][model]))
                file.write("Total infeasible: %i\n" % (total_infeasible[instance_type][model]))
                file.write("Total gap: %.2f%%\n" % (total_gap[instance_type][model]))
                file.write("Total nodes: %i\n" % (total_n_nodes[instance_type][model]))
                if model != "Compact":
                    file.write("Total n_cols: %i\n" % (total_n_cols[instance_type][model]))
                    file.write("Total n_heuristic_cols: %i\n" % (total_n_heuristic_cols[instance_type][model]))
                file.write("Total time: %.2f\n" % (total_time[instance_type][model]))
                if instance_type == "impossible":
                    file.write("Total dual: %.2f\n" % (total_dual["impossible"][model]))
                file.write("\n")
    
                stats[model][instance_type] = {
                    "instances": total_opt[instance_type][model] + total_subopt[instance_type][model] + total_infeasible[instance_type][model] + total_timeout[instance_type][model],
                    "time/gap":  "%is" % total_time[instance_type][model] if instance_type in ["easy", "medium"] else "%.0f\\%%" % (total_gap["hard"][model]) if instance_type == "hard" else "-",
                    "nodes": int(total_n_nodes[instance_type][model]),
                    "n_cols": total_n_cols[instance_type][model] if model != "Compact" else "-",
                    "n_heuristic_cols": total_n_heuristic_cols[instance_type][model] if model != "Compact" else "-"
                }


    print()
    print("Number of solved instances by model:")
    for model in models_to_use:
        print("%10s:" % model, end=" ")
        for difficulty in ["easy", "medium", "hard"]:
            print("(%i," % total_opt[difficulty][model] + "%i)" % total_infeasible[difficulty][model] +"/"+str(len(instances_by_difficulty[difficulty])), end=" ")
        print()
    
    n_instances = {d: len(instances_by_difficulty[d]) for d in ["easy", "medium", "hard"]}
    print_avg_gap_nodes_table(n_instances, n_feasible_instances, models_to_use, total_time, total_gap, total_n_nodes)

    print_latex_table(stats, models_to_use=models_to_use)

def print_avg_gap_nodes_table(n_instances, n_feasible_instances, models_to_use, total_time, total_gap, total_n_nodes):
    """
    Pretty table for 'Average gap|nodes by model' with aligned '|' per column.
    """
    difficulties = ["easy", "medium", "hard"]
    model_w = 12

    # Precompute cell parts per model/difficulty
    cell_parts = {model: {} for model in models_to_use}
    for model in models_to_use:
        for diff in difficulties:
            avg_time = total_time[diff][model] / n_instances[diff]
            avg_gap = total_gap[diff][model] / n_feasible_instances[diff]
            avg_nodes = total_n_nodes[diff][model] / n_instances[diff]
            left = f"{avg_time:.1f}s"
            middle = f"{avg_gap:.1f}%"
            right = f"{avg_nodes:.1f}"
            cell_parts[model][diff] = (left, middle, right)

    # Compute per-column widths (left and right of the pipe)
    lw = {d: 0 for d in difficulties}
    mw = {d: 0 for d in difficulties}
    rw = {d: 0 for d in difficulties}
    for d in difficulties:
        lw[d] = max(len(cell_parts[m][d][0]) for m in models_to_use) if models_to_use else 0
        mw[d] = max(len(cell_parts[m][d][1]) for m in models_to_use) if models_to_use else 0
        rw[d] = max(len(cell_parts[m][d][2]) for m in models_to_use) if models_to_use else 0

    # Header
    col_total = {d: lw[d] + 2 + mw[d] + 2 + rw[d] for d in difficulties}
    print("Average time|gap|nodes by model (over all instances, including unsolved ones)")
    header = f"{'Model':<{model_w}} " + " ".join(name.center(col_total[name]) for name in difficulties)
    sep = "-" * len(header)
    print()
    print(header)
    print(sep)

    # Rows
    for model in models_to_use:
        cells = []
        for d in difficulties:
            left, middle, right = cell_parts[model][d]
            cell = f"{left:>{lw[d]}}|{middle:<{mw[d]}}|{right:<{rw[d]}}"
            cells.append(cell)
        print(f"{model:<{model_w}} " + " ".join(
            f"{cells[i]:<{col_total[difficulties[i]]}}" for i in range(len(difficulties))
        ))
    print()

def generate_stats_report_different_instances(**kwargs):
    """
    Gets model statistics (mean gap and stuff like that). Old way of presenting results, with different instances for each of the methods

    easy:       optimality < time_limit/30
    medium:     optimality < time_limit
    hard:       suboptimal solution at time limit
    impossible: found no solution at time limit
    """

    time_limit = kwargs["time_limit"]
    models_to_use = ["Compact", "DW"] #["Compact", "DW", "DW_PF"]:#, "DW_parallel", "DW_PF_parallel"]:
    n_skipped_easy_instances = 0
    n_skipped_hard_instances = 0

    # for latex pretty print
    stats = {i: {} for i in models_to_use}

    for model in models_to_use:
        prefix = "./Results"
        if kwargs["linear"]:
            prefix += "_linear"

        all_prefixes = [prefix + f"/{name}/" for name in models_to_use]

        prefix += "/" + model + "/"

        result_file = prefix + model + "_results"

        total_opt              = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_subopt           = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_infeasible       = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_timeout          = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_gap              = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_n_nodes          = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_n_cols           = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_n_heuristic_cols = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
        total_time             = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0} 
        total_dual             = {"impossible": 0}

        for complexity in ["low","high"]:
            for n_years in [10,20]:#,30]:
                for machines_per_group in ["20","10_10"]:#,"7_7_6"]:

                    opt              = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    subopt           = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    inf              = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    timeout          = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    gap              = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    n_nodes          = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    n_cols           = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    n_heuristic_cols = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}
                    time             = {"trivial": 0, "easy": 0, "medium":0, "hard": 0, "impossible": 0}   

                    cur_instances = "%s_%ix%sx" % (complexity, n_years, machines_per_group) 
                    directory = prefix + "Statistics/" + cur_instances

                    all_directories = [all_prefixes[i] + "Statistics/" + cur_instances for i in range(len(all_prefixes))]

                    for i in range(50):
                        filename = directory+str(i)

                        all_filenames = [all_directories[index]+str(i)+".stats" for index in range(len(all_prefixes))]
                        skip_instance = True

                        # Skipping instances that are too easy
                        for index in range(len(all_prefixes)):
                            result = scip.readStatistics(all_filenames[index])

                            if result.total_time > 5:
                                skip_instance = False
                                break
                            skip_instance = True

                        if skip_instance:
                            n_skipped_easy_instances += 1
                            continue

                        # Skipping instances that are too hard
                        if not skip_instance:
                            skip_instance = True
                            for index in range(len(all_prefixes)):
                                result = scip.readStatistics(all_filenames[index])

                                if result.n_solutions_found > 0 or result.total_time < time_limit:
                                    skip_instance = False
                                    break

                        if skip_instance:
                            n_skipped_hard_instances += 1
                            continue

                        if kwargs["linear"]:
                            filename += "_linear"
                        filename += ".stats"

                        try:
                            result = scip.readStatistics(filename)
                        except:
                            continue

                        if result.total_time <= time_limit/30:
                            instance_type = "easy"#"trivial"
                        #elif result.total_time <= 60:
                        #    instance_type = "easy"
                        elif result.total_time < time_limit or result.status != "user_interrupt": # the pricer sometimes detects infeasibility at like time_limit + 0.18
                            instance_type = "medium"
                        else:
                            if result.n_solutions_found > 0:
                                instance_type = "hard"
                            else:
                                instance_type = "impossible"
                                if result.dual_bound:
                                    total_dual["impossible"] += result.dual_bound

                        opt[instance_type]     += (result.status == "optimal")
                        inf[instance_type]     += (result.status == "infeasible")
                        timeout[instance_type] += (result.status == "user_interrupt")

                        assert result.status in ["optimal", "infeasible", "user_interrupt"]

                        if result.gap:
                            gap[instance_type]    += result.gap if result.dual_bound > 0 else result.primal_bound
                        
                        if result.n_nodes:
                            n_nodes[instance_type] += result.n_nodes

                        if model != "Compact":
                            n_cols[instance_type] += result.n_presolved_vars

                        time[instance_type]   += result.total_time

                    #for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
                    for instance_type in ["easy", "medium", "hard", "impossible"]:
                        total_opt[instance_type]              += opt[instance_type]
                        total_subopt[instance_type]           += subopt[instance_type]
                        total_infeasible[instance_type]       += inf[instance_type]
                        total_timeout[instance_type]          += timeout[instance_type]
                        total_gap[instance_type]              += gap[instance_type]
                        total_n_nodes[instance_type]          += n_nodes[instance_type]
                        total_n_cols[instance_type]           += n_cols[instance_type]
                        total_n_heuristic_cols[instance_type] += n_heuristic_cols[instance_type]
                        total_time[instance_type]             += time[instance_type]

        with open(result_file, "w+") as file:
            #for instance_type in ["trivial", "easy", "medium", "hard", "impossible"]:
            for instance_type in ["easy", "medium", "hard", "impossible"]:
                file.write(instance_type+"\n")

                file.write("Total optimal: %i\n" % (total_opt[instance_type]))
                file.write("Total suboptimal: %i\n" % (total_subopt[instance_type]))
                file.write("Total timeout: %i\n" % (total_timeout[instance_type]))
                file.write("Total infeasible: %i\n" % total_infeasible[instance_type])
                file.write("Total gap: %.2f%%\n" % total_gap[instance_type])
                file.write("Total nodes: %i\n" % total_n_nodes[instance_type])
                if model != "Compact":
                    file.write("Total n_cols: %i\n" % total_n_cols[instance_type])
                    file.write("Total n_heuristic_cols: %i\n" % total_n_heuristic_cols[instance_type])
                file.write("Total time: %.2f\n" % total_time[instance_type])
                if instance_type == "impossible":
                    file.write("Total dual: %.2f\n" % total_dual["impossible"])
                file.write("\n")
    
                stats[model][instance_type] = {
                    "instances": total_opt[instance_type] + total_subopt[instance_type] + total_infeasible[instance_type] + total_timeout[instance_type],
                    "time/gap":  "%is" % total_time[instance_type] if instance_type in ["easy", "medium"] else "%.0f\\%%" % (total_gap["hard"]) if instance_type == "hard" else "-",
                    "nodes": int(total_n_nodes[instance_type]),
                    "n_cols": total_n_cols[instance_type] if model != "Compact" else "-",
                    "n_heuristic_cols": total_n_heuristic_cols[instance_type] if model != "Compact" else "-"
                }

    print("Skipped %i easy instances and %i hard instances" % (n_skipped_easy_instances/len(models_to_use), n_skipped_hard_instances/len(models_to_use)))
    print_latex_table(stats, models_to_use=models_to_use)

def print_latex_table(stats, models_to_use=None):
    """
    Prints a LaTeX table comparing Compact and DW models.
    Each stats_* argument is a dict with keys: "easy", "medium", "hard", "impossible"/"harder"
    and values: dicts with keys "instances", "time_gap", "nodes".
    """
    # Map keys to LaTeX row names
    row_names = {
        "easy": "easy",
        "medium": "medium",
        "hard": "hard",
        "impossible": "harder"
    }

    # Start LaTeX table
    table = ["\\% Autogenerated by testing.print_method_comparison_table() on {datetime.now().isoformat()}"]
    table.append("\\begin{table}[h]")
    table.append("    \\caption{Performance comparison of the different methods}")
    table.append("    \\label{tbl:MIP5seeds}")
    table.append("    \\scriptsize")
    table.append("    ")
    table.append("    \\begin{tabular*}{\\textwidth}{@{}l@{\\;\\;\\extracolsep{\\fill}}rrrrrrrr@{}}")
    table.append("    \\toprule")
    table.append("    &           \\multicolumn{3}{c}{Compact} & & \\multicolumn{3}{c}{DW}\\\\")
    table.append("    \\cmidrule{2-4} \\cmidrule{5-7}")
    table.append("    Subset         &  instances &   time/gap &   nodes &  instances & time/gap &  nodes\\\\")
    table.append("    \\midrule")

    for key in ["easy", "medium", "hard", "impossible"]:
        c = stats["Compact"].get(key, {})
        d = stats["DW"].get(key, {})
        row = f"    {row_names[key]:<15} & {c.get('instances','-'):>9} & {c.get('time/gap','-'):>8} & {c.get('nodes','-'):>7} & {d.get('instances','-'):>9} & {d.get('time/gap','-'):>8} & {d.get('nodes','-'):>7}\\\\"
        table.append(row)

    table.append("            \\bottomrule")
    table.append("    \\end{tabular*}")
    table.append("\\end{table}")

    print("\n".join(table))
    return

def build_method_comparison_counts(time_limit=300, models_to_use=["Compact", "DW"]):
    """
    Counts per difficulty the feasible/infeasible instances for each model in models_to_use.
    Returns:
      counts[label][model] = {"Feas": int, "Inf": int}
      where label in {"easy","medium","hard","harder"} (harder maps from 'impossible').
    """

    # Get difficulty partition (uses all requested models and time_limit)
    all_instances = _all_instances_for_stats()
    instances_by_difficulty, _ = group_instances_by_difficulty(
        models_to_use=models_to_use,
        all_instances=all_instances,
        time_limit=time_limit,
        skip_infeasible_instances=False
    )

    # difficulty labels: 'impossible' -> 'harder' for display
    label_map = {"easy": "easy", "medium": "medium", "hard": "hard", "impossible": "harder"}
    display_order = ["easy", "medium", "hard", "harder"]

    # Initialize counts container
    counts = {lbl: {m: {"Feas": 0, "Inf": 0} for m in models_to_use} for lbl in display_order}

    def _status(model, instance):
        stats_path = f"./Results/{model}/Statistics/{instance}.stats"
        if not os.path.isfile(stats_path):
            return None
        try:
            res = scip.readStatistics(stats_path)
            return getattr(res, "status", None)
        except Exception:
            return None

    for raw_label, instances in instances_by_difficulty.items():
        if raw_label not in label_map:
            continue
        label = label_map[raw_label]
        for inst in instances:
            for model in models_to_use:
                st = _status(model, inst)
                if st is None:
                    continue
                if st == "infeasible":
                    counts[label][model]["Inf"] += 1
                else:
                    counts[label][model]["Feas"] += 1

    return counts

def print_method_comparison_table(time_limit=300, models_to_use=["Compact", "DW"], write_file=False, out_path="./Media/method_comparison_table.tex"):
    """
    Prints a LaTeX table with counts of feasible/infeasible by model per difficulty bucket,
    and optionally writes it to a file.

    Columns are generated dynamically from models_to_use:
        Interval & (Feas. M1 & Inf. M1) & (Feas. M2 & Inf. M2) & ...
    """
    from datetime import datetime

    counts = build_method_comparison_counts(time_limit=time_limit, models_to_use=models_to_use)
    order = ["easy", "medium", "hard", "harder"]

    # Build dynamic column spec and header
    # One 'l' for Interval + 2 'r' per model (Feas/Inf)
    colspec = "l" + "r" * (2 * len(models_to_use))

    header_cells = ["Interval"]
    for m in models_to_use:
        header_cells += [f"Feas. {m}", f"Inf. {m}"]
    header_line = " & ".join(header_cells) + " \\\\"

    # Build table lines (similar style to print_latex_table)
    table_lines = []
    table_lines.append(f"% Autogenerated by testing.print_method_comparison_table() on {datetime.now().isoformat()}")
    table_lines.append("\\begin{table}[h]")
    table_lines.append("    \\caption{Instance counts by difficulty and method (feasible vs. infeasible)}")
    table_lines.append("    \\label{tbl:method_comparison}")
    table_lines.append("    \\centering")
    table_lines.append("    \\scriptsize")
    table_lines.append(f"    \\begin{tabular}{{{colspec}}}")
    table_lines.append("        \\toprule")
    table_lines.append(f"        {header_line}")
    table_lines.append("        \\midrule")

    for label in order:
        row_cells = [label]
        cur = counts.get(label, {})
        for m in models_to_use:
            val = cur.get(m, {"Feas": 0, "Inf": 0})
            row_cells += [f"{val['Feas']}", f"{val['Inf']}"]
        table_lines.append("        " + " & ".join(row_cells) + " \\\\")

    table_lines.append("        \\bottomrule")
    table_lines.append("    \\end{tabular}")
    table_lines.append("\\end{table}")

    table_str = "\n".join(table_lines)
    print(table_str)

    if write_file:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            f.write(table_str)
        print(f"Wrote LaTeX table to: {out_path}")

    return table_str

if __name__ == "__main__":

    PT = False # different project
    parallel = False

    # To create the instances in the Instance folder.
    n_instances = 50
    set_creation_seed = 1
    for T in [10,20]:
        for complexity in ["low", "high"]:
            for machines_per_group in ["[20]","[10,10]"]:
                kwargs = {
                    "prefix": "PT_" if PT else "",
                    "T": T, 
                    "production_granularity": 1, # leave at 1, have not generalized yet
                    "force_linear": False, 
                    "complexity": complexity, 
                    "machines_per_group": machines_per_group, 
                    "n_instances": n_instances, 
                    "set_seed": set_creation_seed, 
                    "peak_demand": False,
                    "compact_run": False,
                    "plot": False,
                    "PT": PT,
                    "reopt": False,
                    "redirect_output": False,
                    "dual_stabilization": False,
                    "ARMP_use_original_pricing": False,
                    "redcost_fixing": True,
                    "price_and_branch": True,
                    "feasibility": False,
                    "debug_mode": True, # with more convuluted asserts. set to False for performance
                    "stop_at_error": True,
                    "linear_relaxation": False,
                    "discrete_production": 0,
                    "n_workers": os.cpu_count() // 2 if parallel else 1
                }

                create_instance_set(**kwargs)
                set_creation_seed += 1

    # run instance set and generate result files
    time_limit = 300

    # Uncomment to run instance set with either DW (model=0) or Compact (model=1)
    # run_instance_set(model=0, heuristic=1, parallel=False, verbose=3, statistics=True, time_limit = time_limit, **kwargs)
    # run_instance_set(model=1, heuristic=1, parallel=False, verbose=5, statistics=True, time_limit = time_limit, **kwargs)

    # uncomment to get stats from the run
    # generate_stats_report(linear=False, time_limit=time_limit) # groups instances by difficulty and 
    # retrieve_dw_timings()
    
# Known Issues

# Some SCIP bug is making it so multiple identical solutions are reported from the same pricing problem. Not very problematic.

# Sometimes SCIP spends waaay too long on a pricing problem. Likely numerics, or some other bug. See low_10x10_10x0, iteration 38. 80s
# to solve 37 iterations, remainder (220s) for 38. Manually stopping this iter keeps the run going. But instance remains problematic.