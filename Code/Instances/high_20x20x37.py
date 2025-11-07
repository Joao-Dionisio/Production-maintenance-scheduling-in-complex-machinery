import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6169784817366716, 'demand': {1: 10.87, 2: 12.39, 3: 11.05, 4: 10.92, 5: 10.01, 6: 12.52, 7: 13.05, 8: 12.11, 9: 13.14, 10: 10.08, 11: 10.78, 12: 11.58, 13: 13.19, 14: 13.18, 15: 11.29, 16: 10.84, 17: 11.43, 18: 11.64, 19: 13.09, 20: 10.61}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x37.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6169784817366716,complexity="high",force_linear=False,params=params)
