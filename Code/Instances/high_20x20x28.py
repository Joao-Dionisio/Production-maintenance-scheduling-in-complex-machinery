import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9267770465471461, 'demand': {1: 10.42, 2: 11.57, 3: 11.15, 4: 10.99, 5: 12.46, 6: 13.25, 7: 10.87, 8: 12.19, 9: 11.0, 10: 11.86, 11: 11.31, 12: 10.56, 13: 10.54, 14: 10.69, 15: 13.02, 16: 11.66, 17: 10.73, 18: 13.02, 19: 13.32, 20: 11.5}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x28.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9267770465471461,complexity="high",force_linear=False,params=params)
