import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.47610254247229544, 'demand': {1: 12.34, 2: 11.33, 3: 13.27, 4: 12.72, 5: 13.08, 6: 12.31, 7: 12.23, 8: 11.79, 9: 12.66, 10: 11.21, 11: 11.98, 12: 12.26, 13: 11.74, 14: 10.95, 15: 10.26, 16: 10.29, 17: 11.19, 18: 11.93, 19: 12.53, 20: 12.38}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x32.py', 'PT': False}

params[0] = get_random_machine(seed = 0.47610254247229544,complexity="low",force_linear=False,params=params)
