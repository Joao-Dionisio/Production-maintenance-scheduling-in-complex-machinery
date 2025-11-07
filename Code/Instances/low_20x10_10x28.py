import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8889542711979218, 'demand': {1: 10.53, 2: 11.92, 3: 12.26, 4: 11.56, 5: 11.09, 6: 11.51, 7: 13.33, 8: 10.04, 9: 12.95, 10: 12.02, 11: 11.6, 12: 12.13, 13: 12.13, 14: 12.77, 15: 13.26, 16: 11.72, 17: 11.17, 18: 11.21, 19: 13.04, 20: 11.6}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x28.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8889542711979218,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.888954271197922,complexity="low",force_linear=False,params=params)
