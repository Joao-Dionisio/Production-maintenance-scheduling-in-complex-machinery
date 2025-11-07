import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8163716167559534, 'demand': {1: 12.13, 2: 11.79, 3: 10.11, 4: 10.58, 5: 11.23, 6: 10.17, 7: 13.31, 8: 12.55, 9: 13.17, 10: 12.34, 11: 11.14, 12: 10.26, 13: 12.44, 14: 10.38, 15: 11.82, 16: 11.55, 17: 11.65, 18: 10.25, 19: 10.25, 20: 11.73}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x9.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8163716167559534,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8163716167559534,complexity="low",force_linear=False,params=params)
