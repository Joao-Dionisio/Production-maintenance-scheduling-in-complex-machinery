import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5943698771050184, 'demand': {1: 11.93, 2: 11.52, 3: 12.8, 4: 13.15, 5: 11.58, 6: 12.21, 7: 10.2, 8: 12.34, 9: 12.16, 10: 13.31, 11: 12.74, 12: 10.95, 13: 11.29, 14: 12.23, 15: 10.08, 16: 11.54, 17: 10.56, 18: 10.39, 19: 10.2, 20: 12.56}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x3.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5943698771050184,complexity="high",force_linear=False,params=params)
