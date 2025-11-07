import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2613157320387096, 'demand': {1: 11.61, 2: 10.2, 3: 12.08, 4: 12.86, 5: 13.04, 6: 11.2, 7: 10.56, 8: 12.44, 9: 12.52, 10: 10.63, 11: 10.2, 12: 12.23, 13: 11.27, 14: 11.74, 15: 11.88, 16: 12.95, 17: 10.42, 18: 10.87, 19: 10.11, 20: 12.3}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x37.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2613157320387096,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2613157320387096,complexity="high",force_linear=False,params=params)
