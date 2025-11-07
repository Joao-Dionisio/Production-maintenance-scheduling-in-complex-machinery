import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.31388792984782965, 'demand': {1: 10.36, 2: 11.81, 3: 13.07, 4: 11.99, 5: 12.86, 6: 10.71, 7: 10.06, 8: 11.8, 9: 11.62, 10: 11.9, 11: 11.26, 12: 12.08, 13: 12.42, 14: 13.04, 15: 11.03, 16: 11.5, 17: 12.75, 18: 10.75, 19: 10.39, 20: 11.04}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x25.py', 'PT': False}

params[0] = get_random_machine(seed = 0.31388792984782965,complexity="low",force_linear=False,params=params)
