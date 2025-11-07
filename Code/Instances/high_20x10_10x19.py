import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7376042837511602, 'demand': {1: 11.92, 2: 12.14, 3: 10.04, 4: 12.71, 5: 11.1, 6: 12.85, 7: 11.38, 8: 13.04, 9: 10.0, 10: 13.27, 11: 10.32, 12: 11.7, 13: 11.61, 14: 13.29, 15: 12.39, 16: 13.27, 17: 13.02, 18: 11.42, 19: 10.49, 20: 10.49}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x19.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7376042837511602,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.73760428375116,complexity="high",force_linear=False,params=params)
