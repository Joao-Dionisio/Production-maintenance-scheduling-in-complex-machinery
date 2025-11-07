import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.28702645939357063, 'demand': {1: 11.48, 2: 10.67, 3: 12.86, 4: 12.6, 5: 12.63, 6: 10.71, 7: 11.97, 8: 10.85, 9: 12.64, 10: 12.48, 11: 13.32, 12: 12.36, 13: 12.28, 14: 12.59, 15: 10.31, 16: 11.98, 17: 10.11, 18: 11.22, 19: 10.39, 20: 13.16}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x13.py', 'PT': False}

params[0] = get_random_machine(seed = 0.28702645939357063,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2870264593935707,complexity="low",force_linear=False,params=params)
