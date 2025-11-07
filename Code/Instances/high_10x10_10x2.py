import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.731894708878718, 'demand': {1: 12.85, 2: 12.93, 3: 10.29, 4: 12.02, 5: 12.24, 6: 11.69, 7: 10.59, 8: 11.58, 9: 10.3, 10: 13.12}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_10x10_10x2.py', 'PT': False}

params[0] = get_random_machine(seed = 0.731894708878718,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.731894708878718,complexity="high",force_linear=False,params=params)
