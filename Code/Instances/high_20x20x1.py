import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.04658268061775628, 'demand': {1: 12.86, 2: 10.97, 3: 10.48, 4: 10.39, 5: 11.03, 6: 12.72, 7: 10.6, 8: 11.94, 9: 12.13, 10: 11.24, 11: 11.83, 12: 10.21, 13: 10.2, 14: 10.69, 15: 12.27, 16: 11.43, 17: 11.05, 18: 11.95, 19: 11.51, 20: 11.0}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x1.py', 'PT': False}

params[0] = get_random_machine(seed = 0.04658268061775628,complexity="high",force_linear=False,params=params)
