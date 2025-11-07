import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6744632620153453, 'demand': {1: 11.4, 2: 10.86, 3: 12.22, 4: 13.08, 5: 10.76, 6: 10.11, 7: 11.13, 8: 11.4, 9: 12.28, 10: 10.66, 11: 12.66, 12: 12.46, 13: 11.68, 14: 10.68, 15: 13.23, 16: 11.04, 17: 12.73, 18: 10.77, 19: 10.74, 20: 12.53}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x33.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6744632620153453,complexity="high",force_linear=False,params=params)
