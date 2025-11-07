import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.36118993472238414, 'demand': {1: 10.55, 2: 10.49, 3: 10.22, 4: 11.0, 5: 12.01, 6: 10.01, 7: 12.26, 8: 11.13, 9: 11.03, 10: 12.73, 11: 11.6, 12: 11.05, 13: 11.6, 14: 12.35, 15: 10.19, 16: 13.25, 17: 10.08, 18: 12.5, 19: 12.82, 20: 10.06}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x2.py', 'PT': False}

params[0] = get_random_machine(seed = 0.36118993472238414,complexity="low",force_linear=False,params=params)
