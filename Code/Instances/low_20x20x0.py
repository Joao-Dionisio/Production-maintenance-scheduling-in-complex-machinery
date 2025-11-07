import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6229016948897019, 'demand': {1: 12.47, 2: 12.65, 3: 13.14, 4: 12.47, 5: 13.07, 6: 10.1, 7: 11.55, 8: 13.14, 9: 12.16, 10: 13.0, 11: 10.38, 12: 11.56, 13: 10.82, 14: 11.81, 15: 11.91, 16: 10.04, 17: 10.72, 18: 10.93, 19: 13.05, 20: 12.55}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6229016948897019,complexity="low",force_linear=False,params=params)
