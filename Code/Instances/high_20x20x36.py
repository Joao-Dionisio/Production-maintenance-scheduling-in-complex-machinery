import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.049257335851017214, 'demand': {1: 11.58, 2: 11.24, 3: 13.07, 4: 10.64, 5: 11.21, 6: 12.99, 7: 10.1, 8: 11.37, 9: 12.71, 10: 12.56, 11: 10.14, 12: 10.12, 13: 10.21, 14: 13.07, 15: 10.86, 16: 12.49, 17: 13.0, 18: 11.13, 19: 10.91, 20: 13.19}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x36.py', 'PT': False}

params[0] = get_random_machine(seed = 0.049257335851017214,complexity="high",force_linear=False,params=params)
