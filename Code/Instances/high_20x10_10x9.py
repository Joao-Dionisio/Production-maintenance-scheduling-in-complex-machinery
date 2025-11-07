import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5289337598332745, 'demand': {1: 12.79, 2: 10.9, 3: 10.23, 4: 12.44, 5: 10.9, 6: 11.4, 7: 10.39, 8: 12.76, 9: 10.91, 10: 10.97, 11: 12.68, 12: 11.68, 13: 10.92, 14: 12.96, 15: 11.37, 16: 11.2, 17: 13.22, 18: 12.63, 19: 12.49, 20: 10.83}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x9.py', 'PT': False}

params[0] = get_random_machine(seed = 0.5289337598332745,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.5289337598332744,complexity="high",force_linear=False,params=params)
