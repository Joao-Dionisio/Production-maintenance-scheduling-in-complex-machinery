import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.48099206880664347, 'demand': {1: 12.53, 2: 10.0, 3: 11.57, 4: 12.97, 5: 12.06, 6: 11.43, 7: 11.55, 8: 10.33, 9: 10.52, 10: 10.53, 11: 11.25, 12: 11.29, 13: 12.93, 14: 10.51, 15: 10.85, 16: 10.92, 17: 10.54, 18: 10.96, 19: 10.78, 20: 11.61}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x20x21.py', 'PT': False}

params[0] = get_random_machine(seed = 0.48099206880664347,complexity="low",force_linear=False,params=params)
