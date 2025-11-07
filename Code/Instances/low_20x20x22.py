import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.03209550935252348, 'demand': {1: 13.08, 2: 11.23, 3: 13.13, 4: 12.29, 5: 12.25, 6: 11.57, 7: 13.15, 8: 10.39, 9: 12.23, 10: 10.97, 11: 12.25, 12: 12.43, 13: 10.54, 14: 10.67, 15: 10.08, 16: 10.77, 17: 10.26, 18: 11.34, 19: 13.25, 20: 11.21}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x22.py', 'PT': False}

params[0] = get_random_machine(seed = 0.03209550935252348,complexity="low",force_linear=False,params=params)
