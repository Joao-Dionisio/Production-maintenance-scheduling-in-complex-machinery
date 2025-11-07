import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7784399949026813, 'demand': {1: 11.45, 2: 11.98, 3: 13.01, 4: 12.15, 5: 12.12, 6: 10.12, 7: 10.08, 8: 12.57, 9: 11.38, 10: 12.91, 11: 12.75, 12: 13.05, 13: 11.26, 14: 13.33, 15: 12.52, 16: 12.97, 17: 10.49, 18: 12.6, 19: 11.41, 20: 13.24}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x41.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7784399949026813,complexity="low",force_linear=False,params=params)
