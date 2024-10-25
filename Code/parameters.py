"""Holds the Component and the Machines classes"""
params = {}

class Component:
    def __init__(self, name, Rmax, C, Q, L, D, maintenance_duration: int):
        """
        name:                  Name as string
        Rmax:                  Maximum Remaining Useful Life in periods
        C:                     Maintenance cost in nr of periods to generate component cost 
        Q:                     Maximum production at perfect condition
        L:                     Influence of production in degradation
        D:                     Influence of time in degradation
        maintenance_duration:  Component duration of maintenance in nr of periods (must be an integer)
        """

        self.name = name
        self.Rmax = Rmax
        self.C = C
        self.Q = Q 
        self.L = L
        self.D = D
        self.maintenance_duration = maintenance_duration
        self.maintenance_dependencies = [] 
        self.degradation_dependencies = []

class Machine:
    def __init__(self, id, components):
        """
        id:         Identification number (unsure if string or int)
        components: Machine components
        """
        self.id = id
        self.components = components