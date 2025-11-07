import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.41644538207510984, 'demand': {1: 12.88, 2: 13.32, 3: 11.21, 4: 10.66, 5: 12.43, 6: 10.68, 7: 10.02, 8: 13.01, 9: 11.41, 10: 12.73, 11: 11.35, 12: 12.94, 13: 11.54, 14: 10.54, 15: 10.05, 16: 11.84, 17: 12.14, 18: 13.03, 19: 10.3, 20: 12.07}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x43.py', 'PT': False}

params[0] = get_random_machine(seed = 0.41644538207510984,complexity="high",force_linear=False,params=params)
