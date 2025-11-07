import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3067925048517076, 'demand': {1: 13.1, 2: 10.92, 3: 12.39, 4: 10.24, 5: 12.51, 6: 12.23, 7: 13.19, 8: 12.99, 9: 12.29, 10: 12.79, 11: 12.46, 12: 12.04, 13: 10.7, 14: 11.72, 15: 12.99, 16: 10.8, 17: 13.25, 18: 11.81, 19: 11.31, 20: 10.01}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x33.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3067925048517076,complexity="low",force_linear=False,params=params)
