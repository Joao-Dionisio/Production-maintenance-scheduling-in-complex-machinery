import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9716572889821583, 'demand': {1: 11.32, 2: 11.34, 3: 13.16, 4: 12.42, 5: 10.57, 6: 10.42, 7: 10.5, 8: 13.02, 9: 12.69, 10: 10.49, 11: 12.76, 12: 13.27, 13: 12.19, 14: 11.17, 15: 11.83, 16: 10.44, 17: 10.05, 18: 13.24, 19: 12.17, 20: 11.76}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x10.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9716572889821583,complexity="high",force_linear=False,params=params)
