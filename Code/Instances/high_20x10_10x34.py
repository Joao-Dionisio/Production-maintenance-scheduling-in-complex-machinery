import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9924479470672777, 'demand': {1: 12.31, 2: 12.52, 3: 12.95, 4: 12.09, 5: 11.82, 6: 12.75, 7: 11.77, 8: 13.19, 9: 12.54, 10: 10.0, 11: 10.96, 12: 12.95, 13: 10.39, 14: 10.05, 15: 11.94, 16: 12.31, 17: 13.27, 18: 13.21, 19: 12.09, 20: 12.33}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x34.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9924479470672777,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.9924479470672778,complexity="high",force_linear=False,params=params)
