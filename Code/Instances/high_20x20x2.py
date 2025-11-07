import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7943794815224912, 'demand': {1: 12.33, 2: 10.81, 3: 11.91, 4: 11.75, 5: 12.92, 6: 12.43, 7: 10.96, 8: 13.27, 9: 10.39, 10: 11.39, 11: 12.52, 12: 10.51, 13: 11.63, 14: 10.13, 15: 12.23, 16: 12.55, 17: 11.91, 18: 12.92, 19: 11.05, 20: 12.32}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x2.py', 'PT': False}

params[0] = get_random_machine(seed = 0.7943794815224912,complexity="high",force_linear=False,params=params)
