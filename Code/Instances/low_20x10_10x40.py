import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.048114696265958434, 'demand': {1: 10.99, 2: 11.89, 3: 10.91, 4: 11.79, 5: 10.35, 6: 10.86, 7: 12.11, 8: 11.1, 9: 13.26, 10: 11.22, 11: 11.02, 12: 11.34, 13: 12.13, 14: 11.05, 15: 13.26, 16: 10.67, 17: 11.95, 18: 12.91, 19: 10.9, 20: 10.78}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x40.py', 'PT': False}

params[0] = get_random_machine(seed = 0.048114696265958434,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0481146962659584,complexity="low",force_linear=False,params=params)
