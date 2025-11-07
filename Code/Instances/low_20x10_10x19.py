import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7339842628286017, 'demand': {1: 13.24, 2: 12.09, 3: 13.04, 4: 10.91, 5: 10.01, 6: 12.94, 7: 10.1, 8: 13.31, 9: 11.52, 10: 10.2, 11: 10.92, 12: 12.4, 13: 11.28, 14: 12.08, 15: 10.34, 16: 12.79, 17: 11.24, 18: 12.78, 19: 10.49, 20: 12.22}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x19.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7339842628286017,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.7339842628286017,complexity="low",force_linear=False,params=params)
