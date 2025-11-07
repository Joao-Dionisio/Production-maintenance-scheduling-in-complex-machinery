import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7424596231257796, 'demand': {1: 10.38, 2: 11.12, 3: 10.1, 4: 11.5, 5: 12.55, 6: 12.47, 7: 13.01, 8: 12.52, 9: 12.87, 10: 12.35}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_10x10_10x11.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7424596231257796,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.7424596231257796,complexity="low",force_linear=False,params=params)
