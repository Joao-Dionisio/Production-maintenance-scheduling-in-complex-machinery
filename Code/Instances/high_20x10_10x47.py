import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6125322148796885, 'demand': {1: 12.54, 2: 10.3, 3: 10.38, 4: 10.89, 5: 12.22, 6: 10.7, 7: 10.12, 8: 11.4, 9: 10.51, 10: 12.29, 11: 13.16, 12: 12.51, 13: 11.9, 14: 11.36, 15: 10.09, 16: 11.45, 17: 11.74, 18: 11.0, 19: 11.36, 20: 13.14}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x47.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6125322148796885,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.6125322148796886,complexity="high",force_linear=False,params=params)
