import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8832278144381652, 'demand': {1: 2, 2: 2, 3: 2, 4: 3, 5: 2, 6: 2, 7: 4, 8: 3, 9: 4, 10: 2, 11: 2, 12: 3, 13: 3, 14: 4, 15: 4, 16: 4, 17: 4, 18: 2, 19: 4, 20: 3}, 'machines_per_group': [8], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': False, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_20x8x19.py'}

params[0] = get_random_machine(seed = 0.8832278144381652,complexity="low",force_linear=False,params=params)
