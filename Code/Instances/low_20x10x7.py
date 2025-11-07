import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 5, 2: 3, 3: 3, 4: 5, 5: 5, 6: 4, 7: 5, 8: 4, 9: 3, 10: 4, 11: 4, 12: 5, 13: 3, 14: 3, 15: 3, 16: 5, 17: 5, 18: 3, 19: 3, 20: 3}, 'machines_per_group': [10], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_20x10x7.py'}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
