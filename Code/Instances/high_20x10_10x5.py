import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.3514442617106025, 'demand': {1: 13.22, 2: 10.01, 3: 12.79, 4: 10.7, 5: 12.92, 6: 10.11, 7: 13.22, 8: 12.53, 9: 13.3, 10: 11.93, 11: 10.59, 12: 13.23, 13: 11.47, 14: 10.28, 15: 12.02, 16: 11.66, 17: 11.58, 18: 10.52, 19: 10.41, 20: 11.94}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x5.py', 'PT': False}

params[0] = get_random_machine(seed = 0.3514442617106025,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3514442617106024,complexity="high",force_linear=False,params=params)
