import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.24388628384399558, 'demand': {1: 10.04, 2: 11.14, 3: 10.89, 4: 11.41, 5: 11.26, 6: 12.78, 7: 12.97, 8: 10.58, 9: 11.32, 10: 10.55, 11: 12.21, 12: 13.25, 13: 10.67, 14: 12.55, 15: 11.0, 16: 10.04, 17: 12.55, 18: 11.14, 19: 10.57, 20: 11.45}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x3.py', 'PT': False}

params[0] = get_random_machine(seed = 0.24388628384399558,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2438862838439957,complexity="high",force_linear=False,params=params)
