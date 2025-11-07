import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.38362465950249336, 'demand': {1: 11.82, 2: 12.36, 3: 10.58, 4: 10.49, 5: 12.74, 6: 10.29, 7: 12.64, 8: 12.53, 9: 10.73, 10: 12.12, 11: 10.84, 12: 12.94, 13: 10.66, 14: 10.39, 15: 10.12, 16: 12.4, 17: 10.71, 18: 11.05, 19: 13.26, 20: 12.45}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x18.py', 'PT': False}

params[0] = get_random_machine(seed = 0.38362465950249336,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3836246595024932,complexity="high",force_linear=False,params=params)
