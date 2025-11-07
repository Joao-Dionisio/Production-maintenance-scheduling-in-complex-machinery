import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4409434647088827, 'demand': {1: 11.33, 2: 13.33, 3: 11.84, 4: 12.21, 5: 12.39, 6: 12.15, 7: 12.68, 8: 11.24, 9: 12.22, 10: 13.24, 11: 10.55, 12: 12.08, 13: 11.28, 14: 10.2, 15: 10.13, 16: 12.53, 17: 10.38, 18: 12.37, 19: 10.33, 20: 11.23}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x11.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4409434647088827,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4409434647088828,complexity="low",force_linear=False,params=params)
