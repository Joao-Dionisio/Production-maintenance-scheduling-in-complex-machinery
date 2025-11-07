import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4068789276781928, 'demand': {1: 11.32, 2: 11.92, 3: 10.4, 4: 12.15, 5: 13.01, 6: 11.21, 7: 11.66, 8: 10.84, 9: 13.03, 10: 11.26, 11: 11.2, 12: 12.38, 13: 11.24, 14: 13.02, 15: 11.37, 16: 11.96, 17: 11.02, 18: 11.96, 19: 11.57, 20: 10.35}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x27.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4068789276781928,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4068789276781928,complexity="low",force_linear=False,params=params)
