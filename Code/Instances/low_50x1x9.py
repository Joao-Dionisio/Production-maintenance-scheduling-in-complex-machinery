import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1, 11: 0.1, 12: 0.1, 13: 0.1, 14: 0.1, 15: 0.1, 16: 0.1, 17: 0.1, 18: 0.1, 19: 0.1, 20: 0.1, 21: 0.1, 22: 0.1, 23: 0.1, 24: 0.1, 25: 0.1, 26: 0.1, 27: 0.1, 28: 0.1, 29: 0.1, 30: 0.1, 31: 0.1, 32: 0.1, 33: 0.1, 34: 0.1, 35: 0.1, 36: 0.1, 37: 0.1, 38: 0.1, 39: 0.1, 40: 0.1, 41: 0.1, 42: 0.1, 43: 0.1, 44: 0.1, 45: 0.1, 46: 0.1, 47: 0.1, 48: 0.1, 49: 0.1, 50: 0.1}, 'machines_per_group': [1], 'n_groups': 1, 'N': [0], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_50x1x9.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
