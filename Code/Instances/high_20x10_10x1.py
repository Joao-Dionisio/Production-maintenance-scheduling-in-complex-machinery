import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.08414689154985155, 'demand': {1: 6.535, 2: 3.272, 3: 7.389, 4: 3.642, 5: 0.357, 6: 2.169, 7: 3.624, 8: 0.166, 9: 0.083, 10: 3.893, 11: 0.742, 12: 8.391, 13: 4.236, 14: 8.481, 15: 2.85, 16: 0.658, 17: 8.74, 18: 5.241, 19: 4.684, 20: 5.551}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.08414689154985155,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.0841468915498516,complexity="high",params=params)
