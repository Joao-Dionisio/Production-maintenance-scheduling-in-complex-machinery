import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.07254609965648828, 'demand': {1: 10.8, 2: 10.24, 3: 12.23, 4: 12.61, 5: 12.99, 6: 10.51, 7: 12.39, 8: 12.2, 9: 10.48, 10: 12.94, 11: 13.23, 12: 10.73, 13: 13.18, 14: 11.33, 15: 11.62, 16: 13.3, 17: 12.77, 18: 10.54, 19: 11.44, 20: 11.72}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x14.py', 'PT': False}

params[0] = get_random_machine(seed = 0.07254609965648828,complexity="high",force_linear=False,params=params)
