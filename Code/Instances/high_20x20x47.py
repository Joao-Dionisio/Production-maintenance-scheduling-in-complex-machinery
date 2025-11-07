import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.43059900675216545, 'demand': {1: 10.31, 2: 11.47, 3: 11.7, 4: 10.14, 5: 12.12, 6: 10.27, 7: 12.44, 8: 12.59, 9: 11.7, 10: 10.18, 11: 11.68, 12: 11.26, 13: 13.17, 14: 10.45, 15: 12.86, 16: 13.32, 17: 12.44, 18: 12.72, 19: 10.65, 20: 13.27}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x47.py', 'PT': False}

params[0] = get_random_machine(seed = 0.43059900675216545,complexity="high",force_linear=False,params=params)
