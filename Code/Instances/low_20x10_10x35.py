import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3887021252841323, 'demand': {1: 11.17, 2: 10.46, 3: 10.97, 4: 13.3, 5: 13.06, 6: 10.9, 7: 12.6, 8: 10.43, 9: 12.11, 10: 10.29, 11: 12.14, 12: 11.99, 13: 13.31, 14: 11.93, 15: 13.04, 16: 10.81, 17: 12.08, 18: 10.7, 19: 10.23, 20: 13.28}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x35.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3887021252841323,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3887021252841323,complexity="low",force_linear=False,params=params)
