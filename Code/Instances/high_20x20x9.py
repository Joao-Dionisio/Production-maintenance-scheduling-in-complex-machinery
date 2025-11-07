import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3646358853618661, 'demand': {1: 10.73, 2: 10.76, 3: 10.66, 4: 10.68, 5: 12.08, 6: 13.0, 7: 12.8, 8: 11.6, 9: 12.18, 10: 12.67, 11: 10.28, 12: 12.2, 13: 13.03, 14: 12.61, 15: 12.5, 16: 11.59, 17: 10.6, 18: 12.63, 19: 11.11, 20: 12.67}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x9.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3646358853618661,complexity="high",force_linear=False,params=params)
