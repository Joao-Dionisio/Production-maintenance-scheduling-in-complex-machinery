import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8132730633834768, 'demand': {1: 11.99, 2: 12.77, 3: 11.23, 4: 12.6, 5: 12.64, 6: 11.29, 7: 12.18, 8: 12.6, 9: 13.31, 10: 13.07, 11: 12.62, 12: 10.46, 13: 12.03, 14: 12.28, 15: 10.29, 16: 11.54, 17: 12.9, 18: 13.02, 19: 13.08, 20: 10.31}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x10.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8132730633834768,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8132730633834768,complexity="high",force_linear=False,params=params)
