import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8025683233965653, 'demand': {1: 12.46, 2: 12.74, 3: 12.58, 4: 12.02, 5: 11.09, 6: 11.07, 7: 11.21, 8: 12.61, 9: 10.26, 10: 10.66, 11: 12.51, 12: 10.82, 13: 10.22, 14: 10.11, 15: 11.84, 16: 11.09, 17: 13.27, 18: 12.94, 19: 13.29, 20: 10.88}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x38.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8025683233965653,complexity="high",force_linear=False,params=params)
