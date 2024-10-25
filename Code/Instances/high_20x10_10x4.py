import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.5229283564774138, 'demand': {1: 2.193, 2: 2.841, 3: 0.405, 4: 1.267, 5: 4.437, 6: 3.28, 7: 2.171, 8: 9.947, 9: 9.864, 10: 7.251, 11: 4.242, 12: 5.936, 13: 5.13, 14: 3.05, 15: 3.325, 16: 6.372, 17: 4.499, 18: 5.098, 19: 4.839, 20: 7.119}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.5229283564774138,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.5229283564774136,complexity="high",params=params)
