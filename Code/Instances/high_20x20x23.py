import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2521935314626901, 'demand': {1: 10.25, 2: 10.89, 3: 12.43, 4: 10.68, 5: 12.47, 6: 13.25, 7: 11.65, 8: 11.28, 9: 11.6, 10: 12.28, 11: 12.56, 12: 12.06, 13: 12.14, 14: 10.26, 15: 10.49, 16: 10.85, 17: 12.48, 18: 11.01, 19: 11.89, 20: 10.04}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x23.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2521935314626901,complexity="high",force_linear=False,params=params)
