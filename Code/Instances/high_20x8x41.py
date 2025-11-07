import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.15771538452006084, 'demand': {1: 2, 2: 4, 3: 3, 4: 3, 5: 2, 6: 2, 7: 4, 8: 4, 9: 3, 10: 4, 11: 2, 12: 4, 13: 2, 14: 2, 15: 3, 16: 3, 17: 3, 18: 2, 19: 3, 20: 2}, 'machines_per_group': [8], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': False, 'stop_at_error': True, 'force_linear': False, 'filename': 'high_20x8x41.py'}

params[0] = get_random_machine(seed = 0.15771538452006084,complexity="high",force_linear=False,params=params)
