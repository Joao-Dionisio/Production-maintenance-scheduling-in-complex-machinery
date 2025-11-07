import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.032180898337640595, 'demand': {1: 11.81, 2: 12.62, 3: 10.75, 4: 11.88, 5: 13.07, 6: 10.98, 7: 11.57, 8: 12.41, 9: 12.88, 10: 10.56, 11: 12.2, 12: 10.4, 13: 10.37, 14: 13.28, 15: 10.17, 16: 13.07, 17: 12.5, 18: 12.25, 19: 12.43, 20: 12.17}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x12.py', 'PT': False}

params[0] = get_random_machine(seed = 0.032180898337640595,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0321808983376406,complexity="low",force_linear=False,params=params)
