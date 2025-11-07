import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4846579694115095, 'demand': {1: 10.25, 2: 11.31, 3: 11.27, 4: 11.4, 5: 10.96, 6: 11.5, 7: 12.47, 8: 10.25, 9: 10.25, 10: 11.78, 11: 11.93, 12: 12.66, 13: 10.11, 14: 10.03, 15: 12.03, 16: 10.72, 17: 11.65, 18: 10.98, 19: 10.29, 20: 11.87}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x42.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4846579694115095,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4846579694115096,complexity="high",force_linear=False,params=params)
