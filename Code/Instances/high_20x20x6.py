import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.20876318544616446, 'demand': {1: 10.54, 2: 11.13, 3: 10.18, 4: 10.0, 5: 10.5, 6: 10.34, 7: 11.21, 8: 10.09, 9: 12.91, 10: 12.05, 11: 10.5, 12: 10.84, 13: 11.16, 14: 11.21, 15: 10.41, 16: 12.83, 17: 13.31, 18: 11.55, 19: 11.61, 20: 10.29}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x6.py', 'PT': False}

params[0] = get_random_machine(seed = 0.20876318544616446,complexity="high",force_linear=False,params=params)
