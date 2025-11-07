import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3292427598735952, 'demand': {1: 10.62, 2: 13.12, 3: 12.49, 4: 10.11, 5: 12.21, 6: 11.26, 7: 11.25, 8: 11.11, 9: 10.56, 10: 10.01, 11: 10.93, 12: 11.17, 13: 13.19, 14: 10.41, 15: 13.21, 16: 10.69, 17: 11.19, 18: 12.74, 19: 12.74, 20: 11.44}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x35.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3292427598735952,complexity="high",force_linear=False,params=params)
