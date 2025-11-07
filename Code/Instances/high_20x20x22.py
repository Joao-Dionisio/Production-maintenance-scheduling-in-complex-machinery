import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6828953695005007, 'demand': {1: 12.31, 2: 10.77, 3: 10.1, 4: 10.44, 5: 11.2, 6: 10.35, 7: 12.79, 8: 11.86, 9: 12.09, 10: 12.09, 11: 12.27, 12: 11.63, 13: 10.01, 14: 12.66, 15: 12.49, 16: 11.68, 17: 11.78, 18: 12.2, 19: 10.22, 20: 12.46}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x22.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6828953695005007,complexity="high",force_linear=False,params=params)
