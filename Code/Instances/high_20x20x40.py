import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.1533221995931423, 'demand': {1: 12.95, 2: 11.93, 3: 11.09, 4: 11.32, 5: 13.31, 6: 11.69, 7: 10.77, 8: 12.69, 9: 12.18, 10: 13.3, 11: 10.34, 12: 11.58, 13: 12.73, 14: 12.8, 15: 13.05, 16: 10.13, 17: 10.98, 18: 10.4, 19: 10.63, 20: 13.24}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x40.py', 'PT': False}

params[0] = get_random_machine(seed = 0.1533221995931423,complexity="high",force_linear=False,params=params)
