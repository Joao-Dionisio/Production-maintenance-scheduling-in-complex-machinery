import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.6229016948897019, 'demand': {1: 0.925, 2: 3.996, 3: 9.612, 4: 8.405, 5: 1.851, 6: 2.909, 7: 4.853, 8: 9.172, 9: 1.799, 10: 3.041, 11: 1.226, 12: 7.784, 13: 6.998, 14: 4.363, 15: 9.721, 16: 3.598, 17: 7.297, 18: 2.858, 19: 2.866, 20: 4.821}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.6229016948897019,complexity="low",params=params)
