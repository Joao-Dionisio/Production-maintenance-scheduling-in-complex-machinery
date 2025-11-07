import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.793340083761663, 'demand': {1: 12.74, 2: 11.62, 3: 10.87, 4: 10.0, 5: 12.21, 6: 11.57, 7: 12.53, 8: 11.24, 9: 12.57, 10: 10.91, 11: 12.67, 12: 12.43, 13: 11.38, 14: 11.79, 15: 12.27, 16: 10.64, 17: 11.85, 18: 12.68, 19: 10.89, 20: 12.68}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.793340083761663,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.793340083761663,complexity="low",force_linear=False,params=params)
