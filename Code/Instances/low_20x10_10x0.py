import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.793340083761663, 'demand': {1: 9.259, 2: 5.466, 3: 1.584, 4: 8.565, 5: 2.419, 6: 6.551, 7: 3.618, 8: 3.565, 9: 7.715, 10: 7.596, 11: 0.106, 12: 1.752, 13: 5.122, 14: 1.046, 15: 3.681, 16: 8.716, 17: 9.778, 18: 4.925, 19: 4.102, 20: 1.195}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.793340083761663,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.793340083761663,complexity="low",params=params)
