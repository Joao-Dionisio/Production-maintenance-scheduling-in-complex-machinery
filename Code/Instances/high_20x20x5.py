import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.26274661929853793, 'demand': {1: 10.01, 2: 11.4, 3: 11.23, 4: 11.89, 5: 13.18, 6: 12.3, 7: 11.72, 8: 12.06, 9: 12.25, 10: 10.18, 11: 13.0, 12: 12.6, 13: 12.92, 14: 12.66, 15: 11.31, 16: 11.33, 17: 10.35, 18: 12.11, 19: 10.21, 20: 10.22}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x5.py', 'PT': False}

params[0] = get_random_machine(seed = 0.26274661929853793,complexity="high",force_linear=False,params=params)
