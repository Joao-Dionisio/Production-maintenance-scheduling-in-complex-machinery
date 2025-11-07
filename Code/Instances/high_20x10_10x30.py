import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.440275562635577, 'demand': {1: 10.96, 2: 10.25, 3: 11.47, 4: 11.66, 5: 11.12, 6: 12.44, 7: 11.03, 8: 13.27, 9: 13.03, 10: 11.93, 11: 10.34, 12: 11.87, 13: 12.07, 14: 12.17, 15: 11.42, 16: 12.42, 17: 13.32, 18: 12.34, 19: 10.14, 20: 12.09}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x30.py', 'PT': False}

params[0] = get_random_machine(seed = 0.440275562635577,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.440275562635577,complexity="high",force_linear=False,params=params)
