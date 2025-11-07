import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.028013403418403082, 'demand': {1: 13.07, 2: 13.16, 3: 11.45, 4: 12.77, 5: 10.17, 6: 10.46, 7: 10.03, 8: 10.23, 9: 10.01, 10: 12.76, 11: 10.29, 12: 11.97, 13: 10.91, 14: 10.44, 15: 11.4, 16: 10.61, 17: 13.26, 18: 11.28, 19: 11.98, 20: 11.88}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x14.py', 'PT': False}

params[0] = get_random_machine(seed = 0.028013403418403082,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0280134034184032,complexity="low",force_linear=False,params=params)
