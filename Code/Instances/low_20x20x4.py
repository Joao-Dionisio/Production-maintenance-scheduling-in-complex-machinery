import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.0911798641717686, 'demand': {1: 11.14, 2: 12.04, 3: 13.06, 4: 11.13, 5: 13.08, 6: 11.82, 7: 11.04, 8: 11.06, 9: 10.59, 10: 10.26, 11: 10.5, 12: 12.3, 13: 13.32, 14: 10.54, 15: 10.16, 16: 13.29, 17: 11.78, 18: 11.35, 19: 10.79, 20: 11.98}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x4.py', 'PT': False}

params[0] = get_random_machine(seed = 0.0911798641717686,complexity="low",force_linear=False,params=params)
