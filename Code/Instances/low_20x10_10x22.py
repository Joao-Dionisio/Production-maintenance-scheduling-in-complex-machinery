import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7274058558238109, 'demand': {1: 12.34, 2: 12.94, 3: 10.73, 4: 12.43, 5: 11.98, 6: 10.3, 7: 12.92, 8: 11.19, 9: 10.62, 10: 10.61, 11: 13.08, 12: 10.74, 13: 11.28, 14: 11.82, 15: 11.2, 16: 12.19, 17: 10.29, 18: 11.43, 19: 11.95, 20: 12.06}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x22.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7274058558238109,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.727405855823811,complexity="low",force_linear=False,params=params)
