import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9336248050574267, 'demand': {1: 11.45, 2: 12.91, 3: 12.75, 4: 10.7, 5: 10.84, 6: 10.98, 7: 10.8, 8: 11.95, 9: 10.86, 10: 11.4, 11: 10.44, 12: 13.03, 13: 11.18, 14: 11.53, 15: 11.94, 16: 13.01, 17: 11.4, 18: 13.06, 19: 11.67, 20: 11.77}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_20x20x11.py', 'PT': False}

params[0] = get_random_machine(seed = 0.9336248050574267,complexity="high",force_linear=False,params=params)
