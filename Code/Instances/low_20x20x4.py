import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.21751574770397586, 'demand': {1: 7.352, 2: 8.754, 3: 6.653, 4: 0.33, 5: 4.992, 6: 4.435, 7: 9.199, 8: 4.505, 9: 3.12, 10: 2.682, 11: 9.05, 12: 9.919, 13: 5.279, 14: 8.916, 15: 3.301, 16: 7.852, 17: 5.394, 18: 3.796, 19: 5.326, 20: 7.219}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.21751574770397586,complexity="low",params=params)
