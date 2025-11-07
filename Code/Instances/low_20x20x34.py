import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.39016692621990856, 'demand': {1: 10.59, 2: 12.18, 3: 13.0, 4: 13.03, 5: 12.05, 6: 11.29, 7: 10.36, 8: 12.3, 9: 11.84, 10: 12.38, 11: 11.25, 12: 12.96, 13: 10.71, 14: 11.02, 15: 10.89, 16: 12.07, 17: 12.99, 18: 10.56, 19: 12.11, 20: 12.55}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x34.py', 'PT': False}

params[0] = get_random_machine(seed = 0.39016692621990856,complexity="low",force_linear=False,params=params)
