import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.12616666089455564, 'demand': {1: 12.66, 2: 11.51, 3: 10.38, 4: 12.72, 5: 10.13, 6: 11.24, 7: 11.35, 8: 11.73, 9: 10.8, 10: 13.09, 11: 11.94, 12: 11.09, 13: 12.13, 14: 11.27, 15: 11.87, 16: 11.99, 17: 10.82, 18: 12.9, 19: 10.31, 20: 13.11}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x37.py', 'PT': False}

params[0] = get_random_machine(seed = 0.12616666089455564,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.1261666608945555,complexity="low",force_linear=False,params=params)
