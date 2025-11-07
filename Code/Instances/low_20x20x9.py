import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.580845300230795, 'demand': {1: 12.22, 2: 11.4, 3: 12.08, 4: 12.58, 5: 12.12, 6: 12.4, 7: 10.09, 8: 10.53, 9: 11.47, 10: 12.17, 11: 10.73, 12: 12.29, 13: 12.1, 14: 10.14, 15: 11.57, 16: 10.75, 17: 10.18, 18: 10.45, 19: 11.06, 20: 10.61}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x9.py', 'PT': False}

params[0] = get_random_machine(seed = 0.580845300230795,complexity="low",force_linear=False,params=params)
