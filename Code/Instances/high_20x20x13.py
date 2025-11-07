import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7599931425900166, 'demand': {1: 13.04, 2: 11.48, 3: 12.04, 4: 11.69, 5: 11.71, 6: 12.31, 7: 11.51, 8: 11.78, 9: 11.59, 10: 13.14, 11: 12.33, 12: 12.92, 13: 13.14, 14: 10.87, 15: 11.87, 16: 13.14, 17: 12.8, 18: 10.46, 19: 10.41, 20: 11.47}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x13.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7599931425900166,complexity="high",force_linear=False,params=params)
