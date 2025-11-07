import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.02708124827630798, 'demand': {1: 11.18, 2: 11.05, 3: 10.67, 4: 12.85, 5: 12.51, 6: 11.28, 7: 11.88, 8: 12.77, 9: 10.2, 10: 12.18, 11: 12.84, 12: 12.02, 13: 11.75, 14: 10.83, 15: 10.56, 16: 10.59, 17: 11.19, 18: 10.95, 19: 12.6, 20: 10.53}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x36.py', 'PT': False}

params[0] = get_random_machine(seed = 0.02708124827630798,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0270812482763079,complexity="low",force_linear=False,params=params)
