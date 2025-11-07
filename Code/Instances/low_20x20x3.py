import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7877383039804342, 'demand': {1: 11.22, 2: 11.93, 3: 10.03, 4: 10.16, 5: 10.6, 6: 13.18, 7: 10.66, 8: 12.52, 9: 13.1, 10: 13.14, 11: 11.15, 12: 11.18, 13: 11.75, 14: 12.59, 15: 10.36, 16: 12.49, 17: 12.66, 18: 12.87, 19: 10.12, 20: 13.15}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x3.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7877383039804342,complexity="low",force_linear=False,params=params)
