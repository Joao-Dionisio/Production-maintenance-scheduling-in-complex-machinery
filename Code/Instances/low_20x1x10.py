import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.13436424411240122, 'demand': {1: 0.64, 2: 0.63, 3: 0.54, 4: 0.58, 5: 0.57, 6: 0.61, 7: 0.63, 8: 0.52, 9: 0.5, 10: 0.64, 11: 0.57, 12: 0.63, 13: 0.5, 14: 0.57, 15: 0.62, 16: 0.54, 17: 0.66, 18: 0.65, 19: 0.51, 20: 0.5}, 'machines_per_group': [1], 'n_groups': 1, 'N': [0], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': 1, 'redcost_fixing': 1, 'debug_mode': False, 'stop_at_error': True, 'force_linear': False, 'filename': 'low_20x1x10.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13436424411240122,complexity="low",force_linear=False,params=params)
