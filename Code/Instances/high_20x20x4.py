import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8464648998108447, 'demand': {1: 7.808, 2: 8.882, 3: 6.73, 4: 2.566, 5: 1.514, 6: 8.813, 7: 3.04, 8: 9.752, 9: 5.082, 10: 6.535, 11: 1.51, 12: 7.871, 13: 5.849, 14: 5.995, 15: 9.743, 16: 2.472, 17: 4.473, 18: 7.832, 19: 7.991, 20: 1.819}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.8464648998108447,complexity="high",params=params)
