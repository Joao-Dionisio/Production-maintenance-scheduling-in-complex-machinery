import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7794354979838684, 'demand': {1: 8.517, 2: 2.744, 3: 0.797, 4: 0.728, 5: 9.325, 6: 0.863, 7: 8.521, 8: 5.334, 9: 4.15, 10: 3.234, 11: 9.337, 12: 1.415, 13: 8.892, 14: 4.833, 15: 8.925, 16: 8.386, 17: 3.345, 18: 3.911, 19: 5.564, 20: 2.783}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.7794354979838684,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.7794354979838682,complexity="low",params=params)
