import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5077209551440861, 'demand': {1: 10.26, 2: 10.37, 3: 11.46, 4: 11.78, 5: 10.59, 6: 10.88, 7: 10.0, 8: 10.89, 9: 11.03, 10: 11.29, 11: 11.98, 12: 12.84, 13: 12.39, 14: 12.47, 15: 10.94, 16: 11.65, 17: 12.42, 18: 12.98, 19: 10.8, 20: 10.05}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x24.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5077209551440861,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.507720955144086,complexity="low",force_linear=False,params=params)
