import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6070864972291193, 'demand': {1: 12.88, 2: 12.18, 3: 11.07, 4: 10.13, 5: 13.07, 6: 12.86, 7: 12.18, 8: 11.22, 9: 12.76, 10: 12.72, 11: 12.42, 12: 12.0, 13: 11.06, 14: 10.99, 15: 11.19, 16: 11.09, 17: 11.73, 18: 10.38, 19: 12.4, 20: 11.16}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x11.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6070864972291193,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.6070864972291194,complexity="high",force_linear=False,params=params)
