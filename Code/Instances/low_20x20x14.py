import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5334979199471123, 'demand': {1: 11.12, 2: 10.99, 3: 11.77, 4: 11.55, 5: 11.2, 6: 12.48, 7: 11.97, 8: 10.12, 9: 10.84, 10: 11.52, 11: 13.06, 12: 12.96, 13: 11.82, 14: 10.05, 15: 12.59, 16: 11.43, 17: 11.92, 18: 12.36, 19: 12.11, 20: 11.61}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x14.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5334979199471123,complexity="low",force_linear=False,params=params)
