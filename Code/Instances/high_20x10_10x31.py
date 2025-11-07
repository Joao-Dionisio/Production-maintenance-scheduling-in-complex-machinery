import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6232190062478531, 'demand': {1: 11.82, 2: 13.13, 3: 10.17, 4: 10.06, 5: 12.41, 6: 10.33, 7: 10.46, 8: 12.72, 9: 11.21, 10: 12.94, 11: 12.67, 12: 12.21, 13: 11.2, 14: 10.28, 15: 13.25, 16: 12.9, 17: 13.06, 18: 11.7, 19: 10.94, 20: 12.09}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x31.py', 'PT': False}

params[0] = get_random_machine(seed = 0.6232190062478531,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.623219006247853,complexity="high",force_linear=False,params=params)
