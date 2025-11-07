import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.53053908944573, 'demand': {1: 12.83, 2: 12.31, 3: 10.43, 4: 12.09, 5: 10.17, 6: 11.12, 7: 11.11, 8: 13.07, 9: 10.74, 10: 11.25, 11: 11.88, 12: 10.68, 13: 11.51, 14: 10.99, 15: 12.41, 16: 12.65, 17: 11.94, 18: 12.89, 19: 11.64, 20: 12.49}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x35.py', 'PT': False}

params[0] = get_random_machine(seed = 0.53053908944573,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.53053908944573,complexity="high",force_linear=False,params=params)
