import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8120898464292818, 'demand': {1: 11.53, 2: 11.43, 3: 11.1, 4: 13.06, 5: 10.81, 6: 11.38, 7: 10.87, 8: 10.41, 9: 10.07, 10: 12.27, 11: 12.71, 12: 11.06, 13: 11.47, 14: 12.72, 15: 10.18, 16: 10.91, 17: 12.45, 18: 10.83, 19: 10.83, 20: 11.77}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x44.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8120898464292818,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8120898464292818,complexity="low",force_linear=False,params=params)
