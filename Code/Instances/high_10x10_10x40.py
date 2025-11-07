import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.20084864404767933, 'demand': {1: 10.24, 2: 12.61, 3: 13.03, 4: 12.32, 5: 10.39, 6: 13.26, 7: 12.76, 8: 11.7, 9: 10.0, 10: 12.81}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_10x10_10x40.py', 'PT': False}

params[0] = get_random_machine(seed = 0.20084864404767933,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.2008486440476793,complexity="high",force_linear=False,params=params)
