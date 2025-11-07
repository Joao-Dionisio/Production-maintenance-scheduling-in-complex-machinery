import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.027738156560282667, 'demand': {1: 10.42, 2: 11.49, 3: 11.11, 4: 11.73, 5: 12.3, 6: 11.98, 7: 12.62, 8: 11.57, 9: 12.25, 10: 11.39, 11: 10.42, 12: 10.25, 13: 10.61, 14: 11.48, 15: 10.92, 16: 11.87, 17: 12.22, 18: 13.06, 19: 10.5, 20: 13.19}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x28.py', 'PT': False}

params[0] = get_random_machine(seed = 0.027738156560282667,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0277381565602828,complexity="high",force_linear=False,params=params)
