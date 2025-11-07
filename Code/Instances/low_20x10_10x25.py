import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.050880802982543494, 'demand': {1: 11.72, 2: 12.91, 3: 10.51, 4: 12.61, 5: 12.14, 6: 12.88, 7: 13.0, 8: 10.36, 9: 12.65, 10: 10.45, 11: 10.4, 12: 11.33, 13: 11.63, 14: 10.23, 15: 10.92, 16: 10.58, 17: 10.45, 18: 10.33, 19: 10.08, 20: 10.73}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x25.py', 'PT': False}

params[0] = get_random_machine(seed = 0.050880802982543494,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0508808029825434,complexity="low",force_linear=False,params=params)
