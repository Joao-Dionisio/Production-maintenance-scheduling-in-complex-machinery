import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.13800502163322748, 'demand': {1: 11.17, 2: 11.65, 3: 11.89, 4: 10.69, 5: 11.51, 6: 10.2, 7: 10.29, 8: 11.14, 9: 10.48, 10: 13.23, 11: 10.88, 12: 10.92, 13: 12.61, 14: 12.47, 15: 10.87, 16: 12.76, 17: 12.09, 18: 11.3, 19: 12.1, 20: 10.82}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x46.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13800502163322748,complexity="low",force_linear=False,params=params)
