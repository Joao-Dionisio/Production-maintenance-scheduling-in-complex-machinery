import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8993493571009838, 'demand': {1: 10.51, 2: 13.06, 3: 12.9, 4: 12.85, 5: 11.13, 6: 10.84, 7: 10.44, 8: 11.24, 9: 12.85, 10: 11.21, 11: 10.02, 12: 11.02, 13: 10.28, 14: 12.08, 15: 12.56, 16: 13.09, 17: 10.3, 18: 11.27, 19: 10.42, 20: 13.03}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x16.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8993493571009838,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8993493571009838,complexity="low",force_linear=False,params=params)
