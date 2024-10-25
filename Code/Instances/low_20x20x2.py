import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9081182987767402, 'demand': {1: 3.737, 2: 8.786, 3: 5.37, 4: 2.981, 5: 4.562, 6: 0.924, 7: 4.521, 8: 8.081, 9: 2.874, 10: 5.371, 11: 6.014, 12: 4.418, 13: 3.432, 14: 3.406, 15: 5.802, 16: 7.633, 17: 2.156, 18: 3.556, 19: 1.616, 20: 1.003}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.9081182987767402,complexity="low",params=params)
