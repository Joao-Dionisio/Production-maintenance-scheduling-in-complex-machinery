import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.12981858115088285, 'demand': {1: 10.24, 2: 12.47, 3: 10.85, 4: 10.54, 5: 10.28, 6: 12.8, 7: 12.9, 8: 12.24, 9: 10.94, 10: 10.81, 11: 10.98, 12: 11.53, 13: 10.53, 14: 11.49, 15: 10.88, 16: 13.21, 17: 13.24, 18: 11.82, 19: 10.81, 20: 13.22}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x19.py', 'PT': False}

params[0] = get_random_machine(seed = 0.12981858115088285,complexity="high",force_linear=False,params=params)
