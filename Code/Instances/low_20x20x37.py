import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.615732139054062, 'demand': {1: 10.35, 2: 12.53, 3: 12.45, 4: 12.72, 5: 12.68, 6: 12.38, 7: 13.08, 8: 13.19, 9: 12.08, 10: 13.22, 11: 10.34, 12: 10.34, 13: 10.21, 14: 10.69, 15: 11.25, 16: 11.53, 17: 12.27, 18: 12.48, 19: 10.28, 20: 11.34}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x37.py', 'PT': False}

params[0] = get_random_machine(seed = 0.615732139054062,complexity="low",force_linear=False,params=params)
