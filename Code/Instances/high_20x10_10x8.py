import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6251121523324751, 'demand': {1: 13.19, 2: 12.61, 3: 10.99, 4: 12.82, 5: 10.65, 6: 11.23, 7: 13.2, 8: 12.82, 9: 11.04, 10: 10.97, 11: 12.04, 12: 12.81, 13: 12.28, 14: 13.12, 15: 12.43, 16: 12.74, 17: 12.02, 18: 11.21, 19: 11.43, 20: 11.63}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x8.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6251121523324751,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.6251121523324752,complexity="high",force_linear=False,params=params)
