import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 1.28, 2: 1.25, 3: 1.09, 4: 1.17, 5: 1.15, 6: 1.22, 7: 1.26, 8: 1.03, 9: 1.01, 10: 1.28}, 'machines_per_group': [2], 'n_groups': 1, 'N': [0, 1], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_10x2x3.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
