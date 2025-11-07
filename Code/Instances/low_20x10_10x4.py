import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7960988363360673, 'demand': {1: 11.72, 2: 11.57, 3: 12.35, 4: 11.36, 5: 10.29, 6: 12.49, 7: 10.89, 8: 11.63, 9: 12.61, 10: 10.57, 11: 10.07, 12: 10.41, 13: 11.96, 14: 11.2, 15: 10.85, 16: 11.51, 17: 13.09, 18: 10.85, 19: 11.37, 20: 12.93}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'low_20x10_10x4.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7960988363360673,complexity="low",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.7960988363360673,complexity="low",force_linear=False,params=params)
