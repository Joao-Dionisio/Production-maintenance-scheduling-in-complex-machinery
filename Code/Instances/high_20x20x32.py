import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.11213268413726074, 'demand': {1: 10.23, 2: 11.75, 3: 11.94, 4: 11.29, 5: 10.75, 6: 12.0, 7: 10.03, 8: 11.01, 9: 11.54, 10: 13.2, 11: 12.15, 12: 12.95, 13: 11.58, 14: 10.78, 15: 10.82, 16: 13.2, 17: 12.35, 18: 11.02, 19: 10.07, 20: 11.66}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x32.py', 'PT': False}

params[0] = get_random_machine(seed = 0.11213268413726074,complexity="high",force_linear=False,params=params)
