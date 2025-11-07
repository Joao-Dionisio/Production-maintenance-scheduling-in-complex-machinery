import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.87909069356739, 'demand': {1: 11.3, 2: 11.09, 3: 13.28, 4: 10.5, 5: 12.41, 6: 12.14, 7: 10.15, 8: 12.78, 9: 12.97, 10: 12.09, 11: 12.45, 12: 12.71, 13: 10.46, 14: 11.75, 15: 11.68, 16: 12.78, 17: 12.68, 18: 12.75, 19: 11.95, 20: 12.98}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x21.py', 'PT': False}

params[0] = get_random_machine(seed = 0.87909069356739,complexity="high",force_linear=False,params=params)
