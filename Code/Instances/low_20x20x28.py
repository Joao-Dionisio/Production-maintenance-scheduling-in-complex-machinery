import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7637877519351215, 'demand': {1: 11.86, 2: 10.09, 3: 10.17, 4: 10.43, 5: 11.19, 6: 12.87, 7: 13.16, 8: 12.04, 9: 10.77, 10: 11.43, 11: 11.21, 12: 11.1, 13: 10.04, 14: 11.95, 15: 12.76, 16: 12.42, 17: 10.32, 18: 11.77, 19: 10.57, 20: 12.36}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x28.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7637877519351215,complexity="low",force_linear=False,params=params)
