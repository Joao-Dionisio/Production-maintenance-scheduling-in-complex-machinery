import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9583005037279291, 'demand': {1: 12.73, 2: 11.4, 3: 12.71, 4: 12.14, 5: 11.23, 6: 10.47, 7: 11.99, 8: 11.88, 9: 13.19, 10: 13.23, 11: 12.03, 12: 11.17, 13: 12.98, 14: 10.0, 15: 10.36, 16: 11.89, 17: 12.05, 18: 10.47, 19: 12.1, 20: 12.97}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x11.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9583005037279291,complexity="low",force_linear=False,params=params)
