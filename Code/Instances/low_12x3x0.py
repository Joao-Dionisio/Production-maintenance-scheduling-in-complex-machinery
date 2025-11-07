import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 1.92, 2: 1.88, 3: 1.63, 4: 1.75, 5: 1.72, 6: 1.83, 7: 1.89, 8: 1.55, 9: 1.51, 10: 1.92, 11: 1.72, 12: 1.88}, 'machines_per_group': [3], 'n_groups': 1, 'N': [0, 1, 2], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_12x3x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
