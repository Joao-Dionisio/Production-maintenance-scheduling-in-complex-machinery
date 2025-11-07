import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.46901424038333983, 'demand': {1: 11.35, 2: 10.06, 3: 11.77, 4: 12.79, 5: 10.35, 6: 11.49, 7: 10.04, 8: 13.31, 9: 13.23, 10: 12.26, 11: 11.6, 12: 10.23, 13: 10.4, 14: 12.35, 15: 12.65, 16: 13.3, 17: 12.87, 18: 11.46, 19: 10.85, 20: 11.81}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x20.py', 'PT': False}

params[0] = get_random_machine(seed = 0.46901424038333983,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.46901424038334,complexity="low",force_linear=False,params=params)
