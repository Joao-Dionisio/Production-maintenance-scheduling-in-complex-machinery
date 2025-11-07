import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7616088749444486, 'demand': {1: 12.84, 2: 10.75, 3: 12.07, 4: 11.34, 5: 12.22, 6: 13.26, 7: 12.12, 8: 10.04, 9: 11.55, 10: 12.37}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_10x10_10x28.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7616088749444486,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.7616088749444487,complexity="low",force_linear=False,params=params)
