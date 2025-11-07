import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2931030991671718, 'demand': {1: 12.61, 2: 12.76, 3: 10.04, 4: 11.78, 5: 10.91, 6: 13.12, 7: 12.61, 8: 10.82, 9: 10.89, 10: 10.52, 11: 13.3, 12: 10.98, 13: 12.03, 14: 11.58, 15: 12.15, 16: 12.01, 17: 12.48, 18: 10.39, 19: 12.53, 20: 11.0}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x13.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2931030991671718,complexity="low",force_linear=False,params=params)
