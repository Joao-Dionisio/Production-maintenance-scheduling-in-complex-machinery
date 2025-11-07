import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.0840825975562709, 'demand': {1: 10.32, 2: 11.66, 3: 12.37, 4: 11.49, 5: 10.78, 6: 11.39, 7: 12.07, 8: 12.25, 9: 12.49, 10: 12.82, 11: 12.21, 12: 10.4, 13: 12.8, 14: 10.98, 15: 11.89, 16: 11.24, 17: 12.46, 18: 10.66, 19: 10.82, 20: 10.82}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x39.py', 'PT': False}

params[0] = get_random_machine(seed = 0.0840825975562709,complexity="high",force_linear=False,params=params)
