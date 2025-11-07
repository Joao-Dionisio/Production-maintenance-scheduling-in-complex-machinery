import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8031769708141783, 'demand': {1: 10.02, 2: 10.15, 3: 10.1, 4: 12.15, 5: 11.87, 6: 11.61, 7: 13.12, 8: 11.57, 9: 10.69, 10: 13.32, 11: 10.37, 12: 10.17, 13: 10.74, 14: 13.26, 15: 11.39, 16: 11.19, 17: 11.23, 18: 11.23, 19: 12.52, 20: 12.13}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x30.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8031769708141783,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8031769708141783,complexity="low",force_linear=False,params=params)
