import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.4089525048369588, 'demand': {1: 10.01, 2: 11.43, 3: 12.92, 4: 12.17, 5: 10.76, 6: 10.35, 7: 12.96, 8: 10.26, 9: 12.05, 10: 11.99, 11: 10.61, 12: 11.47, 13: 12.87, 14: 13.32, 15: 10.25, 16: 10.1, 17: 10.87, 18: 10.17, 19: 13.09, 20: 10.27}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x40.py', 'PT': False}

params[0] = get_random_machine(seed = 0.4089525048369588,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.4089525048369587,complexity="high",force_linear=False,params=params)
