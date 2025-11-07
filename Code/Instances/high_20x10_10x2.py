import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8809596854831049, 'demand': {1: 10.95, 2: 11.19, 3: 12.93, 4: 10.45, 5: 12.55, 6: 10.33, 7: 12.3, 8: 12.34, 9: 13.17, 10: 12.81, 11: 11.68, 12: 10.66, 13: 10.5, 14: 11.76, 15: 11.7, 16: 10.24, 17: 13.01, 18: 11.69, 19: 12.34, 20: 10.73}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x2.py', 'PT': False}

params[0] = get_random_machine(seed = 0.8809596854831049,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.8809596854831048,complexity="high",force_linear=False,params=params)
