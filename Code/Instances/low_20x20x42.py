import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9941724640838737, 'demand': {1: 10.72, 2: 11.4, 3: 10.9, 4: 11.57, 5: 10.96, 6: 12.22, 7: 10.41, 8: 10.56, 9: 11.53, 10: 10.25, 11: 11.27, 12: 12.99, 13: 12.95, 14: 10.66, 15: 10.06, 16: 12.76, 17: 13.2, 18: 12.0, 19: 10.45, 20: 10.79}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x42.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9941724640838737,complexity="low",force_linear=False,params=params)
