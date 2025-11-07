import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5434661914855143, 'demand': {1: 11.25, 2: 10.39, 3: 11.99, 4: 11.25, 5: 12.28, 6: 11.65, 7: 13.21, 8: 13.15, 9: 10.24, 10: 12.53, 11: 12.4, 12: 10.99, 13: 10.39, 14: 11.6, 15: 11.18, 16: 12.46, 17: 13.06, 18: 11.27, 19: 10.97, 20: 11.66}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x38.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5434661914855143,complexity="low",force_linear=False,params=params)
