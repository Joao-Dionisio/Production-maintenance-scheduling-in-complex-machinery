import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.2267058593810488, 'demand': {1: 0.865, 2: 7.782, 3: 9.343, 4: 6.75, 5: 0.857, 6: 6.719, 7: 8.503, 8: 0.928, 9: 0.448, 10: 7.904, 11: 4.29, 12: 8.195, 13: 5.192, 14: 9.146, 15: 1.938, 16: 6.818, 17: 9.699, 18: 9.677, 19: 3.101, 20: 3.23}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.2267058593810488,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.226705859381049,complexity="high",params=params)
