import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8304951904066603, 'demand': {1: 12.06, 2: 12.91, 3: 12.77, 4: 11.19, 5: 12.92, 6: 12.07, 7: 10.07, 8: 11.11, 9: 12.28, 10: 12.33, 11: 12.34, 12: 12.58, 13: 12.42, 14: 13.02, 15: 10.86, 16: 13.02, 17: 12.96, 18: 12.7, 19: 10.76, 20: 12.01}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x48.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8304951904066603,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8304951904066602,complexity="low",force_linear=False,params=params)
