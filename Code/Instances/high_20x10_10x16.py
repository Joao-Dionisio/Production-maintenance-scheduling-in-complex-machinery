import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9467577064021973, 'demand': {1: 12.17, 2: 11.59, 3: 10.57, 4: 10.79, 5: 11.22, 6: 11.15, 7: 11.24, 8: 12.69, 9: 11.25, 10: 12.1, 11: 10.13, 12: 10.47, 13: 12.37, 14: 12.97, 15: 11.04, 16: 10.11, 17: 10.78, 18: 11.2, 19: 11.22, 20: 11.87}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x16.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9467577064021973,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.9467577064021973,complexity="high",force_linear=False,params=params)
