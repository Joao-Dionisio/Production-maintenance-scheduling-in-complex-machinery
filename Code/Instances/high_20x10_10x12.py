import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.15973781166288403, 'demand': {1: 10.85, 2: 11.3, 3: 11.44, 4: 12.61, 5: 10.33, 6: 10.74, 7: 10.98, 8: 10.59, 9: 12.5, 10: 10.36, 11: 10.17, 12: 11.85, 13: 12.45, 14: 12.75, 15: 11.86, 16: 11.09, 17: 12.94, 18: 12.45, 19: 11.6, 20: 11.88}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x12.py', 'PT': False}

params[0] = get_random_machine(seed = 0.15973781166288403,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.159737811662884,complexity="high",force_linear=False,params=params)
