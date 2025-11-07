import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.16027614951375435, 'demand': {1: 12.62, 2: 10.74, 3: 11.35, 4: 12.82, 5: 12.76, 6: 10.61, 7: 10.73, 8: 11.33, 9: 11.73, 10: 11.28, 11: 10.41, 12: 10.82, 13: 12.42, 14: 12.99, 15: 10.14, 16: 11.87, 17: 12.52, 18: 10.13, 19: 12.79, 20: 10.39}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x45.py', 'PT': False}

params[0] = get_random_machine(seed = 0.16027614951375435,complexity="high",force_linear=False,params=params)
