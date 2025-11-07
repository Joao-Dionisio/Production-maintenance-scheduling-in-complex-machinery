"""Holds the Component and the Machines classes"""
params = {}
class Component:
    def __init__(self, name, Rmax, C, Q, L, D, n_maintenance_actions: int, maintenance_duration: dict[int,int]):
        """
        name:                  Name as string
        Rmax:                  Maximum Remaining Useful Life in periods
        C:                     Maintenance cost in nr of periods to generate component cost 
        Q:                     Maximum production at perfect condition
        L:                     Influence of production in degradation
        D:                     Influence of time in degradation
        artificial:             If the component is artificial (not an actual component, but added for modeling purposes)
        n_maintenance_actions: Number of different possible maintenance actions (light, heavy, replacement, etc.). Must be integer
        maintenance_duration:  Component duration of maintenance maintenance in nr of periods. Must be a dictionary with integer values.
        """

        self.name = name
        self.Rmax = Rmax
        self.C = C
        self.Q = Q 
        self.L = L
        self.D = D
        self.artificial = False
        self.production_limit = lambda x: 1 # by default, no production limit
        self.n_maintenance_actions = n_maintenance_actions
        self.maintenance_duration = maintenance_duration
        self.maintenance_dependencies = []
        self.degradation_dependencies = []
        self.data = {"degradation_dependencies": {}}

class Machine:
    def __init__(self, id, components):
        """
        id:         Identification number (unsure if string or int)
        components: Machine components
        """
        self.id                  = id
        self.components          = components
        self.data                = {}
        self.Q                   = float("inf") # Machine maximum production at perfect condition
        self.n_production_levels = 1

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''

    # you may need to remove this

    #return round(f,n)
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))

class discretePattern:
    def __init__(self):
        self.c = 0
        self.Mu = {}
        self.x_vals = {}

class continuousPattern:
    def __init__(self):
        self.y_vals = {}

def _get_lambda_expressions(params):
    """
    Prints the source code of a lambda function for debugging purposes.
    """
    from inspect import getsource

    for i in range(params["n_groups"]):
        print("Subproblem %i\n"%i)

        print("Production degradation functions:")
        for k1 in params[i].components.values():
            print("Component: %s"%k1.name)
            print(getsource(k1.production_degradation).strip())

        print("\nProduction limit functions:")
        for k1 in params[i].components.values():
            print("Component: %s"%k1.name)
            print(getsource(k1.production_limit).strip())

        print("\nDegradation dependencies:")
        dependencies = False
        for k1 in params[i].components.values():
            for k2 in k1.degradation_dependencies:
                dependencies = True
                print("%s -> %s"%(k1.name, k2.name))
                src = getsource(k2).strip()
                print(src)
        if not dependencies: print("None")
        
        print()

# from pyscipopt import Model
# m = Model()
# m.readProblem("model.cip")
# m.setParam("limits/gap", 0.01)
# m.optimize()

# sols = m.getSols()
# sols = [s for s in sols if m.isLE(m.getSolObjVal(s) - (-10.355844352883523), -1e-07)]
# pass