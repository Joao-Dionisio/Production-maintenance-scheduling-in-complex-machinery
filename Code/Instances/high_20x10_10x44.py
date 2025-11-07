import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.882167025395479, 'demand': {1: 10.6, 2: 11.95, 3: 12.27, 4: 11.02, 5: 12.05, 6: 13.01, 7: 11.39, 8: 10.1, 9: 12.03, 10: 12.6, 11: 11.52, 12: 12.8, 13: 11.18, 14: 11.51, 15: 11.44, 16: 10.31, 17: 10.24, 18: 12.13, 19: 12.96, 20: 10.61}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x44.py', 'PT': False}

params[0] = get_random_machine(seed = 0.882167025395479,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.882167025395479,complexity="high",force_linear=False,params=params)
