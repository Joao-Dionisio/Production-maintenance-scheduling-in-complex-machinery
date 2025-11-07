import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.32966499504776237, 'demand': {1: 10.74, 2: 12.71, 3: 13.28, 4: 12.84, 5: 12.69, 6: 12.73, 7: 12.47, 8: 10.76, 9: 11.73, 10: 11.19, 11: 10.1, 12: 10.09, 13: 10.93, 14: 10.86, 15: 12.31, 16: 13.19, 17: 11.49, 18: 13.12, 19: 13.29, 20: 13.18}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x8.py', 'PT': False}

params[0] = get_random_machine(seed = 0.32966499504776237,complexity="high",force_linear=False,params=params)
