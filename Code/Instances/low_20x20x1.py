import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.15960421235803823, 'demand': {1: 12.66, 2: 10.46, 3: 12.06, 4: 10.42, 5: 10.01, 6: 12.9, 7: 10.7, 8: 10.72, 9: 13.27, 10: 12.91, 11: 10.96, 12: 13.2, 13: 11.8, 14: 12.26, 15: 10.68, 16: 13.14, 17: 12.3, 18: 13.22, 19: 12.98, 20: 11.0}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x1.py', 'PT': False}

params[0] = get_random_machine(seed = 0.15960421235803823,complexity="low",force_linear=False,params=params)
