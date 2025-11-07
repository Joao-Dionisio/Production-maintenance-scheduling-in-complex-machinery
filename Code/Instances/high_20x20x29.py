import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.13959606399972213, 'demand': {1: 10.64, 2: 10.3, 3: 11.14, 4: 10.3, 5: 10.8, 6: 10.86, 7: 11.9, 8: 12.96, 9: 12.5, 10: 11.38, 11: 11.38, 12: 11.75, 13: 11.26, 14: 11.13, 15: 10.21, 16: 10.93, 17: 13.23, 18: 10.42, 19: 11.68, 20: 12.1}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x29.py', 'PT': False}

params[0] = get_random_machine(seed = 0.13959606399972213,complexity="high",force_linear=False,params=params)
