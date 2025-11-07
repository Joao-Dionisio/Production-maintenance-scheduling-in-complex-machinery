import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2350188440814771, 'demand': {1: 11.11, 2: 12.05, 3: 11.16, 4: 11.29, 5: 10.45, 6: 12.77, 7: 12.16, 8: 12.68, 9: 11.44, 10: 12.84, 11: 11.72, 12: 11.98, 13: 11.91, 14: 12.47, 15: 11.32, 16: 10.32, 17: 10.11, 18: 10.67, 19: 10.13, 20: 12.96}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x20.py', 'PT': False}

params[0] = get_random_machine(seed = 0.2350188440814771,complexity="low",force_linear=False,params=params)
