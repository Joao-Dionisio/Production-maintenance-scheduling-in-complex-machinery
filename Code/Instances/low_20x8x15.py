import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3325171998646099, 'demand': {1: 4, 2: 3, 3: 3, 4: 3, 5: 4, 6: 2, 7: 4, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 4, 14: 3, 15: 4, 16: 2, 17: 4, 18: 4, 19: 3, 20: 4}, 'machines_per_group': [8], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': False, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_20x8x15.py'}

params[0] = get_random_machine(seed = 0.3325171998646099,complexity="low",force_linear=False,params=params)
