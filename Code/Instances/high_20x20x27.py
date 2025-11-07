import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9355898883112846, 'demand': {1: 10.83, 2: 10.89, 3: 11.7, 4: 10.63, 5: 11.24, 6: 13.19, 7: 12.95, 8: 12.71, 9: 12.1, 10: 13.04, 11: 13.14, 12: 11.83, 13: 12.4, 14: 10.16, 15: 12.44, 16: 11.5, 17: 12.51, 18: 12.15, 19: 10.95, 20: 10.16}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x27.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9355898883112846,complexity="high",force_linear=False,params=params)
