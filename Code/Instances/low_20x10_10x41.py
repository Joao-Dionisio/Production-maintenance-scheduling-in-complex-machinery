import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5112515749776524, 'demand': {1: 12.83, 2: 12.83, 3: 12.85, 4: 12.38, 5: 10.26, 6: 13.06, 7: 10.52, 8: 10.05, 9: 11.69, 10: 10.06, 11: 10.14, 12: 10.64, 13: 13.28, 14: 10.92, 15: 12.84, 16: 13.14, 17: 10.74, 18: 10.35, 19: 10.72, 20: 12.13}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x41.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5112515749776524,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.5112515749776523,complexity="low",force_linear=False,params=params)
