import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.48199429143262484, 'demand': {1: 12.94, 2: 11.31, 3: 10.72, 4: 10.92, 5: 10.67, 6: 11.87, 7: 11.19, 8: 12.5, 9: 10.81, 10: 11.17, 11: 10.83, 12: 13.27, 13: 12.8, 14: 12.83, 15: 12.06, 16: 11.34, 17: 10.48, 18: 12.77, 19: 11.63, 20: 10.13}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x30.py', 'PT': False}

params[0] = get_random_machine(seed = 0.48199429143262484,complexity="low",force_linear=False,params=params)
