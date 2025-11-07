import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4238807086771459, 'demand': {1: 11.69, 2: 10.36, 3: 11.71, 4: 11.11, 5: 12.04, 6: 12.29, 7: 10.34, 8: 10.24, 9: 12.99, 10: 10.68, 11: 12.26, 12: 12.43, 13: 12.61, 14: 10.02, 15: 12.13, 16: 12.81, 17: 10.12, 18: 10.02, 19: 12.95, 20: 12.31}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x38.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4238807086771459,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.423880708677146,complexity="low",force_linear=False,params=params)
