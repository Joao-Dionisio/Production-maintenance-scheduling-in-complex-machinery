import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.44935728583228585, 'demand': {1: 10.19, 2: 10.1, 3: 12.58, 4: 10.37, 5: 12.4, 6: 11.21, 7: 13.13, 8: 12.84, 9: 10.21, 10: 10.64, 11: 13.16, 12: 12.04, 13: 11.41, 14: 12.61, 15: 12.71, 16: 11.64, 17: 11.56, 18: 10.33, 19: 11.21, 20: 10.48}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x6.py', 'PT': False}

params[0] = get_random_machine(seed = 0.44935728583228585,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4493572858322858,complexity="low",force_linear=False,params=params)
