import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.30954791767795276, 'demand': {1: 11.19, 2: 10.0, 3: 11.27, 4: 11.58, 5: 11.68, 6: 10.67, 7: 11.68, 8: 10.02, 9: 10.88, 10: 10.3, 11: 11.33, 12: 10.14, 13: 10.07, 14: 11.01, 15: 10.78, 16: 11.95, 17: 11.76, 18: 12.5, 19: 12.19, 20: 12.39}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x20.py', 'PT': False}

params[0] = get_random_machine(seed = 0.30954791767795276,complexity="high",force_linear=False,params=params)
