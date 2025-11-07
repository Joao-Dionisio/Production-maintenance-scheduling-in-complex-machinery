import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9447489551908349, 'demand': {1: 11.16, 2: 12.33, 3: 12.07, 4: 10.48, 5: 12.29, 6: 10.27, 7: 10.62, 8: 11.93, 9: 10.42, 10: 13.21, 11: 11.42, 12: 12.1, 13: 13.22, 14: 10.36, 15: 13.33, 16: 10.13, 17: 12.0, 18: 12.19, 19: 13.29, 20: 11.19}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x15.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9447489551908349,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.944748955190835,complexity="high",force_linear=False,params=params)
