import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6968655345300366, 'demand': {1: 12.63, 2: 11.92, 3: 10.99, 4: 11.12, 5: 12.83, 6: 11.73, 7: 10.17, 8: 11.4, 9: 10.79, 10: 12.22, 11: 10.24, 12: 10.9, 13: 10.32, 14: 11.59, 15: 13.28, 16: 11.8, 17: 11.29, 18: 13.11, 19: 10.31, 20: 11.19}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x39.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6968655345300366,complexity="low",force_linear=False,params=params)
