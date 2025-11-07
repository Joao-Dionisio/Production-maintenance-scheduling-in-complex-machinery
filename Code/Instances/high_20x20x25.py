import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9455872768948678, 'demand': {1: 10.7, 2: 11.94, 3: 10.47, 4: 11.75, 5: 13.18, 6: 10.44, 7: 12.73, 8: 11.7, 9: 12.96, 10: 12.34, 11: 10.77, 12: 12.99, 13: 11.62, 14: 10.08, 15: 10.01, 16: 11.64, 17: 11.5, 18: 11.01, 19: 10.47, 20: 11.15}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x25.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9455872768948678,complexity="high",force_linear=False,params=params)
