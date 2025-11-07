import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.09463702768824811, 'demand': {1: 11.29, 2: 11.08, 3: 12.96, 4: 11.66, 5: 11.25, 6: 12.22, 7: 13.18, 8: 12.77, 9: 12.68, 10: 12.22, 11: 12.68, 12: 11.87, 13: 11.3, 14: 11.06, 15: 10.88, 16: 11.12, 17: 11.67, 18: 12.87, 19: 10.79, 20: 11.31}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x10_10x36.py', 'PT': False}

params[0] = get_random_machine(seed = 0.09463702768824811,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.0946370276882482,complexity="high",force_linear=False,params=params)
