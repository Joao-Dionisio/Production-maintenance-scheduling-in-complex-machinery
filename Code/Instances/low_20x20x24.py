import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.09381466147702944, 'demand': {1: 10.24, 2: 13.0, 3: 11.64, 4: 13.12, 5: 10.18, 6: 10.81, 7: 10.17, 8: 11.32, 9: 10.2, 10: 10.85, 11: 11.36, 12: 11.02, 13: 10.17, 14: 10.13, 15: 13.24, 16: 10.6, 17: 11.7, 18: 11.34, 19: 11.77, 20: 10.28}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x24.py', 'PT': False}

params[0] = get_random_machine(seed = 0.09381466147702944,complexity="low",force_linear=False,params=params)
