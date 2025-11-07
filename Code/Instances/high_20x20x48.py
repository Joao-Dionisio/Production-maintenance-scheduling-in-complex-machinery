import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.49186996585042464, 'demand': {1: 13.19, 2: 13.05, 3: 10.55, 4: 12.63, 5: 13.1, 6: 10.22, 7: 11.17, 8: 12.52, 9: 10.53, 10: 12.99, 11: 10.92, 12: 12.72, 13: 10.48, 14: 11.67, 15: 13.07, 16: 10.69, 17: 10.88, 18: 11.69, 19: 11.06, 20: 10.12}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x48.py', 'PT': False}

params[0] = get_random_machine(seed = 0.49186996585042464,complexity="high",force_linear=False,params=params)
