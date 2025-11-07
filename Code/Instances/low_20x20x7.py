import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6945967494508944, 'demand': {1: 12.21, 2: 12.53, 3: 11.21, 4: 12.35, 5: 10.94, 6: 11.62, 7: 12.57, 8: 12.3, 9: 10.98, 10: 13.15, 11: 12.17, 12: 11.94, 13: 10.04, 14: 11.82, 15: 10.84, 16: 12.24, 17: 11.54, 18: 12.72, 19: 12.16, 20: 12.66}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x7.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6945967494508944,complexity="low",force_linear=False,params=params)
