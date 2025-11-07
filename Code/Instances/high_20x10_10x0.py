import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2267058593810488, 'demand': {1: 13.21, 2: 10.42, 3: 12.35, 4: 10.28, 5: 10.82, 6: 13.33, 7: 10.7, 8: 12.14, 9: 11.53, 10: 11.51, 11: 11.65, 12: 10.64, 13: 12.77, 14: 10.3, 15: 10.78, 16: 10.07, 17: 10.89, 18: 11.36, 19: 13.01, 20: 11.26}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2267058593810488,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.226705859381049,complexity="high",force_linear=False,params=params)
