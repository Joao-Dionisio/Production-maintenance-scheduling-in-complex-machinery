import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.0012056217722533624, 'demand': {1: 12.96, 2: 13.28, 3: 11.22, 4: 12.66, 5: 11.68, 6: 11.87, 7: 12.86, 8: 13.14, 9: 11.0, 10: 10.73, 11: 13.05, 12: 11.97, 13: 13.01, 14: 10.74, 15: 12.83, 16: 10.53, 17: 10.49, 18: 10.96, 19: 13.09, 20: 11.29}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x29.py', 'PT': False}

params[0] = get_random_machine(seed = 0.0012056217722533624,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0012056217722534,complexity="high",force_linear=False,params=params)
