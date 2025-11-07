import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.34590555946747037, 'demand': {1: 11.82, 2: 12.95, 3: 11.51, 4: 13.27, 5: 12.39, 6: 10.15, 7: 12.49, 8: 12.21, 9: 12.07, 10: 10.01, 11: 12.93, 12: 11.65, 13: 11.79, 14: 10.57, 15: 10.12, 16: 10.05, 17: 10.7, 18: 11.01, 19: 10.51, 20: 10.19}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x21.py', 'PT': False}

params[0] = get_random_machine(seed = 0.34590555946747037,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3459055594674703,complexity="low",force_linear=False,params=params)
