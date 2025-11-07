import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.35044085737292974, 'demand': {1: 12.07, 2: 10.31, 3: 11.34, 4: 13.12, 5: 10.6, 6: 12.18, 7: 11.09, 8: 11.0, 9: 10.08, 10: 10.07}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'production_granularity': 1.0, 'discrete_production': 0, 'dual_stabilization': False, 'redcost_fixing': True, 'debug_mode': True, 'stop_at_error': True, 'force_linear': False, 'ARMP_use_original_pricing': False, 'filename': 'high_10x10_10x25.py', 'PT': False}

params[0] = get_random_machine(seed = 0.35044085737292974,complexity="high",force_linear=False,params=params)

params[1] = get_random_machine(seed = 1.3504408573729298,complexity="high",force_linear=False,params=params)
