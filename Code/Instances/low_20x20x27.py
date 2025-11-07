import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5560841634875185, 'demand': {1: 12.99, 2: 12.18, 3: 12.53, 4: 11.92, 5: 11.47, 6: 12.72, 7: 12.18, 8: 13.18, 9: 12.43, 10: 12.34, 11: 10.89, 12: 12.71, 13: 11.27, 14: 10.43, 15: 10.22, 16: 10.56, 17: 10.88, 18: 12.25, 19: 10.95, 20: 10.21}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x27.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5560841634875185,complexity="low",force_linear=False,params=params)
