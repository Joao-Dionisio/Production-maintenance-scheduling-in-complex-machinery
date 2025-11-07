import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 5.13, 2: 5.02, 3: 4.34, 4: 4.66, 5: 4.6, 6: 4.87, 7: 5.05, 8: 4.13, 9: 4.04, 10: 5.11, 11: 4.58, 12: 5.02}, 'machines_per_group': [3, 5], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': False, 'force_linear': False, 'filename': 'high_12x3_5x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.134364244112401,complexity="high",force_linear=False,params=params)
