import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.7062518838915391, 'demand': {1: 9.544, 2: 9.878, 3: 6.743, 4: 5.456, 5: 1.238, 6: 5.161, 7: 4.081, 8: 8.093, 9: 5.171, 10: 3.739, 11: 6.698, 12: 1.333, 13: 7.779, 14: 1.202, 15: 5.741, 16: 9.962, 17: 6.55, 18: 3.296, 19: 0.284, 20: 5.696}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.7062518838915391,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.706251883891539,complexity="low",params=params)
