import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.810780041542835, 'demand': {1: 10.02, 2: 12.55, 3: 11.2, 4: 10.05, 5: 10.84, 6: 11.53, 7: 11.28, 8: 11.72, 9: 10.18, 10: 10.73, 11: 13.25, 12: 11.48, 13: 11.57, 14: 10.28, 15: 10.93, 16: 13.18, 17: 12.29, 18: 11.69, 19: 10.18, 20: 11.31}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x40.py', 'PT': False}

params[0] = get_random_machine(seed = 0.810780041542835,complexity="low",force_linear=False,params=params)
