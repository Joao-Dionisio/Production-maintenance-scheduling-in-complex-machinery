import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.31359943644592614, 'demand': {1: 11.84, 2: 11.57, 3: 12.66, 4: 10.23, 5: 12.96, 6: 10.06, 7: 13.18, 8: 12.62, 9: 10.06, 10: 10.18, 11: 10.4, 12: 10.3, 13: 10.56, 14: 10.72, 15: 11.74, 16: 11.64, 17: 10.83, 18: 13.29, 19: 11.98, 20: 11.7}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x47.py', 'PT': False}

params[0] = get_random_machine(seed = 0.31359943644592614,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.313599436445926,complexity="low",force_linear=False,params=params)
