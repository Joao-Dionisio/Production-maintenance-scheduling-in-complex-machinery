import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.33911614433881987, 'demand': {1: 10.65, 2: 11.06, 3: 12.41, 4: 10.06, 5: 11.85, 6: 11.47, 7: 10.06, 8: 11.1, 9: 12.08, 10: 11.71, 11: 10.21, 12: 13.28, 13: 12.63, 14: 13.24, 15: 10.35, 16: 10.89, 17: 10.13, 18: 12.6, 19: 10.9, 20: 10.43}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x15.py', 'PT': False}

params[0] = get_random_machine(seed = 0.33911614433881987,complexity="high",force_linear=False,params=params)
