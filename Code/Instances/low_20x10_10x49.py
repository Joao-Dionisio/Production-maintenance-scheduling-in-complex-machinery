import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.859675715314122, 'demand': {1: 12.83, 2: 10.71, 3: 10.14, 4: 11.83, 5: 10.27, 6: 11.74, 7: 10.4, 8: 10.41, 9: 12.93, 10: 12.07, 11: 10.21, 12: 11.79, 13: 10.97, 14: 11.5, 15: 12.52, 16: 12.98, 17: 10.09, 18: 10.04, 19: 13.06, 20: 10.46}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x49.py', 'PT': False}

params[0] = get_random_machine(seed = 0.859675715314122,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.859675715314122,complexity="low",force_linear=False,params=params)
