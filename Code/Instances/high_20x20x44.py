import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3708436246011326, 'demand': {1: 11.68, 2: 10.49, 3: 10.94, 4: 11.74, 5: 13.08, 6: 10.36, 7: 11.64, 8: 12.68, 9: 13.22, 10: 10.66, 11: 10.42, 12: 13.14, 13: 13.25, 14: 11.61, 15: 10.18, 16: 13.09, 17: 11.29, 18: 13.01, 19: 12.07, 20: 12.75}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x44.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3708436246011326,complexity="high",force_linear=False,params=params)
