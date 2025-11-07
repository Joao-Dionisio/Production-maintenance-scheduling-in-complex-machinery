import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4500236444364596, 'demand': {1: 12.18, 2: 13.08, 3: 11.23, 4: 11.77, 5: 12.38, 6: 13.12, 7: 13.17, 8: 13.29, 9: 11.01, 10: 10.56, 11: 13.11, 12: 10.26, 13: 11.5, 14: 12.45, 15: 11.76, 16: 11.3, 17: 13.08, 18: 11.0, 19: 11.84, 20: 12.77}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x45.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4500236444364596,complexity="low",force_linear=False,params=params)
