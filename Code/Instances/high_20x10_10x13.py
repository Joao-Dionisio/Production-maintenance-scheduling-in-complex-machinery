import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9360518908722214, 'demand': {1: 13.32, 2: 13.1, 3: 10.44, 4: 11.09, 5: 11.36, 6: 10.56, 7: 12.54, 8: 10.2, 9: 12.96, 10: 11.95, 11: 12.05, 12: 11.38, 13: 13.12, 14: 11.93, 15: 12.99, 16: 13.08, 17: 12.31, 18: 13.28, 19: 11.63, 20: 11.22}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x13.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9360518908722214,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.9360518908722213,complexity="high",force_linear=False,params=params)
