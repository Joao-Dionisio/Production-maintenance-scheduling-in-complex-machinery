import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.667291200036621, 'demand': {1: 12.3, 2: 11.71, 3: 11.69, 4: 11.34, 5: 11.5, 6: 11.58, 7: 12.68, 8: 10.53, 9: 10.39, 10: 13.08, 11: 11.7, 12: 12.32, 13: 13.05, 14: 12.45, 15: 11.89, 16: 13.17, 17: 12.08, 18: 11.49, 19: 10.61, 20: 10.53}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x25.py', 'PT': False}

params[0] = get_random_machine(seed = 0.667291200036621,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.6672912000366211,complexity="high",force_linear=False,params=params)
