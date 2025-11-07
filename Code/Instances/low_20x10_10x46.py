import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.45349534013851045, 'demand': {1: 12.7, 2: 11.05, 3: 12.45, 4: 10.55, 5: 10.47, 6: 10.52, 7: 10.59, 8: 13.21, 9: 10.82, 10: 12.18, 11: 10.04, 12: 12.9, 13: 12.49, 14: 12.22, 15: 13.29, 16: 10.11, 17: 12.54, 18: 10.4, 19: 13.14, 20: 10.03}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x46.py', 'PT': False}

params[0] = get_random_machine(seed = 0.45349534013851045,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4534953401385104,complexity="low",force_linear=False,params=params)
