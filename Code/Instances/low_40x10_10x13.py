import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 12.82, 2: 12.55, 3: 10.85, 4: 11.65, 5: 11.5, 6: 12.17, 7: 12.63, 8: 10.31, 9: 10.09, 10: 12.79, 11: 11.44, 12: 12.54, 13: 10.01, 14: 11.48, 15: 12.41, 16: 10.76, 17: 13.15, 18: 13.0, 19: 10.1, 20: 10.08, 21: 11.8, 22: 13.13, 23: 11.27, 24: 10.72, 25: 11.41, 26: 10.1, 27: 10.74, 28: 11.46, 29: 11.65, 30: 10.78, 31: 10.77, 32: 10.73, 33: 11.53, 34: 10.97, 35: 10.07, 36: 12.79, 37: 11.85, 38: 12.14, 39: 10.62, 40: 13.31}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_40x10_10x13.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.134364244112401,complexity="low",force_linear=False,params=params)
