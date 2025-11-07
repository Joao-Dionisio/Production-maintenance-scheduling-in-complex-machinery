import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 5, 2: 7, 3: 5, 4: 8, 5: 8, 6: 8, 7: 8}, 'machines_per_group': [8, 5, 4], 'n_groups': 3, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 'T': [1, 2, 3, 4, 5, 6, 7], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': True, 'stop_at_error': False, 'force_linear': False, 'filename': 'low_7x8_5_4x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.134364244112401,complexity="low",force_linear=False,params=params)

params[2] = get_random_machine(seed = 2.134364244112401,complexity="low",force_linear=False,params=params)
