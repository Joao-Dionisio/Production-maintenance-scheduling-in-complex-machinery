import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5689049033013557, 'demand': {1: 11.61, 2: 11.1, 3: 12.23, 4: 11.47, 5: 12.56, 6: 12.57, 7: 10.03, 8: 11.09, 9: 11.81, 10: 10.99, 11: 12.0, 12: 10.1, 13: 10.35, 14: 11.71, 15: 10.72, 16: 10.69, 17: 11.38, 18: 11.98, 19: 12.18, 20: 12.0}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x32.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5689049033013557,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.5689049033013558,complexity="low",force_linear=False,params=params)
