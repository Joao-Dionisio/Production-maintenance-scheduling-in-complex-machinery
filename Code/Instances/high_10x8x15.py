import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.9976365270880904, 'demand': {1: 2, 2: 4, 3: 3, 4: 3, 5: 4, 6: 2, 7: 3, 8: 2, 9: 2, 10: 3}, 'machines_per_group': [8], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': False, 'stop_at_error': True, 'force_linear': False, 'filename': 'high_10x8x15.py'}

params[0] = get_random_machine(seed = 0.9976365270880904,complexity="high",force_linear=False,params=params)
