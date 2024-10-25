import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8796901056058163, 'demand': {1: 8.127, 2: 7.781, 3: 4.752, 4: 7.062, 5: 9.132, 6: 8.918, 7: 0.79, 8: 5.12, 9: 8.189, 10: 2.091, 11: 1.495, 12: 1.527, 13: 0.313, 14: 5.612, 15: 0.188, 16: 6.256, 17: 9.389, 18: 1.335, 19: 3.06, 20: 6.661}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.8796901056058163,complexity="low",params=params)
