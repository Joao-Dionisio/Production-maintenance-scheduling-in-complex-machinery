import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.035121778774216184, 'demand': {1: 13.12, 2: 10.51, 3: 10.62, 4: 10.42, 5: 11.27, 6: 10.54, 7: 12.38, 8: 11.18, 9: 10.42, 10: 11.22, 11: 12.74, 12: 11.83, 13: 10.23, 14: 11.96, 15: 11.64, 16: 11.73, 17: 12.5, 18: 10.48, 19: 12.33, 20: 12.57}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x49.py', 'PT': False}

params[0] = get_random_machine(seed = 0.035121778774216184,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0351217787742162,complexity="high",force_linear=False,params=params)
