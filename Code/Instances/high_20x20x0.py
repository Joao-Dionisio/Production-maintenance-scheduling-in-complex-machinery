import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.32383276483316237, 'demand': {1: 10.5, 2: 12.17, 3: 10.24, 4: 11.79, 5: 11.22, 6: 10.19, 7: 11.69, 8: 10.12, 9: 11.45, 10: 10.23, 11: 10.3, 12: 11.42, 13: 12.76, 14: 10.41, 15: 10.74, 16: 12.09, 17: 13.16, 18: 11.92, 19: 11.32, 20: 13.25}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x0.py', 'PT': False}

params[0] = get_random_machine(seed = 0.32383276483316237,complexity="high",force_linear=False,params=params)
