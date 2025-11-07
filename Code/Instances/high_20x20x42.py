import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6783197400853727, 'demand': {1: 10.62, 2: 11.04, 3: 10.68, 4: 12.65, 5: 11.83, 6: 10.21, 7: 10.34, 8: 11.32, 9: 11.83, 10: 12.13, 11: 10.3, 12: 10.55, 13: 12.32, 14: 11.37, 15: 10.94, 16: 11.03, 17: 13.18, 18: 11.04, 19: 11.89, 20: 11.19}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x42.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6783197400853727,complexity="high",force_linear=False,params=params)
