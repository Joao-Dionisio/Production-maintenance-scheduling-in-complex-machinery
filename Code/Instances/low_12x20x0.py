import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 12.82, 2: 12.55, 3: 10.85, 4: 11.65, 5: 11.5, 6: 12.17, 7: 12.63, 8: 10.31, 9: 10.09, 10: 12.79, 11: 11.44, 12: 12.54}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_12x20x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
