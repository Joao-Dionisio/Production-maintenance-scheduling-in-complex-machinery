import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5831937655371546, 'demand': {1: 13.1, 2: 11.24, 3: 12.89, 4: 11.5, 5: 10.87, 6: 12.59, 7: 13.15, 8: 10.35, 9: 11.99, 10: 12.07, 11: 10.73, 12: 11.23, 13: 10.47, 14: 10.68, 15: 10.85, 16: 12.0, 17: 12.17, 18: 10.68, 19: 10.04, 20: 11.09}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x41.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5831937655371546,complexity="high",force_linear=False,params=params)
