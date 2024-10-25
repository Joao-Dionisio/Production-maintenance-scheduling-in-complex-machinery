import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.14801889411281266, 'demand': {1: 1.295, 2: 3.885, 3: 7.982, 4: 2.401, 5: 4.248, 6: 1.052, 7: 1.376, 8: 0.618, 9: 9.881, 10: 6.713, 11: 5.58, 12: 2.482, 13: 6.27, 14: 7.61, 15: 9.353, 16: 9.627, 17: 0.547, 18: 5.19, 19: 5.834, 20: 1.954}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.14801889411281266,complexity="high",params=params)
