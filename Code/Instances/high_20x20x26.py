import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.31607804537496975, 'demand': {1: 12.8, 2: 10.01, 3: 12.5, 4: 12.8, 5: 10.4, 6: 13.09, 7: 12.38, 8: 13.01, 9: 10.97, 10: 11.24, 11: 11.31, 12: 13.33, 13: 11.96, 14: 11.2, 15: 11.43, 16: 10.92, 17: 10.16, 18: 10.34, 19: 12.78, 20: 10.95}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x26.py', 'PT': False}

params[0] = get_random_machine(seed = 0.31607804537496975,complexity="high",force_linear=False,params=params)
