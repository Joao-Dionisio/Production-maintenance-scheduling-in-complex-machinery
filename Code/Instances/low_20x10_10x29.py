import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.07060876046214681, 'demand': {1: 11.96, 2: 10.38, 3: 11.16, 4: 12.17, 5: 12.04, 6: 11.79, 7: 12.77, 8: 12.03, 9: 13.23, 10: 12.7, 11: 10.88, 12: 12.61, 13: 11.2, 14: 13.15, 15: 12.06, 16: 11.39, 17: 10.58, 18: 12.83, 19: 11.18, 20: 10.05}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x29.py', 'PT': False}

params[0] = get_random_machine(seed = 0.07060876046214681,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0706087604621468,complexity="low",force_linear=False,params=params)
