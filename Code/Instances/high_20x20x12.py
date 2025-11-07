import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5235065855871663, 'demand': {1: 10.06, 2: 11.47, 3: 10.61, 4: 10.01, 5: 12.66, 6: 10.57, 7: 11.58, 8: 12.42, 9: 11.85, 10: 11.09, 11: 11.73, 12: 11.85, 13: 12.61, 14: 10.35, 15: 11.87, 16: 10.83, 17: 10.92, 18: 12.57, 19: 11.69, 20: 11.87}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x12.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5235065855871663,complexity="high",force_linear=False,params=params)
