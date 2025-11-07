import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3152788304077655, 'demand': {1: 11.62, 2: 12.9, 3: 11.5, 4: 12.81, 5: 10.98, 6: 10.61, 7: 11.34, 8: 10.99, 9: 12.42, 10: 10.4, 11: 12.41, 12: 10.73, 13: 11.36, 14: 10.72, 15: 10.48, 16: 10.46, 17: 13.29, 18: 10.33, 19: 13.08, 20: 11.53}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x43.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3152788304077655,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3152788304077654,complexity="high",force_linear=False,params=params)
