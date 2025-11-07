import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5278435799770181, 'demand': {1: 12.08, 2: 12.68, 3: 10.98, 4: 10.47, 5: 12.96, 6: 12.0, 7: 10.09, 8: 12.32, 9: 12.4, 10: 12.54, 11: 10.44, 12: 10.91, 13: 12.41, 14: 12.23, 15: 11.15, 16: 13.23, 17: 11.01, 18: 12.97, 19: 10.45, 20: 11.52}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x33.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5278435799770181,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.5278435799770183,complexity="high",force_linear=False,params=params)
