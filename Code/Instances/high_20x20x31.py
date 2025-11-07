import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.24846528308918459, 'demand': {1: 10.36, 2: 10.51, 3: 11.74, 4: 12.27, 5: 13.14, 6: 12.41, 7: 12.16, 8: 12.55, 9: 11.52, 10: 11.84, 11: 10.13, 12: 12.61, 13: 10.78, 14: 13.07, 15: 12.15, 16: 11.01, 17: 10.43, 18: 10.84, 19: 12.12, 20: 12.33}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x31.py', 'PT': False}

params[0] = get_random_machine(seed = 0.24846528308918459,complexity="high",force_linear=False,params=params)
