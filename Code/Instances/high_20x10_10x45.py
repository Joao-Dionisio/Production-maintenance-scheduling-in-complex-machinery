import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9047981456899298, 'demand': {1: 11.09, 2: 11.39, 3: 10.14, 4: 10.02, 5: 11.92, 6: 12.95, 7: 12.12, 8: 10.43, 9: 12.21, 10: 10.43, 11: 11.57, 12: 12.5, 13: 11.29, 14: 11.06, 15: 11.07, 16: 10.97, 17: 10.05, 18: 12.42, 19: 11.31, 20: 10.62}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x45.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9047981456899298,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.90479814568993,complexity="high",force_linear=False,params=params)
