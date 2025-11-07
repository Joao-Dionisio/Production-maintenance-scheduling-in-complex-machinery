import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5945211582058174, 'demand': {1: 12.15, 2: 12.3, 3: 12.43, 4: 10.2, 5: 11.62, 6: 12.78, 7: 13.19, 8: 11.06, 9: 12.83, 10: 12.15, 11: 13.09, 12: 10.76, 13: 12.32, 14: 12.8, 15: 11.59, 16: 10.34, 17: 10.65, 18: 10.52, 19: 10.31, 20: 10.51}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x36.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5945211582058174,complexity="low",force_linear=False,params=params)
