import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.07909418169403881, 'demand': {1: 12.84, 2: 12.03, 3: 11.71, 4: 10.89, 5: 12.9, 6: 10.38, 7: 11.94, 8: 12.77, 9: 12.19, 10: 10.16, 11: 10.37, 12: 10.95, 13: 12.44, 14: 10.46, 15: 13.19, 16: 12.95, 17: 11.91, 18: 12.92, 19: 12.12, 20: 10.53}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x38.py', 'PT': False}

params[0] = get_random_machine(seed = 0.07909418169403881,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.079094181694039,complexity="high",force_linear=False,params=params)
