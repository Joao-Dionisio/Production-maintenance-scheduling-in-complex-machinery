import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3478845080276999, 'demand': {1: 12.15, 2: 12.46, 3: 12.76, 4: 11.17, 5: 12.81, 6: 12.9, 7: 12.29, 8: 13.25, 9: 13.19, 10: 11.73, 11: 11.76, 12: 10.55, 13: 12.79, 14: 13.12, 15: 11.59, 16: 12.3, 17: 12.4, 18: 12.43, 19: 10.57, 20: 12.6}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x8.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3478845080276999,complexity="low",force_linear=False,params=params)
