import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.008862279719864308, 'demand': {1: 2.707, 2: 8.379, 3: 4.446, 4: 3.051, 5: 8.396, 6: 3.838, 7: 5.041, 8: 8.088, 9: 8.184, 10: 1.576}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.008862279719864308,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.0088622797198643,complexity="low",params=params)
