import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4526891905659062, 'demand': {1: 10.42, 2: 11.46, 3: 12.42, 4: 12.38, 5: 11.57, 6: 11.31, 7: 11.2, 8: 10.75, 9: 10.66, 10: 11.49, 11: 10.36, 12: 12.42, 13: 12.36, 14: 12.04, 15: 10.08, 16: 11.21, 17: 11.44, 18: 10.31, 19: 13.23, 20: 12.52}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x6.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4526891905659062,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.452689190565906,complexity="high",force_linear=False,params=params)
