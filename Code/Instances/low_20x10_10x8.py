import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.13707201047427242, 'demand': {1: 13.14, 2: 13.03, 3: 11.47, 4: 12.59, 5: 11.49, 6: 10.92, 7: 12.37, 8: 10.21, 9: 12.67, 10: 13.26, 11: 10.95, 12: 13.13, 13: 10.28, 14: 12.86, 15: 10.93, 16: 13.22, 17: 11.44, 18: 13.07, 19: 10.11, 20: 10.29}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x8.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13707201047427242,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.1370720104742724,complexity="low",force_linear=False,params=params)
