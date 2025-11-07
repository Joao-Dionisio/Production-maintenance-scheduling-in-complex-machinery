import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5995197702626399, 'demand': {1: 11.83, 2: 12.09, 3: 11.02, 4: 11.4, 5: 11.94, 6: 11.42, 7: 12.2, 8: 11.49, 9: 11.46, 10: 10.08, 11: 12.06, 12: 11.63, 13: 10.78, 14: 12.55, 15: 12.6, 16: 11.53, 17: 10.6, 18: 11.58, 19: 10.36, 20: 10.43}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x46.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5995197702626399,complexity="high",force_linear=False,params=params)
