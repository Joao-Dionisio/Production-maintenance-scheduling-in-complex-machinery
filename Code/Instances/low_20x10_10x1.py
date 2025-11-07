import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6856898821004409, 'demand': {1: 12.81, 2: 11.12, 3: 10.31, 4: 12.67, 5: 12.68, 6: 11.48, 7: 10.31, 8: 10.66, 9: 12.12, 10: 10.97, 11: 13.17, 12: 11.96, 13: 10.67, 14: 12.18, 15: 11.2, 16: 13.11, 17: 13.03, 18: 11.72, 19: 12.15, 20: 12.33}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x1.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6856898821004409,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.685689882100441,complexity="low",force_linear=False,params=params)
