import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.41609823658133804, 'demand': {1: 1.346, 2: 2.012, 3: 7.658, 4: 7.181, 5: 8.96, 6: 8.35, 7: 4.432, 8: 3.302, 9: 3.474, 10: 0.744, 11: 1.378, 12: 0.814, 13: 8.264, 14: 4.253, 15: 5.748, 16: 4.514, 17: 9.734, 18: 4.853, 19: 5.746, 20: 1.695}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.41609823658133804,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.416098236581338,complexity="low",params=params)
