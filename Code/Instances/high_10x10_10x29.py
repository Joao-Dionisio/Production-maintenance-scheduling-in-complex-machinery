import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.28377127228893784, 'demand': {1: 11.37, 2: 10.04, 3: 10.61, 4: 11.8, 5: 12.31, 6: 12.05, 7: 11.21, 8: 13.17, 9: 12.08, 10: 10.52}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_10x10_10x29.py', 'PT': False}

params[0] = get_random_machine(seed = 0.28377127228893784,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2837712722889378,complexity="high",force_linear=False,params=params)
