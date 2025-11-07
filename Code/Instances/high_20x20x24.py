import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.06066101406364177, 'demand': {1: 10.9, 2: 12.24, 3: 12.31, 4: 12.25, 5: 10.97, 6: 11.72, 7: 11.55, 8: 11.55, 9: 10.4, 10: 12.98, 11: 10.66, 12: 13.26, 13: 13.12, 14: 10.06, 15: 11.53, 16: 12.73, 17: 13.23, 18: 11.5, 19: 10.9, 20: 10.7}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x24.py', 'PT': False}

params[0] = get_random_machine(seed = 0.06066101406364177,complexity="high",force_linear=False,params=params)
