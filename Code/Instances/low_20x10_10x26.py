import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.32728094527416884, 'demand': {1: 11.4, 2: 12.31, 3: 12.04, 4: 11.63, 5: 11.08, 6: 12.05, 7: 10.64, 8: 10.59, 9: 10.38, 10: 12.23, 11: 10.46, 12: 10.74, 13: 11.17, 14: 11.88, 15: 12.16, 16: 11.97, 17: 11.99, 18: 10.64, 19: 13.04, 20: 12.46}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x26.py', 'PT': False}

params[0] = get_random_machine(seed = 0.32728094527416884,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3272809452741687,complexity="low",force_linear=False,params=params)
