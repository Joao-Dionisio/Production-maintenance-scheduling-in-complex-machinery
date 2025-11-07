import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3391517772846362, 'demand': {1: 11.84, 2: 13.09, 3: 10.89, 4: 10.43, 5: 11.76, 6: 10.79, 7: 10.36, 8: 10.54, 9: 10.17, 10: 10.67, 11: 11.04, 12: 11.02, 13: 12.53, 14: 10.97, 15: 11.67, 16: 10.59, 17: 11.16, 18: 10.06, 19: 10.83, 20: 10.05}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x17.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3391517772846362,complexity="high",force_linear=False,params=params)
