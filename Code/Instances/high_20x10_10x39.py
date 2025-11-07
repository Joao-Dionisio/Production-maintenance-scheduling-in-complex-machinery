import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.40438544011708444, 'demand': {1: 10.08, 2: 11.46, 3: 13.3, 4: 11.35, 5: 12.21, 6: 11.2, 7: 12.25, 8: 11.12, 9: 13.04, 10: 11.37, 11: 10.9, 12: 11.43, 13: 10.25, 14: 11.1, 15: 12.46, 16: 11.35, 17: 11.49, 18: 10.78, 19: 12.75, 20: 12.95}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x39.py', 'PT': False}

params[0] = get_random_machine(seed = 0.40438544011708444,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4043854401170845,complexity="high",force_linear=False,params=params)
