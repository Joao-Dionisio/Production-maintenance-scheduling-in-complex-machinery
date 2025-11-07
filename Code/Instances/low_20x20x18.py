import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.15110920793301008, 'demand': {1: 12.1, 2: 11.69, 3: 13.03, 4: 11.85, 5: 12.07, 6: 10.88, 7: 11.84, 8: 10.85, 9: 12.5, 10: 11.72, 11: 10.45, 12: 10.78, 13: 11.24, 14: 12.46, 15: 10.6, 16: 12.38, 17: 12.18, 18: 10.28, 19: 12.23, 20: 10.3}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x18.py', 'PT': False}

params[0] = get_random_machine(seed = 0.15110920793301008,complexity="low",force_linear=False,params=params)
