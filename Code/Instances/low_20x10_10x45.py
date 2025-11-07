import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2729556035961721, 'demand': {1: 10.52, 2: 10.17, 3: 13.28, 4: 12.7, 5: 10.8, 6: 10.39, 7: 11.73, 8: 11.79, 9: 13.12, 10: 11.28, 11: 10.44, 12: 12.82, 13: 10.49, 14: 10.81, 15: 10.73, 16: 12.9, 17: 13.22, 18: 11.27, 19: 12.1, 20: 12.35}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x45.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2729556035961721,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2729556035961722,complexity="low",force_linear=False,params=params)
