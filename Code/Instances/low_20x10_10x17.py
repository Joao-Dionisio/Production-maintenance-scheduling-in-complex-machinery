import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8369646083380187, 'demand': {1: 11.73, 2: 13.18, 3: 11.73, 4: 12.59, 5: 11.63, 6: 11.21, 7: 13.31, 8: 12.81, 9: 11.97, 10: 12.89, 11: 12.16, 12: 12.66, 13: 10.22, 14: 10.44, 15: 10.36, 16: 12.01, 17: 12.4, 18: 10.52, 19: 11.68, 20: 10.38}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x17.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8369646083380187,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8369646083380187,complexity="low",force_linear=False,params=params)
