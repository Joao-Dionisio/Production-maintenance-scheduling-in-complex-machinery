import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3672734015043406, 'demand': {1: 12.86, 2: 11.55, 3: 10.78, 4: 10.21, 5: 10.76, 6: 11.03, 7: 12.82, 8: 11.45, 9: 11.84, 10: 10.88, 11: 11.36, 12: 13.09, 13: 10.38, 14: 12.34, 15: 11.04, 16: 11.39, 17: 12.4, 18: 11.16, 19: 11.63, 20: 11.63}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x41.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3672734015043406,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3672734015043406,complexity="high",force_linear=False,params=params)
