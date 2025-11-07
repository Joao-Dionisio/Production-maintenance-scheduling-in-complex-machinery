import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.608959074609656, 'demand': {1: 10.9, 2: 12.13, 3: 13.24, 4: 11.61, 5: 12.15, 6: 12.79, 7: 10.84, 8: 10.89, 9: 13.23, 10: 11.0, 11: 11.42, 12: 11.24, 13: 13.31, 14: 11.82, 15: 12.99, 16: 10.54, 17: 10.93, 18: 12.17, 19: 11.06, 20: 12.21}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x23.py', 'PT': False}

params[0] = get_random_machine(seed = 0.608959074609656,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.608959074609656,complexity="low",force_linear=False,params=params)
