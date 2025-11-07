import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8118230406087196, 'demand': {1: 10.23, 2: 10.77, 3: 12.73, 4: 12.64, 5: 12.21, 6: 10.09, 7: 12.41, 8: 13.26, 9: 13.33, 10: 12.34, 11: 10.16, 12: 12.81, 13: 10.73, 14: 12.15, 15: 13.17, 16: 12.37, 17: 10.45, 18: 10.97, 19: 13.06, 20: 10.5}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x16.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8118230406087196,complexity="low",force_linear=False,params=params)
