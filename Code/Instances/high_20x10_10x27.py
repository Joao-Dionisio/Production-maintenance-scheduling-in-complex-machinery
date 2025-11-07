import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.1842722275734775, 'demand': {1: 11.62, 2: 11.9, 3: 12.35, 4: 11.46, 5: 12.56, 6: 10.1, 7: 11.16, 8: 10.4, 9: 11.72, 10: 11.91, 11: 11.94, 12: 11.48, 13: 11.23, 14: 11.1, 15: 10.35, 16: 10.64, 17: 11.62, 18: 11.89, 19: 10.33, 20: 12.82}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x27.py', 'PT': False}

params[0] = get_random_machine(seed = 0.1842722275734775,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.1842722275734774,complexity="high",force_linear=False,params=params)
