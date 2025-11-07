import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.46553144887721676, 'demand': {1: 10.52, 2: 10.72, 3: 10.88, 4: 13.16, 5: 10.68, 6: 10.29, 7: 11.18, 8: 10.26, 9: 11.42, 10: 12.07, 11: 12.17, 12: 10.58, 13: 10.46, 14: 11.64, 15: 12.29, 16: 11.49, 17: 11.91, 18: 13.04, 19: 10.48, 20: 10.89}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x49.py', 'PT': False}

params[0] = get_random_machine(seed = 0.46553144887721676,complexity="low",force_linear=False,params=params)
