import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.37584830395281976, 'demand': {1: 11.44, 2: 10.75, 3: 10.97, 4: 13.24, 5: 11.27, 6: 13.2, 7: 13.05, 8: 11.99, 9: 10.87, 10: 13.27, 11: 11.65, 12: 11.38, 13: 11.06, 14: 13.28, 15: 11.64, 16: 10.95, 17: 11.59, 18: 10.41, 19: 12.07, 20: 11.48}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x12.py', 'PT': False}

params[0] = get_random_machine(seed = 0.37584830395281976,complexity="low",force_linear=False,params=params)
